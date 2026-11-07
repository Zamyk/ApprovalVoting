import os
from . import RESULTS_DIRECTORY_PATH, DATASETS_DIRECTORY_PATH
from functools import partial
from ..proportional_rankings import experiment_1_one_rule, Seq_Thile
from votekit.ballot_generator.std_generator.approval_impartial_culture import approval_ic_profile_generator, approval_biased_profile_generator

PARAMS_2_GEOMETRIC = {
    "path_to_results": RESULTS_DIRECTORY_PATH / "experiment_1_2_geometric.csv",
    "path_to_profiles": DATASETS_DIRECTORY_PATH,
    "rule": Seq_Thile,
    "rule_args": {"w": "2-Geometric"},
    "n_jobs": -1,
    "verbose": True
}

PARAMS_5_4_GEOMETRIC = {
    "path_to_results": RESULTS_DIRECTORY_PATH / "experiment_1_5_4_geometric.csv",
    "path_to_profiles": DATASETS_DIRECTORY_PATH,
    "rule": Seq_Thile,
    "rule_args": {"w": "5/4-Geometric"},
    "n_jobs": -1,
    "verbose": True
}

PARAMS_10_GEOMETRIC = {
    "path_to_results": RESULTS_DIRECTORY_PATH / "experiment_1_10_geometric.csv",
    "path_to_profiles": DATASETS_DIRECTORY_PATH,
    "rule": Seq_Thile,
    "rule_args": {"w": "10-Geometric"},
    "n_jobs": -1,
    "verbose": True
}

PARAMS_GREEDYCC = {
    "path_to_results": RESULTS_DIRECTORY_PATH / "experiment_1_greedycc.csv",
    "path_to_profiles": DATASETS_DIRECTORY_PATH,
    "rule": Seq_Thile,
    "rule_args": {"w": "GreedyCC"},
    "n_jobs": -1,
    "verbose": True
}

PARAMS_SEQPAV = {
    "path_to_results": RESULTS_DIRECTORY_PATH / "experiment_1_seqpav.csv",
    "path_to_profiles": DATASETS_DIRECTORY_PATH,
    "rule": Seq_Thile,
    "rule_args": {"w": "SeqPav"},
    "n_jobs": -1,
    "verbose": True
}



def run_experiment_1_thile():
    print(f"Starting experiment_1_thile")
    print(f"Starting experiment_1_2_geometric")
    experiment_1_one_rule(**PARAMS_2_GEOMETRIC)
    print(f"Completed experiment_1_2_geometric")

    print(f"Starting experiment_1_5_4_geometric")
    experiment_1_one_rule(**PARAMS_5_4_GEOMETRIC)
    print(f"Completed experiment_1_5_4_geometric")

    print(f"Starting experiment_1_10_geometric")
    experiment_1_one_rule(**PARAMS_10_GEOMETRIC)
    print(f"Completed experiment_1_10_geometric")

    print(f"Starting experiment_1_greedycc")
    experiment_1_one_rule(**PARAMS_GREEDYCC)
    print(f"Completed experiment_1_greedycc")

    print(f"Starting experiment_1_seqpav")
    experiment_1_one_rule(**PARAMS_SEQPAV)
    print(f"Completed experiment_1_seqpav")
    print(f"Completed experiment_1_thile")


if __name__ == "__main__":
    run_experiment_1_thile()
