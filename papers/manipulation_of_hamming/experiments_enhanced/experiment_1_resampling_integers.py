"""Experiment 1 (manipulability vs orness, 25 voters, m = 3, 4, 5, integer weights) for the
(p, phi)-resampling model with p = 0.5 and phi in {0.3, 0.5, 0.8}."""
from datetime import datetime
from functools import partial
from . import RESULTS_DIRECTORY_PATH

import votekit.elections.election_types.approval.hamming as approval_module
from ..manipulation_of_hamming import _get_weights_on_int
approval_module._get_hamming_weights = _get_weights_on_int
from votekit.ballot_generator.std_generator.approval_impartial_culture import (
    approval_resampling_profile_generator,
)
from ..manipulation_of_hamming import experiment_1

P = 0.5
# (file tag, phi). No dots in the tag: Path.with_suffix would treat ".3" as an extension.
PHIS = [("phi03", 0.3), ("phi05", 0.5), ("phi08", 0.8)]


def make_params(tag, phi):
    return {
        "path": RESULTS_DIRECTORY_PATH / f"experiment_1_resampling_integers_{tag}",
        "n_voters": 25,
        "n_iterations": 10000,
        "candidates": [3, 4, 5],
        "gen": partial(approval_resampling_profile_generator, p=P, phi=phi),
        "n_jobs": -3,
        "verbose": True,
    }


def run_experiment_1_resampling_integers():
    print(f"Starting experiment_1_resampling_integers | time: {datetime.now()}", flush=True)
    for tag, phi in PHIS:
        print(f"p={P} phi={phi}", flush=True)
        experiment_1(**make_params(tag, phi))
    print(f"Completed experiment_1_resampling_integers | time: {datetime.now()}", flush=True)


if __name__ == "__main__":
    run_experiment_1_resampling_integers()
