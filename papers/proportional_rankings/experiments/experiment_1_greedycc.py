import os
from . import RESULTS_DIRECTORY_PATH, DATASETS_DIRECTORY_PATH
from ..proportional_rankings import experiment_1_one_rule, Seq_Thile


PARAMS = {
    "path_to_results": RESULTS_DIRECTORY_PATH / "experiment_1_greedycc.csv",
    "path_to_profiles": DATASETS_DIRECTORY_PATH,
    "rule": Seq_Thile,
    "rule_args": {"w": "GreedyCC"},
    "n_jobs": -1,
    "verbose": True
}



def run_experiment_1_greedycc():
    print(f"Starting experiment_1_greedycc")
    experiment_1_one_rule(**PARAMS)
    print(f"Completed experiment_1_greedycc")


if __name__ == "__main__":
    run_experiment_1_greedycc()
