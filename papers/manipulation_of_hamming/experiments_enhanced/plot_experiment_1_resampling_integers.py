from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

from . import RESULTS_DIRECTORY_PATH, PLOTS_DIRECTORY_PATH

P = 0.5
PHIS = [("phi03", 0.3), ("phi05", 0.5), ("phi08", 0.8)]

LINE_STYLES = {5: (0, (5, 5)), 4: (0, (3, 4)), 3: (0, (1, 2))}
LINE_WIDTHS = {5: 1.8, 4: 1.2, 3: 1.2}


def plot_experiment_1_resampling_integers(directory=None, save=None, show=True):
  directory = Path(directory) if directory else RESULTS_DIRECTORY_PATH
  frames = []
  for tag, phi in PHIS:
    f = directory / f"experiment_1_resampling_integers_{tag}.csv"
    if f.exists():
      frames.append((phi, pd.read_csv(f)))
    else:
      print(f"Warning: {f.name} not found, skipping phi={phi}.")
  if not frames:
    raise FileNotFoundError(f"No experiment_1_resampling_integers_*.csv in {directory}")

  fig, axes = plt.subplots(1, len(frames), figsize=(4.2 * len(frames) + 1.2, 4),
                           sharey=True, layout="constrained", squeeze=False)
  for ax, (phi, df) in zip(axes[0], frames):
    for m in sorted(df["m"].unique(), reverse=True):
      subset = df[df["m"] == m].sort_values("orness")
      ax.plot(subset["orness"], subset["manipulability"], label=f"m={m}", color="black",
              linestyle=LINE_STYLES.get(m, "-"), linewidth=LINE_WIDTHS.get(m, 1.5))
    ax.set_title(rf"$p={P}$, $\varphi={phi}$", fontsize=14)
    ax.set_xlim(0.5, 1.0)
    ax.set_ylim(0, 1.0)
    ax.set_xticks([0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
    ax.set_xticklabels(["0.5", "0.6", "0.7", "0.8", "0.9", "1"])
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.tick_params(axis="both", which="major", direction="in", right=True, top=False, labelsize=12)
  axes[0][0].set_yticklabels(["0", "0.25", "0.5", "0.75", "1"])
  axes[0][0].set_ylabel("Ratio of Manipulation", fontsize=14)
  fig.supxlabel("Orness Measure", fontsize=14)

  handles, labels = axes[0][-1].get_legend_handles_labels()
  fig.legend(handles, labels, loc="outside right center", frameon=False, fontsize=12, handlelength=2.5)

  out = save or PLOTS_DIRECTORY_PATH / "plot_experiment_1_resampling_integers.png"
  fig.savefig(out, dpi=300)
  print(f"Plot saved as '{out}'")
  if show:
    plt.show()
  else:
    plt.close(fig)
  return out


if __name__ == "__main__":
  plot_experiment_1_resampling_integers()
