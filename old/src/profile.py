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
        pass # TODO!


    def __init__(
        self,
        *,
        ballots: Sequence[Ballot] = tuple(),
        candidates: Sequence[str] = tuple(),
        df: pd.DataFrame = pd.DataFrame(),
    ):
        pass # TODO!
