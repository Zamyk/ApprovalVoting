from functools import partial
import random
from . import RESULTS_DIRECTORY_PATH
from ..manipulation_of_hamming import tests
from votekit.ballot_generator.std_generator.approval_impartial_culture import (
    approval_euclidean_generator,
)

APPROVE_RADIUS = 0.2

normal_dist = partial(random.gauss, 0.0, 1.0)
triangle_dist = partial(random.triangular, 0.0, 1.0, 0.5)

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
    "path": RESULTS_DIRECTORY_PATH / "experiment_1_euclidean_normal",
    "n_voters": 25,
    "n_iterations": 10000,
    "candidates": [3, 5, 6],
    "gen": euclidean_normal_generator,
    "n_jobs": -3,
    "verbose": True,
}

PARAMS_TRIANGLE = {
    "path": RESULTS_DIRECTORY_PATH / "experiment_1_euclidean_triangle",
    "n_voters": 25,
    "n_iterations": 10000,
    "candidates": [3, 4, 5],
    "gen": euclidean_triangle_generator,
    "n_jobs": -3,
    "verbose": True,
}


def run_experiment_1_euclidean(iterations=1):
    print("Starting experiment_1_euclidean")
    for i in range(iterations):
        print(f"Starting iteration {i+1}/{iterations}")
        PARAMS_NORMAL["path"] = RESULTS_DIRECTORY_PATH / f"experiment_1_euclidean_normal_{i}"
        PARAMS_TRIANGLE["path"] = RESULTS_DIRECTORY_PATH / f"experiment_1_euclidean_triangle_{i}"
        tests(**PARAMS_NORMAL)
        tests(**PARAMS_TRIANGLE)
    print("Completed experiment_1_euclidean")


if __name__ == "__main__":
    run_experiment_1_euclidean()
