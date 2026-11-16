from pathlib import Path

from approval_with_runoff import seq_components
from pabulib import load_instance, short_name
from plot_election import plot_seq_scores

SAVE = Path(__file__).resolve().parent / "plots" / "warszawa_seq.png"
TOP_N = 12


def plot(show=True, save=None, top_n=TOP_N):
  ballots, _codes, names = load_instance("warszawa_2023")
  labels = [short_name(n) for n in names]
  winner, _, _ = seq_components(ballots)
  return plot_seq_scores(
    ballots,
    labels,
    f"Warszawa 2023, second-place score "
    f"(winner: {labels[winner]}, top {top_n} by approvals)",
    save or SAVE,
    show=show,
    top_n=top_n,
  )


if __name__ == "__main__":
  plot()
