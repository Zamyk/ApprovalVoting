from functools import partial
import random
from datetime import datetime
from . import RESULTS_DIRECTORY_PATH

import votekit.elections.election_types.approval.hamming as approval_module
from ..manipulation_of_hamming import _get_weights_on_int
approval_module._get_weights = _get_weights_on_int

from votekit.ballot_generator.std_generator.approval_impartial_culture import (
    approval_euclidean_generator,
)
from ..manipulation_of_hamming import tests_oneprofile

APPROVE_RADIUS = 0.2

normal_dist = partial(random.gauss, 0.0, 0.5)
triangle_dist = partial(random.triangular, -1.0, 1.0, 0.)

euclidean_normal_generator = partial(
    approval_euclidean_generator,
    candidate_distribution=normal_dist,
    votes_distribution=normal_dist,
    approve_radius=APPROVE_RADIUS,
)

euclidean_triangle_generator = partial(
    approval_euclidean_generator,
    candidate_distribution=triangle_dist,
    votes_distribution=triangle_dist,
    approve_radius=APPROVE_RADIUS,
)

PARAMS_NORMAL = {
    "path": RESULTS_DIRECTORY_PATH / "experiment_1_euclidean_integers_oneprofile_normal",
    "n_voters": 25,
    "n_iterations": 10000,
    "candidates": [3, 4, 5],
    "gen": euclidean_normal_generator,
    "n_jobs": -3,
    "verbose": True,
}

PARAMS_TRIANGLE = {
    "path": RESULTS_DIRECTORY_PATH / "experiment_1_euclidean_integers_oneprofile_triangle",
    "n_voters": 25,
    "n_iterations": 10000,
    "candidates": [3, 4, 5],
    "gen": euclidean_triangle_generator,
    "n_jobs": -3,
    "verbose": True,
}


def run_experiment_1_euclidean_integers_oneprofile(iterations=1):
    print(f"Starting experiment_1_euclidean_integers_oneprofile | time: {datetime.now()}")
    PARAMS_NORMAL["path"] = RESULTS_DIRECTORY_PATH / f"experiment_1_euclidean_integers_oneprofile_normal"
    PARAMS_TRIANGLE["path"] = RESULTS_DIRECTORY_PATH / f"experiment_1_euclidean_integers_oneprofile_triangle"
    tests_oneprofile(**PARAMS_NORMAL)
    tests_oneprofile(**PARAMS_TRIANGLE)
    print(f"Completed experiment_1_euclidean_integers_oneprofile | time: {datetime.now()}")


if __name__ == "__main__":
    run_experiment_1_euclidean_integers_oneprofile()
