import os
from datetime import datetime
from . import RESULTS_DIRECTORY_PATH
from ..manipulation_of_hamming import experiment_2
from votekit.ballot_generator.std_generator.approval_impartial_culture import approval_ic_profile_generator, approval_biased_profile_generator


WEIGHTS_CONFIG = [
        ("f_2n_3", lambda n: ('f', n * 2 // 3)),
        ("f_n_2",  lambda n: ('f', n // 2)),
        ("f_n_3",  lambda n: ('f', n // 3)),
        ("Borda",  lambda _: 'Borda')
    ]

PARAMS = {
    "path": RESULTS_DIRECTORY_PATH / "experiment_2_iterations",
    "voters": [n for n in range(5, 71, 5)],
    "n_iterations": 10000,
    "candidates": ["A", "B", "C", "D", "E"],
    "gen": approval_ic_profile_generator,
    "weights": WEIGHTS_CONFIG,
    "n_jobs": -3,
    "verbose": True
}


def run_experiment_2_iterations(iterations=50):
    print(f"Starting experiment_2_iterations | time: {datetime.now()}")
    for i in range(iterations):
        print(f"Starting iteration {i+1}/{iterations} | time: {datetime.now()}")
        PARAMS["path"] = RESULTS_DIRECTORY_PATH / f"experiment_2_iterations_{i}"
        experiment_2(**PARAMS)
    print(f"Completed experiment_2_iterations | time: {datetime.now()}")


if __name__ == "__main__":
    run_experiment_2_iterations()