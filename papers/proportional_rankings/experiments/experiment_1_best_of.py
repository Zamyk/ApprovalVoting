import os
from . import RESULTS_DIRECTORY_PATH, DATASETS_DIRECTORY_PATH
from ..proportional_rankings import experiment_1_one_rule, Best_of, Seq_Thile, Reverse_Seq_PAV, Phragmen, AV

RULES = [AV, Seq_Thile, Phragmen, 
              Seq_Thile, Seq_Thile, Seq_Thile,
              Seq_Thile, Reverse_Seq_PAV]

RULE_ARGS = [{}, {"w": "GreedyCC"}, {}, 
                  {"w": "5/4-Geometric"}, {"w": "2-Geometric"}, {"w": "10-Geometric"},
                  {"w": "SeqPav"}, {}]

PARAMS = {
    "path_to_results": RESULTS_DIRECTORY_PATH / "experiment_1_bestof.csv",
    "path_to_profiles": DATASETS_DIRECTORY_PATH,
    "rule": Best_of,
    "rule_args": [(rule, args) for rule, args in zip(RULES, RULE_ARGS)],
    "n_jobs": -1,
    "n_profiles_per_file": -10,
    "verbose": True
}



def run_experiment_1_bestof():
    print(f"Starting experiment_1_bestof")
    experiment_1_one_rule(**PARAMS)
    print(f"Completed experiment_1_bestof")


if __name__ == "__main__":
    run_experiment_1_bestof()
