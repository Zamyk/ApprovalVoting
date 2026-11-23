from concurrent.futures import ProcessPoolExecutor
import os
import numpy as np
import pandas as pd

from approval_with_runoff import alpha_seqAV, approval_counts, pair_lines, seq_components
from generators import approval_profiles


DS = [0.1, 0.25, 0.33, 0.5]
N_VOTERS = 20000
N_CANDIDATES = 1000
N_CANDIDATES_2D = 10000
N_ALPHAS = 50
N_REPS = 50


def point_distance(a, b):
  return float(np.linalg.norm(np.asarray(a, dtype=float) - np.asarray(b, dtype=float)))


def _distances_for_profile(candidates, alphas, counts, with_winner):
  """Distance between the two alpha-seqAV finalists for each alpha."""
  distances = np.empty(len(alphas))
  for i, alpha in enumerate(alphas):
    winner, second = alpha_seqAV(counts, with_winner, alpha)
    distances[i] = point_distance(candidates[second], candidates[winner])
  return distances


def _seq_distances(profile, candidates, alphas):
  """Distance between the seqAV finalists for each alpha. The first finalist is the AV
  winner, so this is also the distance of the second finalist from the AV winner."""
  _, counts, with_winner = seq_components(profile)
  return (_distances_for_profile(candidates, alphas, counts, with_winner),)


def run_sample(generator, ds=DS, n_voters=N_VOTERS, n_candidates=N_CANDIDATES, n_alphas=N_ALPHAS):
  """One set of positions, thresholded at every ``d``."""
  alphas = np.linspace(0, 1, n_alphas)
  candidates, voters = generator(n_voters, n_candidates)
  rows = []
  for d, profile in zip(ds, approval_profiles(voters, candidates, ds)):
    (distances,) = _seq_distances(profile, candidates, alphas)
    for alpha, value in zip(alphas, distances):
      rows.append({"d": d, "alpha": float(alpha), "distance": float(value)})
  return pd.DataFrame(rows)


def _pair_positions(candidates, counts, rows, cols, intercept, overlap, alphas, reference):
  """For each alpha, distance of the first and the second alpha-AV finalist from ``reference``.

  The first finalist is the one with more approvals (ties: the one closer to ``reference``).
  """
  first = np.empty(len(alphas))
  second = np.empty(len(alphas))
  for i, alpha in enumerate(alphas):
    best = int(np.argmax(intercept - alpha * overlap))
    a = int(rows[best])
    b = int(cols[best])
    da = point_distance(candidates[a], reference)
    db = point_distance(candidates[b], reference)
    if counts[b] > counts[a] or (counts[b] == counts[a] and db < da):
      da, db = db, da
    first[i] = da
    second[i] = db
  return first, second


def _av_distances(profile, candidates, alphas):
  """Distances of the first and second alpha-AV finalist from the AV winner for each alpha."""
  counts = approval_counts(profile)
  av_winner = candidates[int(np.argmax(counts))]
  rows, cols, intercept, overlap = pair_lines(profile, counts)
  return _pair_positions(candidates, counts, rows, cols, intercept, overlap, alphas, av_winner)


def _repetition(args):
  """One repetition: draw positions once, evaluate ``measure`` on the profile for every ``d``."""
  measure, generator, ds, n_voters, n_candidates, alphas = args
  candidates, voters = generator(n_voters, n_candidates)
  return [measure(profile, candidates, alphas)
          for profile in approval_profiles(voters, candidates, ds)]


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


def _run_repeated(measure, n_outputs, generator, n_reps, ds, n_voters, n_candidates, n_alphas, n_jobs):
  """Run ``measure`` on ``n_reps`` position draws (each shared by all ``d``).

  Returns one min/max/mean frame per output of ``measure``.
  """
  alphas = np.linspace(0, 1, n_alphas)
  if n_jobs is None or n_jobs == -1:
    n_jobs = os.cpu_count() or 1
  tasks = [(measure, generator, ds, n_voters, n_candidates, alphas) for _ in range(n_reps)]
  collected = [[[] for _ in ds] for _ in range(n_outputs)]
  if n_jobs == 1:
    finished = (_repetition(task) for task in tasks)
  else:
    pool = ProcessPoolExecutor(max_workers=n_jobs)
    finished = pool.map(_repetition, tasks)
  try:
    for done, per_d in enumerate(finished, 1):
      for d_index, outputs in enumerate(per_d):
        for k, values in enumerate(outputs):
          collected[k][d_index].append(values)
      print(f"Finished repetition {done}/{len(tasks)}", flush=True)
  finally:
    if n_jobs != 1:
      pool.shutdown()
  return [_aggregate(c, ds, alphas) for c in collected]


def run_iterations(generator, n_reps=N_REPS, ds=DS, n_voters=N_VOTERS, n_candidates=N_CANDIDATES, n_alphas=N_ALPHAS, n_jobs=None):
  """Distance between the seqAV finalists."""
  (second,) = _run_repeated(_seq_distances, 1, generator, n_reps, ds, n_voters, n_candidates, n_alphas, n_jobs)
  return second


def run_av_iterations(generator, n_reps=N_REPS, ds=DS, n_voters=N_VOTERS, n_candidates=N_CANDIDATES, n_alphas=N_ALPHAS, n_jobs=None):
  """Distances of the first and second alpha-AV finalist from the AV winner."""
  winner, second = _run_repeated(_av_distances, 2, generator, n_reps, ds, n_voters, n_candidates, n_alphas, n_jobs)
  return winner, second
