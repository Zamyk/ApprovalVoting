from pathlib import Path

from french_elections import ELECTIONS, load_election
from plot_election import plot_av_pairs

SAVE = Path(__file__).resolve().parent / "plots" / "grenoble_av.png"


def plot(show=True, save=None, min_annotated=0):
  ballots, codes = load_election(ELECTIONS["grenoble"])
  return plot_av_pairs(
    ballots,
    codes,
    "Grenoble 2017, pair score (10 highest average)",
    save or SAVE,
    show=show,
    top_n=10,
    min_annotated=min_annotated,
  )


if __name__ == "__main__":
  plot()
