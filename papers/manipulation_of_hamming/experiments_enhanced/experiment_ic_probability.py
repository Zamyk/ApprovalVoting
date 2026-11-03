"""Manipulability of OrderedWeightedHamming rules in Impartial Culture as a function of the
approval probability p (each candidate is approved independently with probability p).
Fixed: 20 voters, 5 candidates, same rules as the variable-voters experiment."""
import random
from datetime import datetime
from functools import partial

import numpy as np

from . import RESULTS_DIRECTORY_PATH

import votekit.elections.election_types.approval.hamming as approval_module
from ..manipulation_of_hamming import _get_weights_on_int, get_manipulability_ratio, save_data
# integer weights (avoids floating point ties); the function was renamed in VoteKit
approval_module._get_hamming_weights = _get_weights_on_int

from votekit.ballot import ApprovalBallot
from votekit.pref_profile.approval_profile import ApprovalProfile

N_VOTERS = 20
CANDIDATES = ["A", "B", "C", "D", "E"]
PROBABILITIES = [round(i / 20, 2) for i in range(21)]
N_ITERATIONS = 10000
N_JOBS = -3

WEIGHTS_CONFIG = [
    ("f_2n_3", lambda n: ("f", n * 2 // 3)),
    ("f_n_2", lambda n: ("f", n // 2)),
    ("f_n_3", lambda n: ("f", n // 3)),
    ("Borda", lambda _: "Borda"),
]


def approval_ic_p_generator(candidates, number_of_ballots, p):
    """Impartial culture where each candidate is approved independently with probability p."""
    ballots = tuple(
        ApprovalBallot(approvals=[c for c in candidates if random.random() < p])
        for _ in range(number_of_ballots)
    )
    return ApprovalProfile(ballots=ballots, candidates=candidates)


def experiment_ic_probability(
    path=None,
    n_voters=N_VOTERS,
    candidates=CANDIDATES,
    probabilities=PROBABILITIES,
    n_iterations=N_ITERATIONS,
    weights=WEIGHTS_CONFIG,
    n_jobs=N_JOBS,
    verbose=True,
):
    path = path or RESULTS_DIRECTORY_PATH / "experiment_ic_probability"
    total = len(weights) * len(probabilities)
    results = []
    for p in probabilities:
        gen = partial(approval_ic_p_generator, p=p)
        for name, w in weights:
            ratio = get_manipulability_ratio(
                candidates, n_voters, gen, w(n_voters), n_iterations, n_jobs=n_jobs
            )
            results.append({"f": name, "p": p, "manipulability": ratio})
            if verbose:
                print(f"[{len(results) / total:.1%}] p={p} rule={name} manip={ratio:.4f}", flush=True)
    save_data(path.with_suffix(".csv"), results)
    return path.with_suffix(".csv")


def run_experiment_ic_probability():
    print(f"Starting experiment_ic_probability | time: {datetime.now()}", flush=True)
    experiment_ic_probability()
    print(f"Completed experiment_ic_probability | time: {datetime.now()}", flush=True)


if __name__ == "__main__":
    run_experiment_ic_probability()
