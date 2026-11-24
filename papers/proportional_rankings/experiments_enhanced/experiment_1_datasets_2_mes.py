import os
from . import RESULTS_DIRECTORY_PATH, DATASETS_2_DIRECTORY_PATH
from ..proportional_rankings import experiment_1_one_rule, Method_of_Equal_Shares

PARAMS = {
    "path_to_results": RESULTS_DIRECTORY_PATH / "experiment_1_datasets-2_mes.csv",
    "path_to_profiles": DATASETS_2_DIRECTORY_PATH,
    "rule": Method_of_Equal_Shares,
    "n_jobs": -4,
    "verbose": True
}
 



def run_experiment_1_datasets_2_mes():
    print(f"Starting experiment_1_datasets_mes")
    experiment_1_one_rule(**PARAMS)
    print(f"Completed experiment_1_datasets_mes")


if __name__ == "__main__":
    run_experiment_1_datasets_2_mes()
