import os
from . import RESULTS_DIRECTORY_PATH, DATASETS_2_DIRECTORY_PATH
from functools import partial
from ..proportional_rankings import experiment_1_one_rule, AV

PARAMS = {
    "path_to_results": RESULTS_DIRECTORY_PATH / "experiment_1_datasets-2_av.csv",
    "path_to_profiles": DATASETS_2_DIRECTORY_PATH,
    "rule": AV,
    "n_jobs": -4,
    "verbose": True
}
 


def run_experiment_1_datasets_2_av():
    print(f"Starting experiment_1_datasets_av")
    experiment_1_one_rule(**PARAMS)
    print(f"Completed experiment_1_datasets_av")


if __name__ == "__main__":
    run_experiment_1_datasets_2_av()
