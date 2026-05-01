from votekit.ballot import Ballot
from votekit.ballot import ApprovalBallot

from votekit.pref_profile.approval_profile import ApprovalProfile

from votekit.elections.election_types.approval.hamming import OrderedWeightedHamming

ballot = Ballot(approvals=["A", "B", "C"], weight=3 / 2)
print(ballot)

candidates = {"A", "B", "C", "D"}
ballots = [
  Ballot(approvals=["A", "B"]),
  Ballot(approvals=["A", "B"]),
  Ballot(approvals=["A", "D"]),
  Ballot(approvals=["A", "B", "C", "D"])
]

profile = ApprovalProfile(ballots=ballots, candidates=candidates)
print(profile)

election = OrderedWeightedHamming(profile=profile)
print(election)