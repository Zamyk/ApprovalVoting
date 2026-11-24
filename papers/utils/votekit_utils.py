from votekit.pref_profile.approval_profile import ApprovalProfile


def sample_approval_profile(profile, n_voters, rng):
  """Draw n_voters ballots without replacement from an ApprovalProfile."""
  n = profile.num_ballots
  if n < n_voters:
    raise ValueError(f"Need at least {n_voters} voters, got {n}")
  idx = rng.choice(n, size=n_voters, replace=False)
  ballots = tuple(profile.ballots[int(i)] for i in idx)
  return ApprovalProfile(ballots=ballots, candidates=profile.candidates)
