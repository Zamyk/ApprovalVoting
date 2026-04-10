import pandas as pd
import itertools

from typing import Optional
from typing import Sequence

from votekit.elections import Election
from votekit.elections import ElectionState

from profile import ApprovalProfile

class GeneralApproval(Election[ApprovalProfile]):

    def __init__(self, profile: ApprovalProfile):
        super().__init__(profile=profile)


def ow_hamming_hamming_score(profile: ApprovalProfile, weights: Sequence[float], committee: set[str]) -> float:
    scores = profile.df.drop(columns=['Weight', 'Voter Set']).fillna(0)

    committee_vector = pd.Series(
        [1.0 if c in committee else 0.0 for c in scores.columns],
        index=scores.columns
    )        

    distances = (scores != committee_vector).sum(axis=1)
    distances = sorted(distances, reverse=True)

    result = 0
    for i in range(len(distances)):
        result += distances[i] * weights[i]

    return result

def ow_hamming_get_elected(profile: ApprovalProfile, weights: Sequence[float]) -> set[str]:
    candidates = profile.candidates
    best_score = float('inf')
    best_committee = None

    for k in range(len(candidates)):
        for committee in itertools.combinations(candidates, k):
            score = ow_hamming_hamming_score(profile=profile, weights=weights, committee=committee)
            if score < best_score:
                best_score = score
                best_committee = committee

    return best_committee

class OrderedWeightedHamming(GeneralApproval):

    def __init__(
        self, profile: ApprovalProfile, tiebreak: Optional[str] = None, weights: Sequence[float] = None
    ):
        print(profile.df)

        self.weights = weights
        if self.weights == None:
            self.weights = [1.0] * len(profile.df)

        super().__init__(profile=profile)

    def _is_finished(self):
        # single round election
        if len(self.election_states) == 2:
            return True
        return False

    def _run_step(
        self, profile: ApprovalProfile, prev_state: ElectionState, store_states=False
    ) -> ApprovalProfile:

        elected = ow_hamming_get_elected(profile, self.weights)

        if store_states:
            new_state = ElectionState(
                round_number=1,  # single shot election
                elected=tuple(frozenset(elected)),
            )

            self.election_states.append(new_state)

        return profile