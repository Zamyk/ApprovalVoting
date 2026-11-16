from pathlib import Path
import pandas as pd

from . import RESULTS_DIRECTORY_PATH, PLOTS_DIRECTORY_PATH
from ._plot_common import plot_m_panels

P = 0.5
PHIS = [("phi03", 0.3), ("phi05", 0.5), ("phi08", 0.8)]


def plot_experiment_1_resampling_integers(directory=None, save_dir=None, show=True):
  """One figure per phi, each in the experiment 1 layout. Returns the saved paths."""
  directory = Path(directory) if directory else RESULTS_DIRECTORY_PATH
  save_dir = Path(save_dir) if save_dir else PLOTS_DIRECTORY_PATH
  saved = []
  for tag, phi in PHIS:
    f = directory / f"experiment_1_resampling_integers_{tag}.csv"
    if not f.exists():
      print(f"Warning: {f.name} not found, skipping phi={phi}.")
      continue
    df = pd.read_csv(f)
    out = save_dir / f"plot_experiment_1_resampling_integers_{tag}.png"
    saved.append(plot_m_panels([(df, rf"$p={P}$, $\varphi={phi}$")], "Ratio of Manipulation", out, show=show))
  if not saved:
    raise FileNotFoundError(f"No experiment_1_resampling_integers_*.csv in {directory}")
  return saved


if __name__ == "__main__":
  plot_experiment_1_resampling_integers()
