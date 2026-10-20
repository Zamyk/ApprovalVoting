import numpy as np


def approval_matrix(voters, candidates, d):
  return (np.abs(voters[:, None] - candidates[None, :]) <= d).astype(np.int8)


def generate_profile_triangular(n_voters, n_candidates, d):
  rng = np.random.default_rng()
  voters = rng.triangular(-1, 0, 1, n_voters)
  candidates = np.linspace(-1, 1, n_candidates)
  return approval_matrix(voters, candidates, d), candidates


def generate_profile_gaussian(n_voters, n_candidates, d):
  rng = np.random.default_rng()
  voters = rng.normal(0, 0.5, n_voters)
  candidates = rng.uniform(-1, 1, n_candidates)
  return approval_matrix(voters, candidates, d), candidates
