from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

from . import RESULTS_DIRECTORY_PATH, PLOTS_DIRECTORY_PATH
from ._plot_common import F_STYLES as STYLE


def plot_experiment_ic_probability(path=None, save=None, show=True, title="Impartial Culture"):
  path = Path(path) if path else RESULTS_DIRECTORY_PATH / "experiment_ic_probability.csv"
  df = pd.read_csv(path)

  fig, ax = plt.subplots(figsize=(8.5, 4.6), layout="constrained")
  for rule in ["f_2n_3", "f_n_2", "f_n_3", "Borda"]:
    s = df[df["f"] == rule].sort_values("p")
    if s.empty:
      continue
    st = STYLE[rule]
    ax.plot(s["p"], s["manipulability"], color="black", linestyle=st["ls"],
            linewidth=st["lw"], label=st["label"])
  if title:
    ax.set_title(title, fontsize=14)
  ax.set_xlabel("Approval probability", fontsize=13)
  ax.set_ylabel("Ratio of Manipulation", fontsize=13)
  ax.set_xlim(0, 1)
  ax.set_ylim(0, 1)
  ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
  ax.tick_params(axis="both", which="major", direction="in", labelsize=12, length=6)
  handles, labels = ax.get_legend_handles_labels()
  fig.legend(handles, labels, loc="outside right center", frameon=False, fontsize=14, handlelength=3)

  out = save or PLOTS_DIRECTORY_PATH / "plot_experiment_ic_probability.png"
  fig.savefig(out, dpi=300)
  print(f"Plot saved as '{out}'")
  if show:
    plt.show()
  else:
    plt.close(fig)
  return out


if __name__ == "__main__":
  plot_experiment_ic_probability()
