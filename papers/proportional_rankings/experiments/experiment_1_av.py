import os
from . import RESULTS_DIRECTORY_PATH, DATASETS_DIRECTORY_PATH
from ..proportional_rankings import experiment_1_one_rule, AV

PARAMS = {
    "path_to_results": RESULTS_DIRECTORY_PATH / "experiment_1_av.csv",
    "path_to_profiles": DATASETS_DIRECTORY_PATH,
    "rule": AV,
    "n_jobs": -1,
    "verbose": True
}


def run_experiment_1_av():
    print(f"Starting experiment_1")
    experiment_1_one_rule(**PARAMS)
    print(f"Completed experiment_1")


if __name__ == "__main__":
    run_experiment_1_av()
