import votekit.elections.election_types.approval.hamming as approval_module
from papers.manipulation_of_hamming.manipulation_of_hamming import _get_weights_on_int
approval_module._get_weights = _get_weights_on_int
from votekit.elections.election_types.approval.hamming import OrderedWeightedHamming
import numpy as np
import random
from votekit.ballot import ApprovalBallot
from votekit.pref_profile.approval_profile import ApprovalProfile
from votekit.elections.election_types.approval.hamming import OrderedWeightedHamming
from votekit.ballot_generator.std_generator.approval_impartial_culture import approval_ic_profile_generator, approval_biased_profile_generator
from votekit.comsoc.approval_manipulations import for_all_manipulations


def orness(n, fi):
    return (n + fi - 1) / (2 * (n - 1))


def get_elected_committee(profile, weights_type="minisum"):
    election = OrderedWeightedHamming(profile=profile, weights=weights_type)
    elected_tuple = election.get_elected()
    if not elected_tuple:
        return np.array([0 for c in profile.candidates])

    return np.array([c in elected_tuple[0] for c in profile.candidates])


def get_hamming_dist(ballot_vec, committee):
    return np.sum(ballot_vec != committee)


def can_voter_manipulate(voter_idx, profile, weights_type="minimax"):
    preference = profile.votes[voter_idx].copy()

    true_elected = get_elected_committee(profile, weights_type)
    true_dist = get_hamming_dist(preference, true_elected)

    is_manipulable = False

    def check_manipulation(manipulated_profile):
        nonlocal is_manipulable
        manipulated_elected = get_elected_committee(manipulated_profile, weights_type)
        dist = get_hamming_dist(preference, manipulated_elected)
        if dist < true_dist:
            #print("---",manipulated_profile.ballots)
            is_manipulable = True
            return False
        return True

    for_all_manipulations(profile, voter_idx, check_manipulation)
    return is_manipulable





candidates = ["A", "B", "C"]
n_voters = 6

ballots = [
    ApprovalBallot(approvals=["A", "B"]),
    ApprovalBallot(approvals=["B"]),
    ApprovalBallot(approvals=["A", "B"]),
    ApprovalBallot(approvals=["A", "B", "C"]),
    ApprovalBallot(approvals=["A", "B", "C"]),
    ApprovalBallot(approvals=["C"])
        ]

profile = ApprovalProfile(ballots=tuple(ballots), candidates=candidates)

print(get_elected_committee(profile=profile, weights_type="minimax"))
print(get_elected_committee(profile=profile, weights_type="minisum"))
# print(get_elected_committee(profile=profile, weights_type="minimax"))

# for i in range(n_voters):
#     if can_voter_manipulate(i, profile, "minimax"):
#         print(i, 1)


# ballots = [
#     ApprovalBallot(approvals=["A", "B"]),
#     ApprovalBallot(approvals=[]),
#     ApprovalBallot(approvals=["A", "B"]),
#     ApprovalBallot(approvals=["A", "B", "C"]),
#     ApprovalBallot(approvals=["A", "B", "C"]),
#     ApprovalBallot(approvals=["C"])
#         ]
# profile = ApprovalProfile(ballots=tuple(ballots), candidates=candidates)

# print(get_elected_committee(profile=profile, weights_type="minimax"))