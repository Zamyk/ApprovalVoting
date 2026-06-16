import os
from . import RESULTS_DIRECTORY_PATH
from ..manipulation_of_hamming import tests
from votekit.ballot_generator.std_generator.approval_impartial_culture import approval_ic_profile_generator, approval_biased_profile_generator

print(RESULTS_DIRECTORY_PATH / "experiment_1_uniform.csv")

PARAMS_1 = {
    "path": RESULTS_DIRECTORY_PATH / "experiment_1_uniform.csv",
    "n_voters": 25,
    "n_iterations": 10000,
    "candidates": [3, 4, 5],
    "gen": approval_ic_profile_generator,
    "n_jobs": -2,
    "verbose": True
}

PARAMS_2 = {
    "path": RESULTS_DIRECTORY_PATH / "experiment_1_biased.csv",
    "n_voters": 25,
    "n_iterations": 10000,
    "candidates": [3, 4, 5],
    "gen": approval_biased_profile_generator,
    "n_jobs": -2,
    "verbose": True
}


def run_experiment_1():
    print(f"Starting experiment_1")
    tests(**PARAMS_1)
    tests(**PARAMS_2)
    print(f"Completed experiment_1")


if __name__ == "__main__":
    run_experiment_1()
