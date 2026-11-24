import numpy as np
from scipy.spatial.distance import cdist


def _points(x):
  """cdist wants shape (n_points, dim). A 1D list of positions becomes (n, 1)."""
  x = np.asarray(x, dtype=float)
  if x.ndim == 1:
    return x.reshape(len(x), 1)
  return x


def approval_matrix(voters, candidates, d):
  return (cdist(voters, candidates) <= d).astype(np.int8)


def generate_profile_triangular(n_voters, n_candidates, d):
  rng = np.random.default_rng()
  voters = _points(rng.triangular(-1, 0, 1, n_voters))
  candidates = _points(np.linspace(-1, 1, n_candidates))
  return approval_matrix(voters, candidates, d), candidates, voters


def generate_profile_gaussian(n_voters, n_candidates, d):
  rng = np.random.default_rng()
  voters = _points(rng.normal(0, 0.5, n_voters))
  candidates = _points(rng.uniform(-1, 1, n_candidates))
  return approval_matrix(voters, candidates, d), candidates, voters


def generate_profile_triangular_2d(n_voters, n_candidates, d):
  rng = np.random.default_rng()
  voters = np.column_stack((
    rng.triangular(-1, 0, 1, n_voters),
    rng.triangular(-1, 0, 1, n_voters),
  ))
  candidates = rng.uniform(-1, 1, (n_candidates, 2))
  return approval_matrix(voters, candidates, d), candidates, voters


def generate_profile_cone_2d(n_voters, n_candidates, d):
  rng = np.random.default_rng()
  radius = np.sqrt(2.0)
  voters = np.empty((n_voters, 2))
  filled = 0
  while filled < n_voters:
    need = n_voters - filled
    props = rng.uniform(-1, 1, (need * 4, 2))
    dens = 1.0 - np.linalg.norm(props, axis=1) / radius
    keep = props[rng.random(len(props)) < dens]
    take = min(len(keep), need)
    voters[filled:filled + take] = keep[:take]
    filled += take
  candidates = rng.uniform(-1, 1, (n_candidates, 2))
  return approval_matrix(voters, candidates, d), candidates, voters


def generate_profile_gaussian_2d(n_voters, n_candidates, d):
  rng = np.random.default_rng()
  voters = rng.normal(0, 0.5, (n_voters, 2))
  candidates = rng.uniform(-1, 1, (n_candidates, 2))
  return approval_matrix(voters, candidates, d), candidates, voters
