"""Experiment 1 (manipulability vs orness, 25 voters, m = 3, 4, 5, integer weights, one profile set shared across all f) for the
(p, phi)-resampling model with p = 0.5 and phi in {0.25, 0.5, 0.75}."""
from datetime import datetime
from functools import partial
from . import RESAMPLING_P as P, RESAMPLING_PHIS as PHIS, RESULTS_DIRECTORY_PATH

from votekit.ballot_generator.std_generator.approval_impartial_culture import (
    approval_resampling_profile_generator,
)
from ..manipulation_of_hamming import experiment_1_oneprofile


def make_params(tag, phi):
    return {
        "path": RESULTS_DIRECTORY_PATH / f"experiment_1_resampling_integers_oneprofile_{tag}",
        "n_voters": 25,
        "n_iterations": 10000,
        "candidates": [3, 4, 5],
        "gen": partial(approval_resampling_profile_generator, p=P, phi=phi),
        "n_jobs": -2,
        "integer_weights": True,
        "verbose": True,
    }


def run_experiment_1_resampling_integers_oneprofile():
    print(f"Starting experiment_1_resampling_integers_oneprofile | time: {datetime.now()}", flush=True)
    for tag, phi in PHIS:
        print(f"p={P} phi={phi}", flush=True)
        experiment_1_oneprofile(**make_params(tag, phi))
    print(f"Completed experiment_1_resampling_integers_oneprofile | time: {datetime.now()}", flush=True)


if __name__ == "__main__":
    run_experiment_1_resampling_integers_oneprofile()
