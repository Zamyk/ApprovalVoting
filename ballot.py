from typing import Iterable, Union

from votekit.ballot import Ballot

class ApprovalBallot(Ballot):
    __slots__ = ["approved"]

    def __init__(
        self,
        *,
        approved: Iterable[str],
        weight: Union[float, int] = 1.0,
        voter_set: Union[set[str], frozenset[str]] = frozenset(),
        **kwargs
    ):
        self.approved = frozenset(c.strip() for c in approved)
        
        super().__init__(weight=weight, voter_set=voter_set)

    def __hash__(self):
        return hash(self.approved) + super().__hash__()

    def __eq__(self, other):
        if not isinstance(other, ApprovalBallot):
            return False
        return self.approved == other.approved and super().__eq__(other)