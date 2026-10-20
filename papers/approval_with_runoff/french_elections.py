from pathlib import Path
import pandas as pd

DATA = Path(__file__).resolve().parent / "data"

ELECTIONS = {
    "grenoble": DATA / "GrenobleData_2017_Presid+.csv",
    "strasbourg": DATA / "StrasbourgData_2017_Presid+.csv",
    "crolles": DATA / "CrollesData_2017_Presid+.csv",
    "hsc": DATA / "HSCdata_2017_Presid+.csv",
}

_SKIP = {"AV_OPINION", "AV_SPOILED", "AV_BLANCK", "AV_BLANK"}


def load_election(path):
    try:
        df = pd.read_csv(path, sep=";")
    except UnicodeDecodeError:
        df = pd.read_csv(path, sep=";", encoding="latin-1")
    df.columns = [c.strip() for c in df.columns]
    columns = [c for c in df.columns if c.startswith("AV_") and c not in _SKIP]
    ballots = df[columns].apply(pd.to_numeric, errors="coerce")
    ballots = ballots.dropna(how="all").fillna(0).astype(int)
    codes = [c.removeprefix("AV_") for c in columns]
    return ballots.to_numpy(), codes
