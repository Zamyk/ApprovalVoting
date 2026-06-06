import numpy as np

from abcvoting.preferences import Profile
from abcvoting import abcrules

def Sv(votes, committee):
  pass

def alpha_seqAV(votes, committee, alpha):
  pass

# returns pair of indices of winning voters
def get_result(votes, candidates, rule):  
  profile = Profile(num_cand=len(candidates))
  profile.add_voters(votes)
  return abcrules.compute(rule, profile, committeesize=2, resolute=True)

def generate_profile_triangular(n_voters, n_candidates, d):
  rng = np.random.default_rng()
  voters = rng.triangular(-1, 0, 1, n_voters)
  candidates = rng.triangular(-1, 0, 1, n_candidates)

  votes = [{i for i in range(n_candidates) if abs(candidates[i] - voter) <= d} for voter in voters]
  return votes, candidates



def t1():
  ds = [0.1, 0.25, 0.33, 0.5]
  n_voters = 20000
  n_candidates = 1000
  for d in ds:
    votes, candidates = generate_profile_triangular(n_voters, n_candidates, d)
    result = get_result(votes, candidates, "")





# returns profile and distance to center of each voter
def generate_profile_gaussian(n_voters, n_candidates, d):
  pass