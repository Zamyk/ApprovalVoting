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
from fractions import Fraction

from votekit.elections.election_types.approval.proportional_rankings import avg_devided_by_jd
from votekit.pref_profile.approval_profile import ApprovalProfile, ApprovalBallot



def dump_data(data: Any, path: str) -> None:
    with open(path, "wb") as file:
        pickle.dump(data, file, protocol=pickle.HIGHEST_PROTOCOL)

def read_data(path: str) -> Any:
    with open(path, "rb") as file:
        return pickle.load(file)


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


def Seq_Thile(profile: ApprovalProfile, w: list[float | int] | str = "SeqPav"):
    if type(w) == str:
        if w == "SeqPav":
            w = [1/(i+1) for i in range(len(profile.candidates))]
        elif w == "AV":
            w = [1.0] * len(profile.candidates)
        elif w == "GreedyCC":
            w = [1.0] + [0.0] * (len(profile.candidates) - 1)
        elif w.endswith("-Geometric"):
            prefix = w[:-10]
            frac = Fraction(prefix)
            if frac.denominator == 1:
                p = int(frac)    
            else:
                p = float(frac)

            if p <= 1:
                raise ValueError(f"Geometric weight parameter p must be greater than 1, got {p}")
                
            w = [1 / p**(i+1) for i in range(len(profile.candidates))]
        else:
            raise ValueError(f"Unknown weight type: {w}")
    if w is None:
        raise ValueError("Weight vector w cannot be None")
    else:
        w = w

    w_acc = [0] + w.copy()
    for i in range(1, len(w_acc)):
        w_acc[i] += w_acc[i-1]

    approval_sets = [set(ballot.approvals) for ballot in profile.ballots if ballot.approvals]

    elected_candidates = []
    not_elected_candidates = list(profile.candidates)
    current_ranking = []
    for _ in range(len(profile.candidates)):
        max_score = float('-inf')
        best_candidate = None
        for c in not_elected_candidates:
            current_ranking.append(c)
            current_ranking_set = set(current_ranking)
            w_score = 0
            for approval_set in approval_sets:
                n = len(approval_set & current_ranking_set)
                w_score += w_acc[n]

            if w_score > max_score:
                max_score = w_score
                best_candidate = c

            current_ranking.pop(-1)

        elected_candidates.append(best_candidate)
        current_ranking.append(best_candidate)
        not_elected_candidates.remove(best_candidate)
            

    return elected_candidates



def Reverse_Seq_PAV(profile: ApprovalProfile):
    w = [1/(i+1) for i in range(len(profile.candidates))]

    w_acc = [0] + w.copy()
    for i in range(1, len(w_acc)):
        w_acc[i] += w_acc[i-1]

    approval_sets = [set(ballot.approvals) for ballot in profile.ballots if ballot.approvals]

    elected_candidates_reversed = []
    not_elected_candidates = list(profile.candidates)
    current_ranking_set = set(profile.candidates)
    for _ in range(len(profile.candidates)):
        min_score = float('inf')
        best_candidate = None
        for c in not_elected_candidates:
            current_ranking_set.remove(c)
            w_score = 0
            for approval_set in approval_sets:
                n = len(approval_set & current_ranking_set)
                w_score -= w_acc[n]

            if w_score < min_score:
                min_score = w_score
                best_candidate = c

            current_ranking_set.add(c)

        elected_candidates_reversed.append(best_candidate)
        current_ranking_set.remove(best_candidate)
        not_elected_candidates.remove(best_candidate)

    elected_candidates_reversed.reverse()

    return elected_candidates_reversed


# profile = ApprovalProfile(candidates=["A", "B", "C", "D"], ballots=[
#     ApprovalBallot(approvals=["A", "B", "C", "D"]), 
#     ApprovalBallot(approvals=["B", "D"]), 
#     ApprovalBallot(approvals=["A", "B", "C", "D"]),
#     ApprovalBallot(approvals=["A", "B"])])

# print(Reverse_Seq_PAV(profile))

def Phragmen(profile: ApprovalProfile):
    candidate_approval_voters_sets = {c: set() for c in profile.candidates}
    for i, ballot in enumerate(profile.ballots):
        for candidate in ballot.approvals:
            candidate_approval_voters_sets[candidate].add(i)

    not_elected_candidates = list(profile.candidates)

    voters_loads = {i: 0 for i in range(len(profile.ballots))}

    ranking = []

    for _ in range(len(profile.candidates)):
        max_load = float('inf')
        best_candidate = None
        best_candidate_loads = None
        for c in not_elected_candidates:
            n = len(candidate_approval_voters_sets[c])
            if n == 0:
                new_load = None
            else:
                approving_voters_loads=sorted([voters_loads[i] for i in candidate_approval_voters_sets[c]])
                approving_voters_loads.append(float('inf'))
                summed_load = 1
                new_load = None
                for j in range(n):
                    summed_load += approving_voters_loads[j]
                    if summed_load / (j + 1) < approving_voters_loads[j+1]:
                        new_load = summed_load / (j + 1)
                        break

            voters_loads_copy = voters_loads.copy()
            for voter in candidate_approval_voters_sets[c]:
                voters_loads_copy[voter] = max(voters_loads_copy[voter], new_load)

            if new_load is not None and new_load < max_load:
                max_load = new_load
                best_candidate = c
                best_candidate_loads = voters_loads_copy

        if best_candidate is None:
            best_candidate = not_elected_candidates[0]
            best_candidate_loads = voters_loads.copy()

        ranking.append(best_candidate)
        voters_loads = best_candidate_loads
        print(voters_loads)
        not_elected_candidates.remove(best_candidate)

    return ranking



def Best_of(profile: ApprovalProfile, rule_args: list[tuple[Callable[[ApprovalProfile], list[str]], dict]]):
    best_ranking = None
    best_score = -float('inf')

    for rule, args in rule_args:
        ranking = rule(profile, **args)
        rule_score = float('inf')
        for voters_group in get_cohesive_voter_groups(profile):
            ballot_group = [profile.ballots[voter_num] for voter_num in voters_group]
            for k in range(1, len(profile.candidates) + 1):
                avg_d_b_jd = avg_devided_by_jd(ballot_group, ranking[:k], k, len(profile.ballots))
                if avg_d_b_jd is not None:
                    rule_score = min(rule_score, avg_d_b_jd)

        if rule_score > best_score:
            best_score = rule_score
            best_ranking = ranking

    return best_ranking



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
        




import os
import random
import logging
import pandas as pd
from concurrent.futures import ProcessPoolExecutor, as_completed

def process_single_file(args):
    """Pomocnicza funkcja wykonująca obliczenia dla pojedynczego pliku `.pkl` w osobnym procesie."""
    file, path_to_profiles, rule, rule_args, n_profiles_per_file = args
    dataset_path = os.path.join(path_to_profiles, file)
    profiles = read_data(dataset_path)

    if n_profiles_per_file >= 1:
        n_profiles_per_file = min(n_profiles_per_file, len(profiles))  
    elif n_profiles_per_file == -1:
        n_profiles_per_file = len(profiles)
    elif n_profiles_per_file < -1:
        n_profiles_per_file = -int(len(profiles) / n_profiles_per_file)
    
    local_result_points = []
    for profile in profiles[:n_profiles_per_file]:
        ranking = rule(profile, **rule_args)
        candidates = len(profile.candidates)
        n_voters = len(profile.ballots)

        for voters_group in get_cohesive_voter_groups(profile):
            voters_group_size = len(voters_group)
            ballot_group = [profile.ballots[voter_num] for voter_num in voters_group]
            for k in range(1, candidates + 1):
                avg_d_b_jd = avg_devided_by_jd(ballot_group, ranking[:k], k, n_voters)
                if avg_d_b_jd is not None and avg_d_b_jd < 1:
                    local_result_points.append({
                        "file": file,
                        "a": voters_group_size / n_voters, 
                        "y_r": avg_d_b_jd,
                        "k": k,
                        "rule": rule.__name__,
                        "candidates": candidates,
                        "n_voters": n_voters
                    })
                    
    return file, local_result_points




def experiment_1_one_rule(path_to_profiles, path_to_results, rule, *, rule_args={}, n_profiles_per_file=-1, n_jobs=1, verbose=True):
    log_level = logging.INFO if verbose else logging.WARNING
    logging.basicConfig(level=log_level, format='%(message)s')

    if n_jobs == 1:
        pass  
    elif n_jobs == -1:
        n_jobs = os.cpu_count()
    elif n_jobs < -1:
        n_jobs = -int(os.cpu_count() / n_jobs)

    profiles_to_process = 0
    for file in os.listdir(path_to_profiles):
        if file.endswith(".pkl"):
            dataset_path = os.path.join(path_to_profiles, file)
            profiles_to_process += len(read_data(dataset_path))

    file_path = path_to_results.with_name(f"{path_to_results.stem}_files_processed.csv")
    if file_path.exists():
        files_processed_list = pd.read_csv(file_path).to_dict('records')
    else:
        files_processed_list = []

    if path_to_results.exists():
        try:
            result_points = pd.read_csv(path_to_results).to_dict('records')
        except Exception:
            result_points = []
    else:
        result_points = []

    processed_files_set = {item["file"] for item in files_processed_list}
    files = [f for f in os.listdir(path_to_profiles) if f.endswith(".pkl") and f not in processed_files_set]

    profiles_processed = sum(len(read_data(os.path.join(path_to_profiles, item["file"]))) for item in files_processed_list if os.path.exists(os.path.join(path_to_profiles, item["file"])))

    with ProcessPoolExecutor(max_workers=n_jobs) as executor:
        future_to_file = {
            executor.submit(process_single_file, (file, path_to_profiles, rule, rule_args, n_profiles_per_file)): file 
            for file in files
        }

        for future in as_completed(future_to_file):
            file = future_to_file[future]
            try:
                completed_file, local_points = future.result()
                
                result_points.extend(local_points)
                files_processed_list.append({"file": completed_file})
                
                dataset_path = os.path.join(path_to_profiles, completed_file)
                profiles_processed += len(read_data(dataset_path))

                if profiles_to_process > 0:
                    progress_pct = profiles_processed / profiles_to_process
                    logging.info(f"Calculations completion [{progress_pct:.2%}] (Completed {completed_file})")
                
                # save_data(file_path, files_processed_list)
                # save_data(path_to_results, result_points)

            except Exception as exc:
                logging.error(f"File {file} generated an exception: {exc}")

    save_data(path_to_results, result_points)
    logging.info(f"Completed calculations for all files -> {path_to_results}")


# def experiment_1_one_rule(path_to_profiles, path_to_results, rule, *, n_jobs=1, verbose=True):
#     log_level = logging.INFO if verbose else logging.WARNING
#     logging.basicConfig(level=log_level, format='%(message)s')

#     profiles_to_process = 0
#     for file in os.listdir(path_to_profiles):
#         if file.endswith(".pkl"):
#             dataset_path = os.path.join(path_to_profiles, file)
#             profiles_to_process += len(read_data(dataset_path))

#     result_points = []
#     profiles_processed = 0
#     file_path = path_to_results.with_name(f"{path_to_results.stem}_files_processed.csv")
#     if file_path.exists():
#         files_processed_list = pd.read_csv(file_path).to_dict('records')
#     else:
#         files_processed_list = []

#     files = os.listdir(path_to_profiles)

#     files = list(set(files) - set([item["file"] for item in files_processed_list]))

#     random.shuffle(files)
    
#     for f, file in enumerate(files):
#         if file.endswith(".pkl"):
#             dataset_path = os.path.join(path_to_profiles, file)
#             profiles = read_data(dataset_path)
#             files_processed_list.append({ "file": file})
#             for i, profile in enumerate(profiles):
#                 profiles_processed += 1
#                 if profiles_processed % 100 == 0:
#                     logging.info(f"Calculations completion [{(profiles_processed)/profiles_to_process:.2%}]")
#                     save_data(file_path, files_processed_list) 
#                     save_data(path_to_results, result_points)   

#                 ranking = rule(profile)
#                 candidates = len(profile.candidates)
#                 n_voters = len(profile.ballots)

#                 for voters_group in get_cohesive_voter_groups(profile):
#                     viters_group_size = len(voters_group)
#                     ballot_group = [profile.ballots[voter_num] for voter_num in voters_group]
#                     for k in range(1,candidates+1):
#                         avg_d_b_jd = avg_devided_by_jd(ballot_group, ranking[:k], k, n_voters)
#                         if avg_d_b_jd is not None and avg_d_b_jd < 1:
#                             result_points.append({ "a": viters_group_size / n_voters, "y_r": avg_d_b_jd })

#     save_data(path_to_results, result_points)
#     logging.info(f"Completed calculations for {file}")














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





# print(Seq_Thile(ApprovalProfile(candidates=["A", "B", "C"], ballots=[ApprovalBallot(approvals=["A", "B"]), ApprovalBallot(approvals=["B", "C"]), ApprovalBallot(approvals=["A", "C"])]), w="5/4-Geometric"))