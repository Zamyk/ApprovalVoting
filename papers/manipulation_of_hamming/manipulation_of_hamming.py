import numpy as np
import pandas as pd
from concurrent.futures import ProcessPoolExecutor
import os
import logging
from pathlib import Path

from votekit.pref_profile.approval_profile import ApprovalProfile
from votekit.elections.election_types.approval.hamming import OrderedWeightedHamming
from votekit.ballot_generator.std_generator.approval_impartial_culture import approval_ic_profile_generator, approval_biased_profile_generator
from votekit.comsoc.approval_manipulations import for_all_manipulations


def orness(n, fi):
    return (n + fi - 1) / (2 * (n - 1))


def get_elected_committee(profile, weights_type="minisum"):
    election = OrderedWeightedHamming(profile=profile, hamming_weights=weights_type)
    elected_tuple = election.get_elected()
    if not elected_tuple:
        return np.array([0 for c in profile.candidates])

    return np.array([c in elected_tuple[0] for c in profile.candidates])


def get_hamming_dist(ballot_vec, committee):
    return np.sum(ballot_vec != committee)


def can_voter_manipulate(voter_idx, profile, weights_type="minimax"):
    preference = profile.votes[voter_idx].copy()

    true_elected = get_elected_committee(profile, weights_type)
    true_dist = get_hamming_dist(preference, true_elected)

    is_manipulable = False

    def check_manipulation(manipulated_profile):
        nonlocal is_manipulable
        manipulated_elected = get_elected_committee(manipulated_profile, weights_type)
        dist = get_hamming_dist(preference, manipulated_elected)
        if dist < true_dist:
            is_manipulable = True
            return False
        return True

    for_all_manipulations(profile, voter_idx, check_manipulation)
    return is_manipulable


def _single_iteration(args):
    """Module-level function required for pickling with multiprocessing."""
    candidates, n_voters, weights_type, gen = args
    profile = gen(candidates, n_voters)
    for i in range(n_voters):
        if can_voter_manipulate(i, profile, weights_type):
            return 1
    return 0


def get_manipulability_ratio(candidates, n_voters, gen, weights_type, n_iterations, *, n_jobs=1, per_voter=False):
    """Share of profiles where some voter can manipulate; with ``per_voter`` the share of voters who can."""
    args = [(candidates, n_voters, weights_type, gen)] * n_iterations
    worker = _single_iteration_e4_e5 if per_voter else _single_iteration

    if n_jobs == 1:
        results = [worker(arg) for arg in args]
    else:
        if n_jobs == -1:
            n_jobs = os.cpu_count()
        elif n_jobs < -1:
            n_jobs = -int(os.cpu_count() / n_jobs)

        with ProcessPoolExecutor(max_workers=n_jobs) as executor:
            results = list(executor.map(worker, args, chunksize=max(1, n_iterations // (n_jobs * 4))))

    return sum(results) / n_iterations / (n_voters if per_voter else 1)


def save_data(path, data):
    df = pd.DataFrame(data)
    df.to_csv(path, index=False)


def experiment_1(path, n_voters, n_iterations, candidates, gen, *, n_jobs=1, verbose=True, integer_weights=False, per_voter=False):
    log_level = logging.INFO if verbose else logging.WARNING
    logging.basicConfig(level=log_level, format='%(message)s')

    results = []
    for i, m in enumerate(candidates):
        inner_candidates = [str(k) for k in range(m)]
        for j, fi in enumerate(range(n_voters)):
            manipulability_ratio = get_manipulability_ratio(inner_candidates, n_voters, gen, resolve_weights(("f", fi), n_voters, integer_weights), n_iterations, n_jobs=n_jobs, per_voter=per_voter)
            results.append({
                'm': m,
                'orness': orness(n_voters, fi),
                'manipulability': manipulability_ratio
            })
            logging.info(f"Calculations completion [{(i*n_voters+j+1)/(len(candidates)*n_voters):.2%}]")
        logging.info(f"Completed calculations for {m} candidates")
    save_data(path.with_suffix(".csv"), results)


def experiment_2(path, voters, n_iterations, candidates, gen, weights, *, n_jobs=1, verbose=True, integer_weights=False, per_voter=False):
    log_level = logging.INFO if verbose else logging.WARNING
    logging.basicConfig(level=log_level, format='%(message)s')

    results = []
    for i, (name, w) in enumerate(weights):
        for j, n in enumerate(voters):
            manipulability_ratio = get_manipulability_ratio(candidates, n, gen, resolve_weights(w(n), n, integer_weights), n_iterations, n_jobs=n_jobs, per_voter=per_voter)
            results.append({
                'f': name,
                'n': n,
                'manipulability': manipulability_ratio
            })
            logging.info(f"Calculations completion [{(i*len(voters)+j+1)/(len(weights)*len(voters)):.2%}]")
        logging.info(f"Completed calculations for weight {name}")
    save_data(path.with_suffix(".csv"), results)


def resolve_weights(weights, n, integer_weights=False):
    """Weights as passed to OrderedWeightedHamming.

    With ``integer_weights`` the spec ("minisum", ("f", i), ...) is turned into an explicit numpy
    array of integers (unnormalised: 1/0 or n..1), which VoteKit accepts as is. Integer weights
    make ties between committees exact instead of depending on floating point rounding.
    """
    if not integer_weights:
        return weights
    return _get_weights_on_int(weights, n)


def _get_weights_on_int(weights, n):
    if weights == "minisum":
        weights = ("f", 0)
    elif weights == "minimax":
        weights = ("f", n - 1)
    elif weights == "Borda":
        weights = [i for i in range(n, 0, -1)]

    if isinstance(weights, tuple) and weights[0] == "f":
        i = weights[1]
        assert i < n and i >= 0
        return np.array([1] * (n - i) + [0] * i)

    return np.array(weights)

def _single_iteration_e4_e5(args):
    """Module-level function required for pickling with multiprocessing."""
    candidates, n_voters, weights_type, gen = args
    profile = gen(candidates, n_voters)
    manipulating_voters = 0
    for i in range(n_voters):
        if can_voter_manipulate(i, profile, weights_type):
            manipulating_voters += 1
    return manipulating_voters

def _single_iteration_oneprofile(args):
    """Module-level function required for pickling with multiprocessing."""
    candidates, n_voters, weights_type, profile = args
    for i in range(n_voters):
        if can_voter_manipulate(i, profile, weights_type):
            return 1
    return 0


def _single_iteration_oneprofile_per_voter(args):
    """Module-level function required for pickling with multiprocessing."""
    candidates, n_voters, weights_type, profile = args
    return sum(can_voter_manipulate(i, profile, weights_type) for i in range(n_voters))


def get_manipulability_ratio_oneprofile(candidates, n_voters, weights_type, profiles, *, n_jobs=1, per_voter=False):
    """Same as get_manipulability_ratio, but on given profiles."""
    args = [(candidates, n_voters, weights_type, profile) for profile in profiles]
    worker = _single_iteration_oneprofile_per_voter if per_voter else _single_iteration_oneprofile

    if n_jobs == 1:
        results = [worker(arg) for arg in args]
    else:
        if n_jobs == -1:
            n_jobs = os.cpu_count()
        elif n_jobs < -1:
            n_jobs = -int(os.cpu_count() / n_jobs)

        with ProcessPoolExecutor(max_workers=n_jobs) as executor:
            results = list(executor.map(worker, args, chunksize=max(1, len(profiles) // (n_jobs * 4))))

    return sum(results) / len(profiles) / (n_voters if per_voter else 1)

def experiment_1_oneprofile(path, n_voters, n_iterations, candidates, gen, *, n_jobs=1, verbose=True, integer_weights=False, per_voter=False):
    log_level = logging.INFO if verbose else logging.WARNING
    logging.basicConfig(level=log_level, format='%(message)s')

    results = []
    for i, m in enumerate(candidates):
        inner_candidates = [str(k) for k in range(m)]
        profiles = [gen(inner_candidates, n_voters) for _ in range(n_iterations)]
        for j, fi in enumerate(range(n_voters)):
            manipulability_ratio = get_manipulability_ratio_oneprofile(inner_candidates, n_voters, resolve_weights(("f", fi), n_voters, integer_weights), profiles, n_jobs=n_jobs, per_voter=per_voter)
            results.append({
                'm': m,
                'orness': orness(n_voters, fi),
                'manipulability': manipulability_ratio
            })
            logging.info(f"Calculations completion [{(i*n_voters+j+1)/(len(candidates)*n_voters):.2%}]")
        logging.info(f"Completed calculations for {m} candidates")
    save_data(path.with_suffix(".csv"), results)