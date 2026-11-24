from . import RESULTS_DIRECTORY_PATH, PLOTS_DIRECTORY_PATH
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

RULES_INFO = [
    {"title": "AV", "suffix": "av"},
    {"title": "Greedy CC", "suffix": "greedycc"},
    {"title": "Phragmén", "suffix": "phragmen"},
    {"title": "MES", "suffix": "mes"},
    {"title": "5/4-Geometric Rule", "suffix": "5-4-geometric"},
    {"title": "2-Geometric Rule", "suffix": "2-geometric"},
    {"title": "10-Geometric Rule", "suffix": "10-geometric"},
    {"title": "PAV", "suffix": "pav"},
    {"title": "SeqPAV", "suffix": "seqpav"},
    {"title": "Reverse SeqPAV", "suffix": "revseqpav"},
    {"title": "Best-of", "suffix": "bestof"},
    {"title": "Peters", "suffix": "peters"},
]


def _plot_single_histogram(ax, series, title, xlabel, bins, xticks=None):
  clean = series.dropna()
  if clean.empty:
    ax.set_facecolor("#f9f9f9")
    ax.text(
        0.5,
        0.5,
        "Brak danych",
        color="gray",
        ha="center",
        va="center",
        transform=ax.transAxes,
        fontsize=11,
    )
  else:
    ax.hist(
        clean,
        bins=bins,
        color="#4C72B0",
        edgecolor="white",
        linewidth=0.8,
    )
    if xticks is not None:
      ax.set_xticks(xticks)

  ax.set_title(f"{title} (n={len(clean)})", fontsize=12, pad=8)
  ax.set_xlabel(xlabel, fontsize=11)
  ax.set_ylabel("Liczba rekordów", fontsize=11)
  ax.grid(True, axis="y", linestyle=":", color="gray", alpha=0.6)
  ax.tick_params(axis="both", which="major", labelsize=9)


def plot_histograms_candidates_and_voters(voter_bin_width=50):
  os.makedirs(PLOTS_DIRECTORY_PATH, exist_ok=True)

  # Koszyki dla kandydatów: centrowane na liczbach całkowitych (np. 1.5..15.5)
  cand_bins = np.arange(1.5, 16.6, 1.0)
  cand_xticks = list(range(2, 16))

  # Koszyki dla wyborców: co voter_bin_width (domyślnie 0..600 co 50)
  voter_bins = np.arange(0, 600 + voter_bin_width, voter_bin_width)
  voter_xticks = list(range(0, 601, 100))

  for rule in RULES_INFO:
    file_path = RESULTS_DIRECTORY_PATH / f"experiment_1_{rule['suffix']}.csv"
    output_name = f"___test___plot_hist_candidates_voters_{rule['suffix']}.png"

    fig, (ax_cand, ax_voters) = plt.subplots(1, 2, figsize=(13, 5))

    if os.path.exists(file_path):
      try:
        df = pd.read_csv(file_path)

        _plot_single_histogram(
            ax=ax_cand,
            series=df["candidates"],
            title="Rozkład liczby kandydatów",
            xlabel="candidates",
            bins=cand_bins,
            xticks=cand_xticks,
        )

        _plot_single_histogram(
            ax=ax_voters,
            series=df["n_voters"],
            title="Rozkład liczby wyborców",
            xlabel="n_voters",
            bins=voter_bins,
            xticks=voter_xticks,
        )

      except Exception as e:
        for ax, lbl in [
            (ax_cand, "Rozkład liczby kandydatów"),
            (ax_voters, "Rozkład liczby wyborców"),
        ]:
          ax.set_facecolor("#ffe6e6")
          ax.text(
              0.5,
              0.5,
              "Błąd pliku",
              color="red",
              ha="center",
              va="center",
              transform=ax.transAxes,
              fontsize=11,
          )
          ax.set_title(lbl, fontsize=12)
        print(f"Error reading '{file_path}': {e}")
    else:
      for ax, lbl in [
          (ax_cand, "Rozkład liczby kandydatów"),
          (ax_voters, "Rozkład liczby wyborców"),
      ]:
        ax.set_facecolor("#ffe6e6")
        ax.text(
            0.5,
            0.5,
            "Brak pliku",
            color="red",
            ha="center",
            va="center",
            transform=ax.transAxes,
            fontsize=11,
            fontweight="bold",
        )
        ax.set_title(lbl, fontsize=12)
      print(f"Missing file: '{file_path}'")

    fig.suptitle(rule["title"], fontsize=14, y=1.02)
    plt.tight_layout()
    plt.savefig(PLOTS_DIRECTORY_PATH / output_name, bbox_inches="tight", dpi=300)
    plt.close(fig)
    print(f"Plot saved as '{output_name}'")


if __name__ == "__main__":
  plot_histograms_candidates_and_voters()