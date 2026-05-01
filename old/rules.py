import pandas as pd
import itertools

from typing import Optional, Union, Sequence

from votekit.elections import Election
from votekit.elections import ElectionState

from profile import ApprovalProfile

class GeneralApproval(Election[ApprovalProfile]):

    def __init__(self, profile: ApprovalProfile):
        super().__init__(profile=profile)


def _hamming_score(profile: ApprovalProfile, weights: Sequence[float], committee: set[str]) -> float:
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

def _get_elected(profile: ApprovalProfile, weights: Sequence[float], tiebreak: Optional[str]) -> set[str]:
    candidates = profile.candidates
    best_score = float('inf')
    best_committee = set()

    # for k in range(len(candidates) + 1):
    #     for committee in itertools.combinations(candidates, k):
    #if tiebreak != 'lex': todo!

    for mask in range( (1 << (len(candidates))) - 1, -1, -1):
        committee = {cand for i, cand in enumerate(candidates) if (mask >> (len(candidates) - 1 - i)) & 1}
        score = _hamming_score(profile=profile, weights=weights, committee=committee)
        if score < best_score:
            best_score = score
            best_committee = set(committee)
    
    return best_committee

def _get_weights(weights, n):
    if weights == "minisum":
        weights = ("f", 0)
    elif weights == "minimax":
        weights = ("f", n-1)

    if isinstance(weights, tuple) and weights[0] == "f":
        i = weights[1]
        return [1.0/(n-i)] * (n-i) + [0.0] * i

    return weights

class OrderedWeightedHamming(GeneralApproval):

    def __init__(
        self, profile: ApprovalProfile, tiebreak: Optional[str] = None, weights: Union[Sequence[float] | str | tuple[str, int]] = "minisum"
    ):
        #print(profile.df)

        self.tiebreak = tiebreak
        self.weights = _get_weights(weights, len(profile.df))

        super().__init__(profile=profile)

    def _is_finished(self):
        # single round election
        if len(self.election_states) == 2:
            return True
        return False

    def _run_step(
        self, profile: ApprovalProfile, prev_state: ElectionState, store_states=False
    ) -> ApprovalProfile:

        elected = _get_elected(profile, self.weights, self.tiebreak)

        if store_states:
            new_state = ElectionState(
                round_number=1,  # single shot election
                elected=tuple(frozenset(elected)),
                eliminated=set(profile.candidates) - elected,
            )

            self.election_states.append(new_state)

        return profile