import os
from . import RESULTS_DIRECTORY_PATH
import papers.manipulation_of_hamming.manipulation_of_hamming as manipulation_module
from ..manipulation_of_hamming import get_manipulability_ratio_e4_e5
manipulation_module.get_manipulability_ratio = get_manipulability_ratio_e4_e5
from votekit.ballot_generator.std_generator.approval_impartial_culture import approval_ic_profile_generator, approval_biased_profile_generator
from ..manipulation_of_hamming import variable_voters_tests


WEIGHTS_CONFIG = [
        ("f_2n_3", lambda n: ('f', n * 2 // 3)),
        ("f_n_2",  lambda n: ('f', n // 2)),
        ("f_n_3",  lambda n: ('f', n // 3)),
        ("Borda",  lambda _: 'Borda')
    ]

PARAMS = {
    "path": RESULTS_DIRECTORY_PATH / "experiment_5",
    "voters": [n for n in range(5, 71, 5)],
    "n_iterations": 100,
    "candidates": ["A", "B", "C", "D", "E"],
    "gen": approval_ic_profile_generator,
    "weights": WEIGHTS_CONFIG,
    "n_jobs": -3,
    "verbose": True
}


def run_experiment_5():
    print(f"Starting experiment_5")
    for i in range(1):
        print(f"Starting iteration {i+1}/50")
        PARAMS["path"] = RESULTS_DIRECTORY_PATH / f"experiment_5_{i}"
        variable_voters_tests(**PARAMS)
    print(f"Completed experiment_5")


if __name__ == "__main__":
    run_experiment_5()