import os
from . import RESULTS_DIRECTORY_PATH
import papers.manipulation_of_hamming.manipulation_of_hamming as manipulation_module
from ..manipulation_of_hamming import get_manipulability_ratio_e4_e5
manipulation_module.get_manipulability_ratio = get_manipulability_ratio_e4_e5
from votekit.ballot_generator.std_generator.approval_impartial_culture import approval_ic_profile_generator, approval_biased_profile_generator
from ..manipulation_of_hamming import tests

print(RESULTS_DIRECTORY_PATH / "experiment_4_uniform.csv")

PARAMS_1 = {
    "path": RESULTS_DIRECTORY_PATH / "experiment_4_uniform",
    "n_voters": 25,
    "n_iterations": 10000,
    "candidates": [3, 4, 5],
    "gen": approval_ic_profile_generator,
    "n_jobs": -3,
    "verbose": True
}

PARAMS_2 = {
    "path": RESULTS_DIRECTORY_PATH / "experiment_4_biased",
    "n_voters": 25,
    "n_iterations": 10000,
    "candidates": [3, 4, 5],
    "gen": approval_biased_profile_generator,
    "n_jobs": -3,
    "verbose": True
}


def run_experiment_4():
    print(f"Starting experiment_4")
    for i in range(50):
        print(f"Starting iteration {i+1}/50")
        PARAMS_1["path"] = RESULTS_DIRECTORY_PATH / f"experiment_4_uniform_{i}"
        PARAMS_2["path"] = RESULTS_DIRECTORY_PATH / f"experiment_4_biased_{i}"
        tests(**PARAMS_1)
        tests(**PARAMS_2)
    print(f"Completed experiment_4")


if __name__ == "__main__":
    run_experiment_4()
