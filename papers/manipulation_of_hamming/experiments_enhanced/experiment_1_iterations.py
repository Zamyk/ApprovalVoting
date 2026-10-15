import os
from datetime import datetime
from . import RESULTS_DIRECTORY_PATH
from ..manipulation_of_hamming import experiment_1
from votekit.ballot_generator.std_generator.approval_impartial_culture import approval_ic_profile_generator, approval_biased_profile_generator

print(RESULTS_DIRECTORY_PATH / "experiment_1_iterations_uniform.csv")

PARAMS_1 = {
    "path": RESULTS_DIRECTORY_PATH / "experiment_1_iterations_uniform",
    "n_voters": 25,
    "n_iterations": 10000,
    "candidates": [3, 4, 5],
    "gen": approval_ic_profile_generator,
    "n_jobs": -3,
    "verbose": True
}

PARAMS_2 = {
    "path": RESULTS_DIRECTORY_PATH / "experiment_1_iterations_biased",
    "n_voters": 25,
    "n_iterations": 10000,
    "candidates": [3, 4, 5],
    "gen": approval_biased_profile_generator,
    "n_jobs": -3,
    "verbose": True
}


def run_experiment_1_iterations(iterations=50):
    print(f"Starting experiment_1_iterations | time: {datetime.now()}")
    for i in range(iterations):
        print(f"Starting iteration {i+1}/{iterations} | time: {datetime.now()}")
        PARAMS_1["path"] = RESULTS_DIRECTORY_PATH / f"experiment_1_iterations_uniform_{i}"
        PARAMS_2["path"] = RESULTS_DIRECTORY_PATH / f"experiment_1_iterations_biased_{i}"
        experiment_1(**PARAMS_1)
        experiment_1(**PARAMS_2)
    print(f"Completed experiment_1_iterations | time: {datetime.now()}")


if __name__ == "__main__":
    run_experiment_1_iterations()
