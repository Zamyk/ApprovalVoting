import os
from . import RESULTS_DIRECTORY_PATH, DATASETS_DIRECTORY_PATH
from ..proportional_rankings import experiment_1_one_rule, AV
from votekit.ballot_generator.std_generator.approval_impartial_culture import approval_ic_profile_generator, approval_biased_profile_generator

PARAMS = {
    "path_to_results": RESULTS_DIRECTORY_PATH / "experiment_1.csv",
    "path_to_profiles": DATASETS_DIRECTORY_PATH,
    "rule": AV,
    "n_jobs": -1,
    "verbose": True
}


def run_experiment_1():
    print(f"Starting experiment_1")
    experiment_1_one_rule(**PARAMS)
    print(f"Completed experiment_1")


if __name__ == "__main__":
    run_experiment_1()
