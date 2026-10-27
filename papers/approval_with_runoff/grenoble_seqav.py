from pathlib import Path

from approval_with_runoff import seq_components
from french_elections import ELECTIONS, load_election
from plot_election import plot_seq_scores

SAVE = Path(__file__).resolve().parent / "plots" / "grenoble_seq.png"


def plot(show=True, save=None):
  ballots, codes = load_election(ELECTIONS["grenoble"])
  winner, _, _ = seq_components(ballots)
  return plot_seq_scores(
    ballots,
    codes,
    f"Grenoble 2017, second-place score (winner: {codes[winner]})",
    save or SAVE,
    show=show,
  )


if __name__ == "__main__":
  plot()
