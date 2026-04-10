import pandas as pd
import itertools

from typing import Optional
from typing import Sequence

from votekit.elections import Election
from votekit.elections import ElectionState

from profile import ApprovalProfile

class GeneralApproval(Election[ApprovalProfile]):
    pass

class OrderedWeightedHamming(GeneralApproval):

    def __init__(
        self, profile: ApprovalProfile, tiebreak: Optional[str] = None, weights: Sequence[float] = None
    ):
        #super().__init__(profile, m=m, tiebreak=tiebreak)
        self.weights = weights

    def _is_finished(self):
        # single round election
        if len(self.election_states) == 2:
            return True
        return False

    def _run_step(
        self, profile: ApprovalProfile, prev_state: ElectionState, store_states=False
    ) -> ApprovalProfile:
        # TODO!
        pass

    def _hamming_score(profile: ApprovalProfile, weights: Sequence[float], committee: set[str]) -> float:
        scores = profile.df.drop(columns=['weight'])

        committee_vector = pd.Series(
            [1 if c in committee else 0 for c in scores.columns],
            index=scores.columns
        )

        distances = (scores ^ committee_vector).sum(axis=1)
        distances.sort(reverse=True)

        result = 0
        for i in range(len(distances)):
            result += distances[i] * weights[i]

        return result

    def _get_elected(profile: ApprovalProfile, weights: Sequence[float]) -> set[str]:
        candidates = profile.candidates
        best_score = float('-inf')
        best_committee = None

        for committee in itertools.combinations(candidates):
            score = _hamming_score(profile=profile, weights=weights, committee=committee)
            if score < best_score:
                best_score = score
                best_committee = committee
        
        return best_committee

