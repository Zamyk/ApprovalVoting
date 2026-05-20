import os
from . import RESULTS_DIRECTORY_PATH
from ..manipulation_of_hamming import tests
from votekit.ballot_generator.std_generator.approval_impartial_culture import approval_ic_profile_generator, approval_biased_profile_generator

print(RESULTS_DIRECTORY_PATH / "experiment_1_uniform.csv")

PARAMS_1 = {
    "path": RESULTS_DIRECTORY_PATH / "experiment_1_uniform",
    "n_voters": 25,
    "n_iterations": 1,
    "candidates": [3, 4, 5],
    "gen": approval_ic_profile_generator,
    "n_jobs": -3,
    "verbose": True
}

PARAMS_2 = {
    "path": RESULTS_DIRECTORY_PATH / "experiment_1_biased",
    "n_voters": 25,
    "n_iterations": 1,
    "candidates": [3, 4, 5],
    "gen": approval_biased_profile_generator,
    "n_jobs": -3,
    "verbose": True
}


def run_experiment_1():
    print(f"Starting experiment_1")
    for i in range(50):
        print(f"Starting iteration {i+1}/50")
        PARAMS_1["path"] = RESULTS_DIRECTORY_PATH / f"experiment_1_uniform_{i}"
        PARAMS_2["path"] = RESULTS_DIRECTORY_PATH / f"experiment_1_biased_{i}"
        tests(**PARAMS_1)
        tests(**PARAMS_2)
    print(f"Completed experiment_1")


if __name__ == "__main__":
    run_experiment_1()
