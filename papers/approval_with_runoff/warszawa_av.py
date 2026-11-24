from pathlib import Path

from pabulib import load_instance, short_name
from plot_election import plot_av_pairs

SAVE = Path(__file__).resolve().parent / "plots" / "warszawa_av.png"
TOP_N = 10
WIN_SCAN = 40
MIN_ANNOTATED = 6


def plot(show=True, save=None, top_n=TOP_N, win_scan=WIN_SCAN, min_annotated=MIN_ANNOTATED):
  ballots, _codes, names = load_instance("warszawa_2023")
  labels = [short_name(n, 28) for n in names]
  return plot_av_pairs(
    ballots,
    labels,
    f"Warszawa 2023, pair score ({top_n} highest average)",
    save or SAVE,
    show=show,
    top_n=top_n,
    win_scan=win_scan,
    min_annotated=min_annotated,
  )


if __name__ == "__main__":
  plot()
