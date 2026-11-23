import os
from . import RESULTS_DIRECTORY_PATH, DATASETS_2_DIRECTORY_PATH
from functools import partial
from ..proportional_rankings import experiment_1_one_rule, Phragmen

PARAMS = {
    "path_to_results": RESULTS_DIRECTORY_PATH / "experiment_1_datasets-2_phragmen.csv",
    "path_to_profiles": DATASETS_2_DIRECTORY_PATH,
    "rule": Phragmen,
    "n_jobs": -4,
    "verbose": True
}
 





def run_experiment_1_datasets_2_phragmen():
    print(f"Starting experiment_1_datasets_phragmen")
    experiment_1_one_rule(**PARAMS)
    print(f"Completed experiment_1_datasets_phragmen")


if __name__ == "__main__":
    run_experiment_1_datasets_2_phragmen()
