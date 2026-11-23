"""Euclidean approval profiles: voters and candidates are points, a voter approves every
candidate within distance ``d``.

A point distribution is a function ``(rng, n) -> array of shape (n, dim)``. A position
generator is ``(n_voters, n_candidates) -> (candidates, voters)``; build one with
``position_generator(voter_dist, candidate_dist)``. It is a ``functools.partial`` of a
module-level function, so it pickles into ``ProcessPoolExecutor`` workers. The same positions
are then turned into one profile per ``d`` with ``approval_profiles``.
"""

from functools import partial

import numpy as np
from scipy.spatial.distance import cdist


def approval_profiles(voters, candidates, ds):
  """Yield one approval profile per threshold in ``ds``, all from the same positions.

  The distance matrix is computed once; profiles are built one at a time to bound memory.
  """
  distances = cdist(voters, candidates)
  for d in ds:
    yield (distances <= d).astype(np.int8)


# ---- point distributions ---------------------------------------------------------------

def triangular_1d(rng, n):
  return rng.triangular(-1, 0, 1, (n, 1))


def gaussian_1d(rng, n):
  return rng.normal(0, 0.5, (n, 1))


def triangular_2d(rng, n):
  """Independent triangular(-1, 0, 1) on each axis."""
  return rng.triangular(-1, 0, 1, (n, 2))


def cone_2d(rng, n):
  """Radial cone on [-1, 1]^2: density proportional to 1 - |x| / sqrt(2) (rejection sampling)."""
  radius = np.sqrt(2.0)
  points = np.empty((n, 2))
  filled = 0
  while filled < n:
    need = n - filled
    props = rng.uniform(-1, 1, (need * 4, 2))
    dens = 1.0 - np.linalg.norm(props, axis=1) / radius
    keep = props[rng.random(len(props)) < dens]
    take = min(len(keep), need)
    points[filled:filled + take] = keep[:take]
    filled += take
  return points


def gaussian_2d(rng, n):
  return rng.normal(0, 0.5, (n, 2))


def uniform_2d(rng, n):
  return rng.uniform(-1, 1, (n, 2))


# ---- position generators ---------------------------------------------------------------

def _positions(voter_dist, candidate_dist, n_voters, n_candidates):
  rng = np.random.default_rng()
  voters = voter_dist(rng, n_voters)
  candidates = candidate_dist(rng, n_candidates)
  return candidates, voters


def position_generator(voter_dist, candidate_dist=None):
  """Candidates follow ``candidate_dist``, or the voters' distribution when it is omitted."""
  return partial(_positions, voter_dist, candidate_dist or voter_dist)
