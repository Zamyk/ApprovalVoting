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
    election = OrderedWeightedHamming(profile=profile, weights=weights_type)
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


def get_manipulability_ratio(candidates, n_voters, gen, weights_type, n_iterations, *, n_jobs=1):
    args = [(candidates, n_voters, weights_type, gen)] * n_iterations

    if n_jobs == 1:
        results = [_single_iteration(arg) for arg in args]
    else:
        if n_jobs == -1:
            n_jobs = os.cpu_count()
        elif n_jobs < -1:
            n_jobs = -int(os.cpu_count() / n_jobs)

        with ProcessPoolExecutor(max_workers=n_jobs) as executor:
            results = list(executor.map(_single_iteration, args, chunksize=max(1, n_iterations // (n_jobs * 4))))

    return sum(results) / n_iterations


def save_data(path, data):
    df = pd.DataFrame(data)
    df.to_csv(path, index=False)


def tests(path, n_voters, n_iterations, candidates, gen, *, n_jobs=1, verbose=True):
    log_level = logging.INFO if verbose else logging.WARNING
    logging.basicConfig(level=log_level, format='%(message)s')

    results = []
    for i, m in enumerate(candidates):
        inner_candidates = [str(k) for k in range(m)]
        for j, fi in enumerate(range(n_voters)):
            manipulability_ratio = get_manipulability_ratio(inner_candidates, n_voters, gen, ("f", fi), n_iterations, n_jobs=n_jobs)
            results.append({
                'm': m,
                'orness': orness(n_voters, fi),
                'manipulability': manipulability_ratio
            })
            logging.info(f"Calculations completion [{(i*n_voters+j+1)/(len(candidates)*n_voters):.2%}]")
        logging.info(f"Completed calculations for {m} candidates")
    save_data(path.with_suffix(".csv"), results)


def variable_voters_tests(path, voters, n_iterations, candidates, gen, weights, *, n_jobs=1, verbose=True):
    log_level = logging.INFO if verbose else logging.WARNING
    logging.basicConfig(level=log_level, format='%(message)s')

    results = []
    for i, (name, w) in enumerate(weights):
        for j, n in enumerate(voters):
            manipulability_ratio = get_manipulability_ratio(candidates, n, gen, w(n), n_iterations, n_jobs=n_jobs)
            results.append({
                'f': name,
                'n': n,
                'manipulability': manipulability_ratio
            })
            logging.info(f"Calculations completion [{(i*len(voters)+j+1)/(len(weights)*len(voters)):.2%}]")
        logging.info(f"Completed calculations for weight {name}")
    save_data(path.with_suffix(".csv"), results)

# if __name__ == "__main__":
#     TRIALS = 10000
#     tests("uniform_vk.csv", 25, TRIALS, [3, 4, 5], gen=approval_ic_profile_generator)
#     tests("biased_vk.csv", 25, TRIALS, [3, 4, 5], gen=approval_biased_profile_generator)

#     WEIGHTS_CONFIG = [
#         ("f_2n_3", lambda n: ('f', n * 2 // 3)),
#         ("f_n_2",  lambda n: ('f', n // 2)),
#         ("f_n_3",  lambda n: ('f', n // 3)),
#         ("Borda",  lambda n: 'Borda')
#     ]
#     variable_voters_tests("variable_voters.csv", [n for n in range(5, 71, 5)], TRIALS, ["A", "B", "C", "D", "E"], gen=approval_ic_profile_generator, weights = WEIGHTS_CONFIG)