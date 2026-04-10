import pandas as pd
import numpy as np

from typing import Sequence, cast, Tuple

from votekit.pref_profile import ScoreProfile
from votekit.pref_profile import ProfileError
from votekit.ballot import Ballot

from ballot import ApprovalBallot

class ApprovalProfile(ScoreProfile):
    def __init__(
        self,
        *,
        ballots: Sequence[Ballot] = tuple(),
        candidates: Sequence[str] = tuple(),
        df: pd.DataFrame = pd.DataFrame(),
    ):
        self.candidates = tuple(candidates)

        if df.equals(pd.DataFrame()):
            (
                self.df,
                self.candidates_cast,
            ) = self._init_from_approval_ballots(cast(Sequence[ApprovalBallot], ballots))

            if self.candidates == tuple():
                self.candidates = self.candidates_cast

        else:
            self.df, self.candidates_cast = self._init_from_approval_df(df)

        super().__init__(
            candidates=self.candidates,
            candidates_cast=self.candidates_cast,
            df=self.df,
        )

    def __update_ballot_approved_data(
        self,
        approval_ballot_data: dict[str, list],
        idx: int,
        ballot: ApprovalBallot,
        candidates_cast: list[str],
        num_ballots: int,
    ) -> None:
        """
        Update the score data from a ballot.

        Args:
            ballot_data (dict[str, list]): Dictionary storing ballot data.
            idx (int): Index of ballot.
            ballot (ScoreBallot): Ballot.
            candidates_cast (list[str]): List of candidates who have received votes.
            num_ballots (int): Total number of ballots.
        """
        if ballot.scores is None:
            return

        for c in ballot.approved:
            if ballot.weight > 0 and c not in candidates_cast:
                candidates_cast.append(c)

            if c not in approval_ballot_data:
                if self.candidates:
                    raise ProfileError(
                        f"Candidate {c} found in ballot {ballot} but not in "
                        f"candidate list {self.candidates}."
                    )
                approval_ballot_data[c] = [np.nan] * num_ballots
            approval_ballot_data[c][idx] = score

    def __update_score_ballot_data_attrs(
        self,
        score_ballot_data: dict[str, list],
        idx: int,
        ballot: ApprovalBallot,
        candidates_cast: list[str],
        num_ballots: int,
    ) -> None:
        """
        Update all ballot data from a ballot.

        Args:
            ballot_data (dict[str, list]): Dictionary storing ballot data.
            idx (int): Index of ballot.
            ballot (ApprovalBallot): Ballot.
            candidates_cast (list[str]): List of candidates who have received votes.
            num_ballots (int): Total number of ballots.
        """
        score_ballot_data["Weight"][idx] = ballot.weight

        if ballot.voter_set != frozenset():
            score_ballot_data["Voter Set"][idx] = ballot.voter_set

        if ballot.approved is not None:
            self.__update_ballot_approved_data(
                score_ballot_data=score_ballot_data,
                idx=idx,
                ballot=ballot,
                candidates_cast=candidates_cast,
                num_ballots=num_ballots,
            )

    def __init_score_ballot_data(
        self, ballots: Sequence[ApprovalBallot]
    ) -> Tuple[int, dict[str, list]]:
        """
        Create the ballot data objects.

        Args:
            ballots (Sequence[ApprovalBallot,...]): Tuple of ballots.

        Returns:
            Tuple[int, dict[str, list]]: num_ballots, score_ballot_data

        """
        num_ballots = len(ballots)

        approval_ballot_data: dict[str, list] = {
            "Weight": [np.nan] * num_ballots,
            "Voter Set": [set()] * num_ballots,
        }

        if self.candidates != tuple():
            approval_ballot_data.update({c: [np.nan] * num_ballots for c in self.candidates})

        return num_ballots, approval_ballot_data

    def __init_formatted_score_df(
        self,
        score_ballot_data: dict[str, list],
        candidates_cast: list[str],
    ) -> pd.DataFrame:
        """
        Create a pandas dataframe from the ballot data.

        Args:
            score_ballot_data (dict[str, list]): Dictionary storing ballot data.
            candidates_cast (list[str]): List of candidates who received votes.

        Returns:
            pd.DataFrame: Dataframe of profile.
        """
        df = pd.DataFrame(score_ballot_data)
        temp_col_order = [
            "Voter Set",
            "Weight",
        ]

        col_order = list(self.candidates) + temp_col_order

        if self.candidates == tuple():
            remaining_cands = set(candidates_cast) - set(df.columns)
            empty_df_cols = np.full((len(df), len(remaining_cands)), np.nan)
            df[list(remaining_cands)] = empty_df_cols

            col_order = sorted([c for c in df.columns if c not in temp_col_order]) + temp_col_order

        df = df[col_order]
        df.index.name = "Ballot Index"
        return df

    def _init_from_approval_ballots(
        self, ballots: Sequence[ApprovalBallot]
    ) -> tuple[pd.DataFrame, tuple[str, ...]]:
        """
        Create the pandas dataframe representation of the profile.

        Args:
            ballots (Sequence[ApprovalBallot,...]): Tuple of ballots.

        Returns: 
            tuple[pd.DataFrame, tuple[str, ...]]: df, candidates_cast

        """
        # `score_ballot_data` sends {Weight, Voter Set} keys to a list to be
        # indexed in the same order as the output df containing information
        # for each ballot. So ballot_data[<weight>][<index>] is the weight value for
        # the ballot at index <index> in the df.
        num_ballots, approval_ballot_data = self.__init_score_ballot_data(ballots)

        candidates_cast: list[str] = []

        for i, b in enumerate(ballots):
            self.__update_score_ballot_data_attrs(
                approval_ballot_data=approval_ballot_data,
                idx=i,
                ballot=b,
                candidates_cast=candidates_cast,
                num_ballots=num_ballots,
            )

        df = self.__init_formatted_score_df(
            score_ballot_data=score_ballot_data,
            candidates_cast=candidates_cast,
        )
        return (
            df,
            tuple(candidates_cast),
        )

    def __validate_init_approval_df_params(self, df: pd.DataFrame) -> None:
        """
        Validate that the correct params were passed to the init method when constructing
        from a dataframe.

        Args:
            df (pd.DataFrame): Dataframe representation of ballots.

        Raises:
            ValueError: One of contains_rankings and contains_scores must be True.
            ValueError: If contains_rankings is True, max_ranking_length must be provided.
            ValueError: Candidates must be provided.
        """
        boiler_plate = "When providing a dataframe and no ballot list to the init method, "
        if len(df) == 0:
            return

        if self.candidates == tuple():
            raise ProfileError(boiler_plate + "candidates must be provided.")

    def __validate_init_approval_df(self, df: pd.DataFrame) -> None:
        """
        Validate that the df passed to the init method is of valid type.

        Args:
            df (pd.DataFrame): Dataframe representation of ballots.

        Raises:
            ValueError: Candidate column is missing.
            ValueError: Ranking column is missing.
            ValueError: Weight column is missing.
            ValueError: Voter set column is missing.
            ValueError: Index column is misformatted.

        """
        if "Weight" not in df.columns:
            raise ProfileError(f"Weight column not in dataframe: {df.columns}")
        if "Voter Set" not in df.columns:
            raise ProfileError(f"Voter Set column not in dataframe: {df.columns}")
        if df.index.name != "Ballot Index":
            raise ProfileError(f"Index not named 'Ballot Index': {df.index.name}")
        if any(c not in df.columns for c in self.candidates):
            for c in self.candidates:
                if c not in df.columns:
                    raise ProfileError(f"Candidate column '{c}' not in dataframe: {df.columns}")

    def __find_candidates_cast_from_init_score_df(self, df: pd.DataFrame) -> tuple[str, ...]:
        """
        Compute which candidates received votes from the df and set the candidates_cast and
        candidates attr.

        Args:
            df (pd.DataFrame): Dataframe representation of ballots.

        Returns:
            tuple[str]: Candidates cast.
        """

        mask = df["Weight"] > 0

        candidates_cast: set[str] = set()

        positive = df.loc[mask, list(self.candidates)].gt(0).any()
        # .any() applies along the columns, so we get a boolean series where the
        # value is True the candidate has any positive score the column
        candidates_cast |= set(positive[positive].index)

        return tuple(candidates_cast)

    def _init_from_approval_df(self, df: pd.DataFrame) -> tuple[pd.DataFrame, tuple[str, ...]]:
        """
        Validate the dataframe and determine the candidates cast.

        Args:
            df (pd.DataFrame): Dataframe representation of ballots.

        Returns
            tuple[pd.DataFrame, tuple[str]]: df, candidates_cast
        """
        self.__validate_init_approval_df_params(df)
        self.__validate_init_approval_df(df)
        candidates_cast = self.__find_candidates_cast_from_init_score_df(df)

        return df, candidates_cast

    # todo?
    # @cached_property
    # def ballots(self: ScoreProfile) -> tuple[ScoreBallot, ...]:
    #     """
    #     Compute the ballot tuple as a cached property.
    #     """
    #     # TODO with map?
    #     computed_ballots = [ScoreBallot()] * len(self.df)
    #     for i, (_, b_row) in enumerate(self.df.iterrows()):
    #         computed_ballots[i] = convert_row_to_score_ballot(b_row, tuple(self.candidates))
    #     return tuple(computed_ballots)

    # todo!
    def __add__(self, other):
        return self        

    # todo?
    # def group_ballots(self) -> ScoreProfile:
    #     """
    #     Groups ballots by scores and updates weights. Retains voter sets, but
    #     loses ballot ids.

    #     Returns:
    #         ScoreProfile: A ScoreProfile object with grouped ballot list.
    #     """
    #     empty_df = pd.DataFrame(columns=["Voter Set", "Weight"], dtype=np.float64)
    #     empty_df.index.name = "Ballot Index"

    #     if len(self.df) == 0:
    #         return ScoreProfile(
    #             candidates=self.candidates,
    #         )

    #     non_group_cols = ["Weight", "Voter Set"]
    #     cand_cols = [c for c in self.df.columns if c not in non_group_cols]

    #     group_df = self.df.groupby(cand_cols, dropna=False)
    #     new_df = group_df.aggregate(
    #         {
    #             "Weight": "sum",
    #             "Voter Set": (lambda sets: set().union(*sets)),
    #         }
    #     ).reset_index()

    #     new_df.index.name = "Ballot Index"

    #     return ScoreProfile(
    #         df=new_df,
    #         candidates=self.candidates,
    #     )

    def __eq__(self, other):
        if not isinstance(other, ApprovalProfile):
            return False

        return super().__eq__(other)

    def __str__(self) -> str:
        repr_str = "ApprovalProfile\n"

        repr_str += (
            f"Candidates: {self.candidates}\n"
            f"Candidates who received votes: {self.candidates_cast}\n"
            f"Total number of Ballot objects: {self.num_ballots}\n"
            f"Total weight of Ballot objects: {self.total_ballot_wt}\n"
        )

        return repr_str

    __repr__ = __str__

    # todo!
    # def to_csv(
    #     self,
    #     fpath: str | PathLike | Path | None = None,
    #     include_voter_set: bool = False,
    #     weight_precision: int = 2,
    # ) -> str | None:        

    # todo!
    #@classmethod
    #def from_csv(cls, fpath: Union[str, PathLike, Path]) -> PreferenceProfile:   