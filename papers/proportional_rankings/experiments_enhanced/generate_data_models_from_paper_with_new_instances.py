import os
from . import DATASETS_2_DIRECTORY_PATH
from ..proportional_rankings import experiment_1_generate_datasets
from votekit.ballot_generator.std_generator.approval_impartial_culture import approval_urn_model_generator, approval_ic_profile_generator, approval_spatial_model_with_districts_generator, approval_k_groups_generator

N_ALL_INSTANCES = 75000

gen_params_list = [
        {
            "candidates": [str(num) for num in range(m)],
            "number_of_ballots": n,
        } for m in range(2, 15 + 1) for n in range(2, 600 + 1)
    ]

n_possible_parameters = len(gen_params_list)

N_INSTANCES_PER_PARAMETER = N_ALL_INSTANCES // n_possible_parameters + 1

PARAMS_1 = {
    "path": None,
    "gen_params": None,
    "n_iterations": N_INSTANCES_PER_PARAMETER,
    "gen": approval_urn_model_generator,
    "n_jobs": -2,
    "verbose": True
}

PARAMS_2 = {
    "path": None,
    "gen_params": None,
    "n_iterations": N_INSTANCES_PER_PARAMETER,
    "gen": approval_ic_profile_generator,
    "n_jobs": -2,
    "verbose": True
}

PARAMS_3 = {
    "path": None,
    "gen_params": None,
    "n_iterations": N_INSTANCES_PER_PARAMETER,
    "gen": approval_spatial_model_with_districts_generator,
    "n_jobs": -2,
    "verbose": True
}

PARAMS_4 = {
    "path": None,
    "gen_params": None,
    "n_iterations": N_INSTANCES_PER_PARAMETER,
    "gen": approval_k_groups_generator,
    "n_jobs": -2,
    "verbose": True
}

PARAMS_LIST = [PARAMS_1, PARAMS_2, PARAMS_3, PARAMS_4]


def run_experiment_1():
    print(f"Starting experiment_1 data generation")
    for PARAMS in PARAMS_LIST:
        for i in range(n_possible_parameters):
            PARAMS['gen_params'] = gen_params_list[i]
            candidates = len(PARAMS['gen_params']['candidates'])
            ballots = PARAMS['gen_params']['number_of_ballots']
            gen_name = PARAMS['gen'].__name__
            PARAMS["path"] = DATASETS_2_DIRECTORY_PATH / f"experiment_1_dataset_gen_{gen_name}_candidates_{candidates}_ballots_{ballots}_profiles_{N_INSTANCES_PER_PARAMETER}.pkl"
            
            if PARAMS['gen'] == approval_urn_model_generator:
                max_approved = min(8, candidates)
                min_approved = min(5, max_approved)
                PARAMS['gen_params']["max_candidates_approved"] = max_approved
                PARAMS['gen_params']["min_candidates_approved"] = min_approved
                
            print(f"Generating dataset for {gen_name} with candidates={candidates} and ballots={ballots}")
            experiment_1_generate_datasets(**PARAMS)
    print(f"Completed experiment_1 data generation")


if __name__ == "__main__":
    run_experiment_1()
