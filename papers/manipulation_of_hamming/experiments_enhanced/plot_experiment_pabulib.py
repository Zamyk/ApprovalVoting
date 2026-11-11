from pathlib import Path
import pandas as pd

from . import RESULTS_DIRECTORY_PATH, PLOTS_DIRECTORY_PATH
from ._plot_common import plot_m_grid

DEFAULT_CSV = "experiment_pabulib_integers_oneprofile_n25.csv"


def plot_experiment_pabulib(path=None, save=None, show=True, title="Pabulib Elections"):
  path = Path(path) if path else RESULTS_DIRECTORY_PATH / DEFAULT_CSV
  df = pd.read_csv(path)

  out = save or PLOTS_DIRECTORY_PATH / "plot_experiment_pabulib.png"
  return plot_m_grid(
    [(df, title)],
    "Ratio of Manipulation",
    out,
    figsize=(9.5, 4.2),
    group_col="label",
    show=show,
  )


if __name__ == "__main__":
  from .experiment_pabulib import VOTER_COUNTS

  for n in VOTER_COUNTS:
    plot_experiment_pabulib(
      path=RESULTS_DIRECTORY_PATH / f"experiment_pabulib_integers_oneprofile_n{n}.csv",
      save=PLOTS_DIRECTORY_PATH / f"plot_experiment_pabulib_integers_oneprofile_n{n}.png",
      show=False,
      title=f"Pabulib Elections ({n} voters)",
    )
