import os
from . import DATASETS_DIRECTORY_PATH
from ..proportional_rankings import experiment_1_generate_datasets
from votekit.ballot_generator.std_generator.approval_impartial_culture import approval_urn_model_generator

N_ALL_INSTANCES = 75000

gen_params_list = [
        {
            "candidates": [str(num) for num in range(m)],
            "number_of_ballots": n,
        } for m in range(9, 15 + 1) for n in range(200, 600 + 1)
    ]

n_possible_parameters = len(gen_params_list)

N_INSTANCES_PER_PARAMETER = N_ALL_INSTANCES // n_possible_parameters + 1

PARAMS = {
    "path": None,
    "gen_params": None,
    "n_iterations": N_INSTANCES_PER_PARAMETER,
    "gen": approval_urn_model_generator,
    "n_jobs": -2,
    "verbose": True
}



def run_experiment_1():
    print(f"Starting experiment_1")
    for i in range(n_possible_parameters):
        PARAMS['gen_params'] = gen_params_list[i]
        candidates = len(PARAMS['gen_params']['candidates'])
        ballots = PARAMS['gen_params']['number_of_ballots']
        gen_name = PARAMS['gen'].__name__
        PARAMS["path"] = DATASETS_DIRECTORY_PATH / f"experiment_1_dataset_gen_{gen_name}_candidates_{candidates}_ballots_{ballots}_profiles_{N_INSTANCES_PER_PARAMETER}.pkl"
        print(f"Generating dataset for {gen_name} with candidates={candidates} and ballots={ballots}")
        experiment_1_generate_datasets(**PARAMS)
    print(f"Completed experiment_1")


if __name__ == "__main__":
    run_experiment_1()
