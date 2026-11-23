from . import RESULTS_DIRECTORY_PATH, PLOTS_DIRECTORY_PATH
import os
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

VOTER_BINS = [
    (2, 100, "2-100"),
    (101, 200, "101-200"),
    (201, 300, "201-300"),
    (301, 400, "301-400"),
    (401, 500, "401-500"),
    (501, 600, "501-600"),
]


def _format_subplot(ax, title, show_ylabel=False):
  ax.set_xlim(0.0, 1.0)
  ax.set_ylim(0.0, 1.0)
  ax.set_xticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
  ax.set_yticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
  ax.set_xticklabels(["0.0", "0.2", "0.4", "0.6", "0.8", "1.0"], fontsize=8)
  ax.set_yticklabels(["0.0", "0.2", "0.4", "0.6", "0.8", "1.0"], fontsize=8)
  ax.grid(True, linestyle=":", color="gray", alpha=0.7)
  ax.set_xlabel("a", fontsize=11)
  if show_ylabel:
    ax.set_ylabel("y_r", fontsize=11)
  ax.set_title(title, fontsize=12, pad=8)
  ax.tick_params(axis="both", which="major", labelsize=9)


def plot_scatter_a_yr_by_voters_bins():
  os.makedirs(PLOTS_DIRECTORY_PATH, exist_ok=True)

  for rule in RULES_INFO:
    file_path = RESULTS_DIRECTORY_PATH / f"experiment_1_{rule['suffix']}.csv"
    output_name = f"plot_scatter_a_yr_{rule['suffix']}_voters_bins.png"

    fig, axes = plt.subplots(2, 3, figsize=(15, 9))
    axes_flat = axes.flatten()

    if os.path.exists(file_path):
      try:
        df = pd.read_csv(file_path)

        for idx, (low, high, label) in enumerate(VOTER_BINS):
          ax = axes_flat[idx]
          subset = df[(df["n_voters"] >= low) & (df["n_voters"] <= high)]

          if not subset.empty:
            ax.scatter(
                subset["a"],
                subset["y_r"],
                color="gray",
                s=10,
                edgecolors="none",
            )
          else:
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

          _format_subplot(
              ax,
              title=f"Voters: {label}",
              show_ylabel=(idx % 3 == 0),
          )

      except Exception as e:
        for idx, (_, _, label) in enumerate(VOTER_BINS):
          ax = axes_flat[idx]
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
          _format_subplot(ax, title=f"Voters: {label}", show_ylabel=(idx % 3 == 0))
        print(f"Error reading '{file_path}': {e}")
    else:
      for idx, (_, _, label) in enumerate(VOTER_BINS):
        ax = axes_flat[idx]
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
        _format_subplot(ax, title=f"Voters: {label}", show_ylabel=(idx % 3 == 0))
      print(f"Missing file: '{file_path}'")

    fig.suptitle(rule["title"].replace("\n", " "), fontsize=15, y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(PLOTS_DIRECTORY_PATH / output_name, bbox_inches="tight", dpi=300)
    plt.close(fig)
    print(f"Plot saved as '{output_name}'")


if __name__ == "__main__":
  plot_scatter_a_yr_by_voters_bins()