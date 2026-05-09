import numpy as np
import pandas as pd
from concurrent.futures import ProcessPoolExecutor
import os

from votekit.pref_profile.approval_profile import ApprovalProfile
from votekit.elections.election_types.approval.hamming import OrderedWeightedHamming
from votekit.ballot_generator.std_generator.approval_impartial_culture import approval_ic_profile_generator, approval_biased_profile_generator

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
    candidates = profile.candidates
    n_cands = len(candidates)

    preference = profile.votes[voter_idx].copy()

    true_elected = get_elected_committee(profile, weights_type)
    true_dist = get_hamming_dist(preference, true_elected)

    for mask in range(1 << n_cands):
        new_vote_vec = np.array([(mask >> i) & 1 for i in range(n_cands)], dtype=bool)

        profile.votes[voter_idx] = new_vote_vec
        manipulated_elected = get_elected_committee(profile, weights_type)
        dist = get_hamming_dist(preference, manipulated_elected)
        profile.votes[voter_idx] = preference

        if dist < true_dist:
            return True

    return False

def _single_iteration(args):
    """Module-level function required for pickling with multiprocessing."""
    candidates, n_voters, weights_type, gen = args
    profile = gen(candidates, n_voters)
    for i in range(n_voters):
        if can_voter_manipulate(i, profile, weights_type):
            return 1
    return 0

def get_manipulability_ratio(candidates, n_voters, gen, weights_type, n_iterations):
    n_jobs = os.cpu_count()
    args = [(candidates, n_voters, weights_type, gen)] * n_iterations

    with ProcessPoolExecutor(max_workers=n_jobs) as executor:
        results = list(executor.map(_single_iteration, args, chunksize=max(1, n_iterations // (n_jobs * 4))))

    return sum(results) / n_iterations


def save_data(path, data):
    df = pd.DataFrame(data)
    df.to_csv(path, index=False)

def tests(path, n_voters, trials, m_candidates, gen):
    results = []
    for m in m_candidates:
        candidates = [str(i) for i in range(m)]
        for fi in range(n_voters):
            manipulability_ratio = get_manipulability_ratio(candidates, n_voters, gen, ("f", fi), trials)
            results.append({
                'm': m,
                'orness': orness(n_voters, fi),
                'manipulability': manipulability_ratio
            })
        print(f"Completed calculations for m={m}")
    save_data(path, results)

def variable_voters_tests(path, n_voters, trials, candidates, gen, weights):
    results = []
    for name, w in weights:
        for n in n_voters:
            manipulability_ratio = get_manipulability_ratio(candidates, n, gen, w(n), trials)
            results.append({
                'f': name,
                'n': n,
                'manipulability': manipulability_ratio
            })
    save_data(path, results)

if __name__ == "__main__":
    TRIALS = 1000
    #tests("uniform_vk.csv", 25, TRIALS, [3, 4, 5], gen=approval_ic_profile_generator)
    # tests("biased_vk.csv", 25, TRIALS, [3, 4, 5], gen=approval_biased_profile_generator)
    # variable_voters_tests("variable_voters.csv", [n for n in range(5, 20)], TRIALS, ["A", "B", "C", "D", "E"], gen=approval_ic_profile_generator, weights = 
    #       [("f2n/3", lambda x : ('f', x * 2 // 3)), ("f2n/3", lambda x : ('fn/2', x // 2)), ("f2n/3", lambda x : ('fn/3', x // 3)), ("Borda", lambda x : 'Borda')])

    WEIGHTS_CONFIG = [
        ("f_2n_3", lambda n: ('f', n * 2 // 3)),
        ("f_n_2",  lambda n: ('f', n // 2)),
        ("f_n_3",  lambda n: ('f', n // 3)),
        ("Borda",  lambda n: 'Borda')
    ]
    variable_voters_tests("variable_voters.csv", [n for n in range(5, 71, 5)], TRIALS, ["A", "B", "C", "D", "E"], gen=approval_ic_profile_generator, weights = WEIGHTS_CONFIG)