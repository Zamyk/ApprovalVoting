import pandas as pd
import numpy as np

from typing import Sequence, cast, Tuple

from votekit.pref_profile import ScoreProfile
from votekit.pref_profile import ProfileError
from votekit.ballot import Ballot
from votekit.ballot import ScoreBallot

from ballot import ApprovalBallot

class ApprovalProfile(ScoreProfile):
    def __new__(
        cls,
        *,
        ballots: Sequence[Ballot] = tuple(),
        candidates: Sequence[str] = tuple(),
        df: pd.DataFrame = pd.DataFrame(),
    ):
        return super().__new__(cls)


    def __init__(
        self,
        *,
        ballots: Sequence[Ballot] = tuple(),
        candidates: Sequence[str] = tuple(),
        df: pd.DataFrame = pd.DataFrame(),
    ):
        self.candidates = tuple(candidates)



        if df.equals(pd.DataFrame()):
            score_ballots = [ScoreBallot(scores={c: 1 for c in ballot.approved}, weight=ballot.weight, voter_set=ballot.voter_set) for ballot in ballots]
            super().__init__(ballots=score_ballots, candidates=candidates, df=df)
        else:
            self.__validate_init_approval_df_binary_scores(self, df)
            super().__init__(candidates=candidates, df=df)

    def __validate_init_approval_df_binary_scores(self, df: pd.DataFrame) -> None:
        """
        Ensures that all candidate scores in the DataFrame are either 0 or 1.
        """
        # Identify columns that are candidate scores (everything except 'weight')
        score_cols = [col for col in df.columns if col != "weight"]

        # Check if all values in these columns are within the set {0, 1}
        # .isin([0, 1]) creates a boolean mask; .all().all() checks the entire grid
        if not df[score_cols].isin([0, 1]).all().all():
            raise ProfileError(
                "ApprovalProfile requires binary scores. "
                "Found values outside of {0, 1} in the provided DataFrame."
            )