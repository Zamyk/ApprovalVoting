from votekit.ballot import Ballot
from votekit.pref_profile.approval_profile import ApprovalProfile
from votekit.elections.election_types.approval.hamming import OrderedWeightedHamming

jan_ballot = Ballot(approvals={"praca1"})
mateusz_ballot = Ballot(approvals={"praca1", "praca2"})
piotr_ballot = Ballot(approvals={"praca3"})

profile = ApprovalProfile(ballots=[jan_ballot, mateusz_ballot, piotr_ballot])

election = OrderedWeightedHamming(profile=profile)
print(set(election.get_elected()[0]))