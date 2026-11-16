"""Experiment 2 (manipulability vs number of voters, 5 candidates, integer weights) for the
(p, phi)-resampling model with p = 0.5 and phi in {0.3, 0.5, 0.8}."""
from datetime import datetime
from functools import partial
from . import RESULTS_DIRECTORY_PATH

from votekit.ballot_generator.std_generator.approval_impartial_culture import (
    approval_resampling_profile_generator,
)
from ..manipulation_of_hamming import experiment_2

P = 0.5
# (file tag, phi). No dots in the tag: Path.with_suffix would treat ".3" as an extension.
PHIS = [("phi03", 0.3), ("phi05", 0.5), ("phi08", 0.8)]

WEIGHTS_CONFIG = [
    ("f_2n_3", lambda n: ("f", n * 2 // 3)),
    ("f_n_2", lambda n: ("f", n // 2)),
    ("f_n_3", lambda n: ("f", n // 3)),
    ("Borda", lambda _: "Borda"),
]


def make_params(tag, phi):
    return {
        "path": RESULTS_DIRECTORY_PATH / f"experiment_2_resampling_integers_{tag}",
        "voters": [n for n in range(5, 71, 5)],
        "n_iterations": 10000,
        "candidates": ["A", "B", "C", "D", "E"],
        "gen": partial(approval_resampling_profile_generator, p=P, phi=phi),
        "weights": WEIGHTS_CONFIG,
        "n_jobs": -3,
        "integer_weights": True,
        "verbose": True,
    }


def run_experiment_2_resampling_integers():
    print(f"Starting experiment_2_resampling_integers | time: {datetime.now()}", flush=True)
    for tag, phi in PHIS:
        print(f"p={P} phi={phi}", flush=True)
        experiment_2(**make_params(tag, phi))
    print(f"Completed experiment_2_resampling_integers | time: {datetime.now()}", flush=True)


if __name__ == "__main__":
    run_experiment_2_resampling_integers()
