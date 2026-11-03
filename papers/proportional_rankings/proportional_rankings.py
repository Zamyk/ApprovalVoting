import numpy as np
import pandas as pd
from concurrent.futures import ProcessPoolExecutor
import os
import logging
from pathlib import Path
import pickle
import random
from itertools import combinations
from typing import Any
from collections.abc import Callable
from dataclasses import dataclass

from votekit.elections.election_types.approval.proportional_rankings import avg_devided_by_jd
from votekit.pref_profile.approval_profile import ApprovalProfile, ApprovalBallot


# @dataclass(frozen=True)
# class ProfileGeneratingConfig:
#     n_candidates_interval: tuple[int, int]
#     n_voters_interval: tuple[int, int]
#     profile_generator: Callable[..., ApprovalProfile]
#     n_iterations: int


def dump_data(data: Any, path: str) -> None:
    with open(path, "wb") as file:
        pickle.dump(data, file, protocol=pickle.HIGHEST_PROTOCOL)

def read_data(path: str) -> Any:
    with open(path, "rb") as file:
        return pickle.load(file)

# # --- PRZYKŁAD UŻYCIA ---
# moje_dane = {"identyfikator": 123, "wartosci": [1.5, 2.5, 3.5]}

# # Zapis
# dump_data(moje_dane, "magazyn.pkl")

# # Odczyt
# wczytane_dane = read_data("magazyn.pkl")
# print(wczytane_dane)


def AV(profile: ApprovalProfile):
    scores = {c: 0 for c in profile.candidates} 
    for ballot in profile.ballots:
        if ballot.approvals:
            for approves in ballot.approvals:
                scores[approves] += ballot.weight

    scores = list(scores.items())
    scores = sorted(scores, key=lambda item: item[1], reverse=True)
    ranking = [item[0] for item in scores]
    return ranking

# ballots = [ApprovalBallot(approvals=["A","B","C","D"]),
#            ApprovalBallot(approvals=["D","B","C"]),
#            ApprovalBallot(approvals=["B","C"]),
#            ApprovalBallot(approvals=["C"])]

# profile = ApprovalProfile(ballots=ballots, candidates=["A","B","C","D"])

# print(AV(profile))



def save_data(path, data):
    df = pd.DataFrame(data)
    df.to_csv(path, index=False)

def get_cohesive_voter_groups(profile: ApprovalProfile) -> list[set[int]]:
  """Generuje wszystkie maksymalne grupy wyborców mające co najmniej 1 wspólnego kandydata.

  Zwraca listę zbiorów indeksów wyborców.
  """
  n_voters = len(profile.ballots)
  candidates = profile.candidates
  voter_groups = []
  seen_groups = set()

  # Przeglądamy podzbiory kandydatów o długości 1, 2, ..., m
  # W praktyce rzadko grupy aprobują wspólnie więcej niż kilka kandydatek
  for r in range(1, len(candidates) + 1):
    for cand_subset in combinations(candidates, r):
      cand_set = set(cand_subset)

      # Znajdujemy wszystkich wyborców, którzy aprobują WSZYSTKIE kandydata z cand_set
      matching_voters = set()
      for voter_idx, ballot in enumerate(profile.ballots):
        if ballot.approvals and cand_set.issubset(ballot.approvals):
          matching_voters.add(voter_idx)

      # Jeśli grupa istnieje i jeszcze jej nie rozważaliśmy
      if matching_voters:
        group_key = frozenset(matching_voters)
        if group_key not in seen_groups:
          seen_groups.add(group_key)
          voter_groups.append(matching_voters)

  return voter_groups

@dataclass(frozen=True)
class ProfileGeneratingConfig:
    candidates: tuple[int, int]
    number_of_ballots: tuple[int, int]


def experiment_1_generate_datasets(path, gen_params: ProfileGeneratingConfig, gen, n_iterations, *, n_jobs=1, verbose=True):
    log_level = logging.INFO if verbose else logging.WARNING
    logging.basicConfig(level=log_level, format='%(message)s')

    profiles = []

    for i in range(n_iterations):
        if i % 100 == 0:
            logging.info(f"Profiles generation completion [{(i)/n_iterations:.2%}]")
            dump_data(profiles, path)

        profiles.append(gen(**gen_params))

    dump_data(profiles, path)
    logging.info(f"Profiles generation completed")
        



def experiment_1_one_rule(path_to_profiles, path_to_results, rule, *, n_jobs=1, verbose=True):
    log_level = logging.INFO if verbose else logging.WARNING
    logging.basicConfig(level=log_level, format='%(message)s')

    profiles_to_process = 0
    for file in os.listdir(path_to_profiles):
        if file.endswith(".pkl"):
            dataset_path = os.path.join(path_to_profiles, file)
            profiles_to_process += len(read_data(dataset_path))

    result_points = []
    profiles_processed = 0

    files = os.listdir(path_to_profiles)

    random.shuffle(files)
    
    for file in files:
        if file.endswith(".pkl"):
            dataset_path = os.path.join(path_to_profiles, file)
            profiles = read_data(dataset_path)
            for i, profile in enumerate(profiles):
                profiles_processed += 1
                if profiles_processed % 100 == 0:
                    logging.info(f"Calculations completion [{(profiles_processed)/profiles_to_process:.2%}]")
                    save_data(path_to_results, result_points)   

                ranking = rule(profile)
                candidates = len(profile.candidates)
                n_voters = len(profile.ballots)

                for voters_group in get_cohesive_voter_groups(profile):
                    viters_group_size = len(voters_group)
                    ballot_group = [profile.ballots[voter_num] for voter_num in voters_group]
                    for k in range(1,candidates+1):
                        avg_d_b_jd = avg_devided_by_jd(ballot_group, ranking[:k], k, n_voters)
                        if avg_d_b_jd is not None and avg_d_b_jd < 1:
                            result_points.append({ "a": viters_group_size / n_voters, "y_r": avg_d_b_jd })

    save_data(path_to_results, result_points)
    logging.info(f"Completed calculations for {file}")

    # results = []
    # for i, m in enumerate(candidates):
    #     inner_candidates = [str(k) for k in range(m)]
    #     for j, fi in enumerate(range(n_voters)):
    #         manipulability_ratio = get_manipulability_ratio(inner_candidates, n_voters, gen, ("f", fi), n_iterations, n_jobs=n_jobs)
    #         results.append({
    #             'm': m,
    #             'orness': orness(n_voters, fi),
    #             'manipulability': manipulability_ratio
    #         })
    #         logging.info(f"Calculations completion [{(i*n_voters+j+1)/(len(candidates)*n_voters):.2%}]")
    #     logging.info(f"Completed calculations for {m} candidates")
    # save_data(path.with_suffix(".csv"), results)





# def experiment_1_one_rule(path, configs: list[ProfileGeneratingConfig], *, n_jobs=1, verbose=True):
#     log_level = logging.INFO if verbose else logging.WARNING
#     logging.basicConfig(level=log_level, format='%(message)s')

#     profiles_to_generate = [config.n_iterations for config in configs]

#     result_points = []

#     while sum(profiles_to_generate) > 0:
#         for i, config in enumerate(configs):
#             iterations = min(profiles_to_generate[i], 100)
#             profiles_to_generate[i] -= iterations
#             for j in range(iterations):
#                 candidates = [str(num) for num in range(random.randint(*config.n_candidates_interval))]
#                 n_voters = random.randint(*config.n_voters_interval)
#                 profile = config.profile_generator(candidates, n_voters)
#                 ranking = AV(profile)

#                 for voters_group in get_cohesive_voter_groups(profile):
#                     viters_group_size = len(voters_group)
#                     ballot_group = [profile.ballots[voter_num] for voter_num in voters_group]
#                     for k in range(1,len(candidates)+1):
#                         avg_d_b_jd = avg_devided_by_jd(ballot_group, ranking[:k], k, n_voters)
#                         if avg_d_b_jd is not None and avg_d_b_jd < 1:
#                            result_points.append((viters_group_size / n_voters, avg_d_b_jd))

#         dump_data(result_points,"result_points.pkl")

#     dump_data(result_points,"result_points.pkl")
#     return result_points