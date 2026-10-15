import os
from datetime import datetime
from . import RESULTS_DIRECTORY_PATH

import votekit.elections.election_types.approval.hamming as approval_module
from ..manipulation_of_hamming import _get_weights_on_int
approval_module._get_weights = _get_weights_on_int
from votekit.ballot_generator.std_generator.approval_impartial_culture import (
    approval_ic_profile_generator,
    approval_biased_profile_generator
)
from ..manipulation_of_hamming import tests

PARAMS_1 = {
    "path": RESULTS_DIRECTORY_PATH / "experiment_1_integers_uniform",
    "n_voters": 25,
    "n_iterations": 10000,
    "candidates": [3, 4, 5],
    "gen": approval_ic_profile_generator,
    "n_jobs": -3,
    "verbose": True
}

PARAMS_2 = {
    "path": RESULTS_DIRECTORY_PATH / "experiment_1_integers_biased",
    "n_voters": 25,
    "n_iterations": 10000,
    "candidates": [3, 4, 5],
    "gen": approval_biased_profile_generator,
    "n_jobs": -3,
    "verbose": True
}


def run_experiment_1_integers():
    print(f"Starting experiment_1_integers | time: {datetime.now()}")
    PARAMS_1["path"] = RESULTS_DIRECTORY_PATH / f"experiment_1_integers_uniform"
    PARAMS_2["path"] = RESULTS_DIRECTORY_PATH / f"experiment_1_integers_biased"
    tests(**PARAMS_1)
    tests(**PARAMS_2)
    print(f"Completed experiment_1_integers | time: {datetime.now()}")


if __name__ == "__main__":
    run_experiment_1_integers()
