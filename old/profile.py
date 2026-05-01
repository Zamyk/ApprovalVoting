import pandas as pd
import numpy as np

from typing import Sequence

from votekit.pref_profile import ScoreProfile
from votekit.ballot import Ballot
from votekit.ballot import ScoreBallot


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
            d = {c: (1 if c in ballots[0].approved else 0) for c in candidates}
            score_ballots = [ScoreBallot(scores={c: (1 if c in ballot.approved else 0) for c in candidates}, weight=ballot.weight, voter_set=ballot.voter_set) for ballot in ballots]
            super().__init__(ballots=score_ballots, candidates=candidates, df=df)
        else:
            self.__validate_init_approval_df_binary_scores(df)
            super().__init__(candidates=candidates, df=df)

    def __validate_init_approval_df_binary_scores(self, df: pd.DataFrame) -> None:
        pass
        # """
        # Ensures that all candidate scores in the DataFrame are either 0 or 1.
        # """
        # scores = df.drop(columns=['Weight', 'Voter Set']).fillna(0)

        # if not df[score_cols].isin([0, 1]).all().all():
        #     raise ProfileError(
        #         "ApprovalProfile requires binary scores. "
        #         "Found values outside of {0, 1} in the provided DataFrame."
        #     )
    
    def change_vote(self, ballot_index: int, approved: set[str]) -> "ApprovalProfile":
        if ballot_index not in self.df.index:
            raise IndexError("ballot_index not in DataFrame index")

        df2 = self.df.copy()

        new_row = {c: 1 if c in approved else 0 for c in df2.columns if c not in ("Weight", "Voter Set")}

        for col in ("Weight", "Voter Set"):
            if col in df2.columns:
                new_row[col] = df2.at[ballot_index, col]

        df2.loc[ballot_index] = pd.Series(new_row)

        return ApprovalProfile(candidates=self.candidates, df=df2)