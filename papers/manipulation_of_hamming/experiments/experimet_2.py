import os
from . import RESULTS_DIRECTORY_PATH
from ..manipulation_of_hamming import variable_voters_tests
from votekit.ballot_generator.std_generator.approval_impartial_culture import approval_ic_profile_generator, approval_biased_profile_generator


WEIGHTS_CONFIG = [
        ("f_2n_3", lambda n: ('f', n * 2 // 3)),
        ("f_n_2",  lambda n: ('f', n // 2)),
        ("f_n_3",  lambda n: ('f', n // 3)),
        ("Borda",  lambda _: 'Borda')
    ]

PARAMS = {
    "path": RESULTS_DIRECTORY_PATH / "experiment_2.csv",
    "n_voters": [n for n in range(5, 71, 5)],
    "trials": 10000,
    "candidates": ["A", "B", "C", "D", "E"],
    "gen": approval_ic_profile_generator,
    "weights": WEIGHTS_CONFIG
}


def run_experiment_2():
    print(f"Starting experiment_2")
    variable_voters_tests(**PARAMS)
    print(f"Completed experiment_2")


if __name__ == "__main__":
    run_experiment_2()