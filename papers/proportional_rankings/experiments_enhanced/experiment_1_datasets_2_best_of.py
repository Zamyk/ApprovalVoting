import os
from . import RESULTS_DIRECTORY_PATH, DATASETS_2_DIRECTORY_PATH
from functools import partial
from ..proportional_rankings import experiment_1_one_rule, Best_of, Seq_Thile, Reverse_Seq_PAV, Phragmen, AV

RULES = [
    AV, 
    Seq_Thile, 
    Phragmen, 
    Seq_Thile, 
    Seq_Thile, 
    Seq_Thile,
    Seq_Thile, 
    Reverse_Seq_PAV
]

RULE_ARGS = [
    {}, 
    {"w": "GreedyCC"}, 
    {}, 
    {"w": "5/4-Geometric"}, 
    {"w": "2-Geometric"}, 
    {"w": "10-Geometric"},
    {"w": "SeqPav"}, 
    {}
]

PARAMS = {
    "path_to_results": RESULTS_DIRECTORY_PATH / "experiment_1_datasets-2_bestof.csv",
    "path_to_profiles": DATASETS_2_DIRECTORY_PATH,
    "rule": Best_of,
    "rule_args": {"rule_args": [(rule, args) for rule, args in zip(RULES, RULE_ARGS)]},
    "n_jobs": -3,
    "verbose": True
}
 




def run_experiment_1_datasets_2_bestof():
    print(f"Starting experiment_1_datasets_bestof")
    experiment_1_one_rule(**PARAMS)
    print(f"Completed experiment_1_datasets_bestof")


if __name__ == "__main__":
    run_experiment_1_datasets_2_bestof()
