from functools import partial
import random
from . import RESULTS_DIRECTORY_PATH
from ..manipulation_of_hamming import variable_voters_tests
from votekit.ballot_generator.std_generator.approval_impartial_culture import (
    approval_euclidean_generator,
)

APPROVE_RADIUS = 0.2

WEIGHTS_CONFIG = [
    ("f_2n_3", lambda n: ("f", n * 2 // 3)),
    ("f_n_2", lambda n: ("f", n // 2)),
    ("f_n_3", lambda n: ("f", n // 3)),
    ("Borda", lambda _: "Borda"),
]

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
    "path": RESULTS_DIRECTORY_PATH / "experiment_2_euclidean_normal",
    "voters": [n for n in range(5, 71, 5)],
    "n_iterations": 10000,
    "candidates": ["A", "B", "C", "D", "E"],
    "gen": euclidean_normal_generator,
    "weights": WEIGHTS_CONFIG,
    "n_jobs": -3,
    "verbose": True,
}

PARAMS_TRIANGLE = {
    "path": RESULTS_DIRECTORY_PATH / "experiment_2_euclidean_triangle",
    "voters": [n for n in range(5, 71, 5)],
    "n_iterations": 10000,
    "candidates": ["A", "B", "C", "D", "E"],
    "gen": euclidean_triangle_generator,
    "weights": WEIGHTS_CONFIG,
    "n_jobs": -3,
    "verbose": True,
}


def run_experiment_2_euclidean(iterations=1):
    print("Starting experiment_2_euclidean")
    for i in range(iterations):
        print(f"Starting iteration {i+1}/{iterations}")
        PARAMS_NORMAL["path"] = RESULTS_DIRECTORY_PATH / f"experiment_2_euclidean_normal_{i}"
        PARAMS_TRIANGLE["path"] = RESULTS_DIRECTORY_PATH / f"experiment_2_euclidean_triangle_{i}"
        variable_voters_tests(**PARAMS_NORMAL)
        variable_voters_tests(**PARAMS_TRIANGLE)
    print("Completed experiment_2_euclidean")


if __name__ == "__main__":
    run_experiment_2_euclidean()
