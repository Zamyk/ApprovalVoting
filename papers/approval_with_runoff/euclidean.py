from concurrent.futures import ProcessPoolExecutor
import os
import numpy as np
import pandas as pd

from approval_with_runoff import alpha_seqAV, approval_counts, pair_lines, seq_components
from generators import generate_profile_gaussian, generate_profile_triangular


DS = [0.1, 0.25, 0.33, 0.5]
N_VOTERS = 20000
N_CANDIDATES = 1000
N_ALPHAS = 50
N_REPS = 50


def finalist_distance(candidates, winner, second):
  return abs(float(candidates[second]) - float(candidates[winner]))


def _distances_for_profile(candidates, alphas, counts, with_winner):
  distances = np.empty(len(alphas))
  for i, alpha in enumerate(alphas):
    winner, second = alpha_seqAV(counts, with_winner, alpha)
    distances[i] = finalist_distance(candidates, winner, second)
  return distances


def run_sample(generator, ds=DS, n_voters=N_VOTERS, n_candidates=N_CANDIDATES, n_alphas=N_ALPHAS):
  alphas = np.linspace(0, 1, n_alphas)
  rows = []
  for d in ds:
    profile, candidates = generator(n_voters, n_candidates, d)
    winner, counts, with_winner = seq_components(profile)
    distances = _distances_for_profile(candidates, alphas, counts, with_winner)
    for alpha, value in zip(alphas, distances):
      rows.append({"d": d, "alpha": float(alpha), "distance": float(value)})
  return pd.DataFrame(rows)


def run_triangle(ds=DS, n_voters=N_VOTERS, n_candidates=N_CANDIDATES, n_alphas=N_ALPHAS):
  return run_sample(generate_profile_triangular, ds, n_voters, n_candidates, n_alphas)


def run_gaussian(ds=DS, n_voters=N_VOTERS, n_candidates=N_CANDIDATES, n_alphas=N_ALPHAS):
  return run_sample(generate_profile_gaussian, ds, n_voters, n_candidates, n_alphas)


def _iteration(args):
  generator, d_index, d, n_voters, n_candidates, alphas = args
  profile, candidates = generator(n_voters, n_candidates, d)
  winner, counts, with_winner = seq_components(profile)
  distances = _distances_for_profile(candidates, alphas, counts, with_winner)
  return d_index, distances


def run_iterations(generator, n_reps=N_REPS, ds=DS, n_voters=N_VOTERS, n_candidates=N_CANDIDATES, n_alphas=N_ALPHAS, n_jobs=None):
  alphas = np.linspace(0, 1, n_alphas)
  if n_jobs is None or n_jobs == -1:
    n_jobs = os.cpu_count() or 1
  tasks = [
    (generator, d_index, d, n_voters, n_candidates, alphas)
    for _ in range(n_reps)
    for d_index, d in enumerate(ds)
  ]
  collected = [[] for _ in ds]
  if n_jobs == 1:
    finished = (_iteration(task) for task in tasks)
  else:
    pool = ProcessPoolExecutor(max_workers=n_jobs)
    finished = pool.map(_iteration, tasks)
  try:
    for done, (d_index, distances) in enumerate(finished, 1):
      collected[d_index].append(distances)
      print(f"Finished profile {done}/{len(tasks)}", flush=True)
  finally:
    if n_jobs != 1:
      pool.shutdown()

  rows = []
  for d_index, d in enumerate(ds):
    values = np.vstack(collected[d_index])
    for alpha, low, high, mid in zip(alphas, values.min(axis=0), values.max(axis=0), values.mean(axis=0)):
      rows.append({
        "d": d,
        "alpha": float(alpha),
        "min": float(low),
        "max": float(high),
        "mean": float(mid),
      })
  return pd.DataFrame(rows)


def _pair_positions(candidates, counts, rows, cols, intercept, overlap, alphas):
  winner = np.empty(len(alphas))
  second = np.empty(len(alphas))
  for i, alpha in enumerate(alphas):
    best = int(np.argmax(intercept - alpha * overlap))
    a = int(rows[best])
    b = int(cols[best])
    if counts[b] > counts[a] or (counts[b] == counts[a] and abs(candidates[b]) < abs(candidates[a])):
      a, b = b, a
    winner[i] = abs(float(candidates[a]))
    second[i] = abs(float(candidates[b]))
  return winner, second


def _av_iteration(args):
  generator, d_index, d, n_voters, n_candidates, alphas = args
  profile, candidates = generator(n_voters, n_candidates, d)
  counts = approval_counts(profile)
  rows, cols, intercept, overlap = pair_lines(profile, counts)
  winner, second = _pair_positions(candidates, counts, rows, cols, intercept, overlap, alphas)
  return d_index, winner, second


def _aggregate(collected, ds, alphas):
  rows = []
  for d_index, d in enumerate(ds):
    values = np.vstack(collected[d_index])
    for alpha, low, high, mid in zip(alphas, values.min(axis=0), values.max(axis=0), values.mean(axis=0)):
      rows.append({
        "d": d,
        "alpha": float(alpha),
        "min": float(low),
        "max": float(high),
        "mean": float(mid),
      })
  return pd.DataFrame(rows)


def run_av_iterations(generator, n_reps=N_REPS, ds=DS, n_voters=N_VOTERS, n_candidates=N_CANDIDATES, n_alphas=N_ALPHAS, n_jobs=None):
  alphas = np.linspace(0, 1, n_alphas)
  if n_jobs is None or n_jobs == -1:
    n_jobs = os.cpu_count() or 1
  tasks = [
    (generator, d_index, d, n_voters, n_candidates, alphas)
    for _ in range(n_reps)
    for d_index, d in enumerate(ds)
  ]
  winners = [[] for _ in ds]
  seconds = [[] for _ in ds]
  if n_jobs == 1:
    finished = (_av_iteration(task) for task in tasks)
  else:
    pool = ProcessPoolExecutor(max_workers=n_jobs)
    finished = pool.map(_av_iteration, tasks)
  try:
    for done, (d_index, winner, second) in enumerate(finished, 1):
      winners[d_index].append(winner)
      seconds[d_index].append(second)
      print(f"Finished profile {done}/{len(tasks)}", flush=True)
  finally:
    if n_jobs != 1:
      pool.shutdown()
  return _aggregate(winners, ds, alphas), _aggregate(seconds, ds, alphas)
