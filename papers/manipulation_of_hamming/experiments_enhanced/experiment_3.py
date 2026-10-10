import os
from . import RESULTS_DIRECTORY_PATH

import votekit.elections.election_types.approval.hamming as approval_module
from ..manipulation_of_hamming import _get_weights_on_int
approval_module._get_weights = _get_weights_on_int
from votekit.ballot_generator.std_generator.approval_impartial_culture import (
    approval_ic_profile_generator,
    approval_biased_profile_generator
)
from ..manipulation_of_hamming import tests

print(RESULTS_DIRECTORY_PATH / "experiment_3_uniform.csv")

PARAMS_1 = {
    "path": RESULTS_DIRECTORY_PATH / "experiment_3_uniform",
    "n_voters": 25,
    "n_iterations": 10000,
    "candidates": [3, 4, 5],
    "gen": approval_ic_profile_generator,
    "n_jobs": -3,
    "verbose": True
}

PARAMS_2 = {
    "path": RESULTS_DIRECTORY_PATH / "experiment_3_biased",
    "n_voters": 25,
    "n_iterations": 10000,
    "candidates": [3, 4, 5],
    "gen": approval_biased_profile_generator,
    "n_jobs": -3,
    "verbose": True
}


def run_experiment_3():
    print(f"Starting experiment_3")
    for i in range(1):
        print(f"Starting iteration {i+1}/50")
        PARAMS_1["path"] = RESULTS_DIRECTORY_PATH / f"experiment_3_uniform_{i}"
        PARAMS_2["path"] = RESULTS_DIRECTORY_PATH / f"experiment_3_biased_{i}"
        tests(**PARAMS_1)
        tests(**PARAMS_2)
    print(f"Completed experiment_3")


if __name__ == "__main__":
    run_experiment_3()
