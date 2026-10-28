import pandas as pd
import matplotlib.pyplot as plt

from . import RESULTS_DIRECTORY_PATH, PLOTS_DIRECTORY_PATH


def plot_experiment_pabulib(path=None, save=None, show=True):
  path = path or RESULTS_DIRECTORY_PATH / "experiment_pabulib.csv"
  df = pd.read_csv(path)

  plt.figure(figsize=(8, 4.5))
  # Prefer higher m first so legend reads m=5, m=4, m=3
  for label in sorted(df["label"].unique(), key=lambda s: -int(df.loc[df["label"] == s, "m"].iloc[0])):
    subset = df[df["label"] == label].sort_values("orness")
    plt.plot(subset["orness"], subset["manipulability"], label=label)

  plt.xlabel("Orness Measure")
  plt.ylabel("Ratio of Manipulable Elections")
  plt.xlim(0.5, 1.0)
  plt.ylim(0, 1.0)
  plt.legend(loc="best", fontsize=9)
  plt.grid(False)
  plt.tight_layout()

  out = save or PLOTS_DIRECTORY_PATH / "plot_experiment_pabulib.png"
  plt.savefig(out, dpi=150, bbox_inches="tight")
  print(f"Plot saved as '{out}'")
  if show:
    plt.show()
  else:
    plt.close()
  return out


if __name__ == "__main__":
  plot_experiment_pabulib()
