from votekit.ballot import Ballot
from votekit.ballot import ApprovalBallot

ballot = Ballot(approvals=["A", "B", "C"], weight=3 / 2)
print(ballot)