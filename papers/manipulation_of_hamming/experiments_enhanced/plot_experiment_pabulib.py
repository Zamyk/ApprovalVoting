from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

from . import RESULTS_DIRECTORY_PATH, PLOTS_DIRECTORY_PATH


def plot_experiment_pabulib(path=None, save=None, show=True, title="Pabulib Elections"):
  if path is None:
    default_path = RESULTS_DIRECTORY_PATH / "experiment_pabulib.csv"
    smoke_path = RESULTS_DIRECTORY_PATH / "experiment_pabulib_smoke.csv"
    path = default_path if default_path.exists() else (smoke_path if smoke_path.exists() else default_path)
  else:
    path = Path(path)

  df = pd.read_csv(path)

  fig, ax = plt.subplots(figsize=(9.5, 4.2), layout="constrained")

  # Define line styles and widths for different 'm' values to match the black-and-white print style
  line_styles = {
      5: (0, (5, 5)),  # Thicker standard dashed
      4: (0, (3, 4)),  # Thinner, tighter dashed
      3: (0, (1, 2)),  # Dotted
  }

  line_widths = {
      5: 1.8,
      4: 1.2,
      3: 1.2,
  }

  if "label" in df.columns:
    group_col = "label"
    sort_key = lambda s: -int(df.loc[df["label"] == s, "m"].iloc[0]) if "m" in df.columns else s
  else:
    group_col = "m"
    sort_key = lambda s: -int(s)

  # Sort descending so legend displays m=5, m=4, m=3 from top to bottom
  for key in sorted(df[group_col].unique(), key=sort_key):
    subset = df[df[group_col] == key].sort_values("orness")
    m = int(subset["m"].iloc[0]) if "m" in subset.columns else key
    label = key if group_col == "label" else f"m={m}"

    ls = line_styles.get(m, "-")
    lw = line_widths.get(m, 1.5)

    ax.plot(
        subset["orness"],
        subset["manipulability"],
        label=label,
        color="black",
        linestyle=ls,
        linewidth=lw,
    )

  if title:
    ax.set_title(title, fontsize=14)

  # Format axis limits and ticks to match experiment 1
  ax.set_xlim(0.5, 1.0)
  ax.set_ylim(0, 1.0)
  ax.set_xticks([0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
  ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])

  # Configure ticks to point inward (direction='in') as in experiment 1
  ax.tick_params(axis="both", which="major", direction="in", right=True, top=False, labelsize=12)
  ax.set_xticklabels(["0.5", "0.6", "0.7", "0.8", "0.9", "1"])
  ax.set_yticklabels(["0", "0.25", "0.5", "0.75", "1"])

  # Set X and Y labels
  ax.set_xlabel("Orness Measure", fontsize=14, labelpad=10)
  ax.set_ylabel("Ratio of Manipulation", fontsize=14, labelpad=10)

  # Place legend outside the axes on the right
  handles, labels = ax.get_legend_handles_labels()
  fig.legend(
      handles,
      labels,
      loc="outside right center",
      frameon=False,
      fontsize=12,
      handlelength=2.5,
  )

  out = save or PLOTS_DIRECTORY_PATH / "plot_experiment_pabulib.png"
  fig.savefig(out, dpi=300)
  print(f"Plot saved as '{out}'")
  if show:
    plt.show()
  else:
    plt.close()
  return out


if __name__ == "__main__":
  plot_experiment_pabulib()

