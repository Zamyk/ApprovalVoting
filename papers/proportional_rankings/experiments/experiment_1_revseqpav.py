import os
from . import RESULTS_DIRECTORY_PATH, DATASETS_DIRECTORY_PATH
from ..proportional_rankings import experiment_1_one_rule, Reverse_Seq_PAV
from votekit.ballot_generator.std_generator.approval_impartial_culture import approval_ic_profile_generator, approval_biased_profile_generator



PARAMS = {
    "path_to_results": RESULTS_DIRECTORY_PATH / "experiment_1_revseqpav.csv",
    "path_to_profiles": DATASETS_DIRECTORY_PATH,
    "rule": Reverse_Seq_PAV,
    "n_jobs": -1,
    "verbose": True
}



def run_experiment_1_seqpav():
    print(f"Starting experiment_1_seqpav")
    experiment_1_one_rule(**PARAMS)
    print(f"Completed experiment_1_seqpav")


if __name__ == "__main__":
    run_experiment_1_seqpav()
