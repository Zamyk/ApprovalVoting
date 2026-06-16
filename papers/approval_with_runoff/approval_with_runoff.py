from pathlib import Path
import numpy as np
import pandas as pd
import logging


def alpha_seqAV(votes, committee, alpha):
  winner = 0
  winner_score = -1

  counts = [0] * len(committee)
  for vote in votes:
    for candidate in vote:
      counts[candidate] += 1

  for candidate in range(len(committee)):
    if counts[candidate] > winner_score:
      winner = candidate
      winner_score = counts[candidate]

  with_winner = [0] * len(committee)
  for vote in votes:
    if winner in vote:
      for candidate in vote:
        if candidate != winner:
          with_winner[candidate] += 1

  second = 0
  second_score = -float('inf')
  for i in range(len(committee)):
    score = -alpha * with_winner[i] + counts[i]
    eps = 1e-9
    if i != winner and (score > second_score - eps) or ( abs(score - second_score) <= eps and abs(committee[i]) > abs(committee[second])):# so we can use different things there idk what is correct
      second = i
      second_score = score

  return winner, second

def alpha_AV(votes, candidates, alpha):
  pass


def generate_profile_triangular(n_voters, n_candidates, d):
  rng = np.random.default_rng()
  voters = rng.triangular(-1, 0, 1, n_voters)
  candidates = np.linspace(-1, 1, n_candidates)

  votes = [{i for i in range(n_candidates) if abs(candidates[i] - voter) <= d} for voter in voters]
  return votes, candidates

def generate_profile_gaussian(n_voters, n_candidates, d):
  rng = np.random.default_rng()
  voters = rng.normal(0, 0.5, n_voters)
  #candidates = np.linspace(-1, 1, n_candidates)
  candidates = np.random.uniform(-1, 1, n_candidates)

  votes = [{i for i in range(n_candidates) if abs(candidates[i] - voter) <= d} for voter in voters]
  return votes, candidates


def t1(path, verbose = True):
  ds = [0.1, 0.25, 0.33, 0.5]
  n_voters = 20000
  n_candidates = 1000

  log_level = logging.INFO if verbose else logging.WARNING
  logging.basicConfig(level=log_level, format='%(message)s')

  results = []

  for d in ds:
    logging.info(f"Calculations for [d={d}")
    votes, candidates = generate_profile_gaussian(n_voters, n_candidates, d)
    for alpha in np.linspace(0, 1, 50):
      second = abs(candidates[alpha_seqAV(votes, candidates, alpha)[1]])
      results.append({
          'd': d,
          'alpha' : alpha,
          'winner': second
      })
      logging.info(f"Done for [alpha={alpha}")
    logging.info(f"Calculations completion [d={d}")

  df = pd.DataFrame(results)
  df.to_csv(path.with_suffix(".csv"), index=False)


def from_csv():
  pass

for i in range(50):
  t1(Path(__file__).resolve().parent / f"results{i}")