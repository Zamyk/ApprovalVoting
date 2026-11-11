from . import PLOTS_DIRECTORY_PATH, RESULTS_DIRECTORY_PATH
from .plot_experiment_pabulib import plot_experiment_pabulib


def plot_experiment_pabulib_100(path=None, save=None, show=True, title="Pabulib Elections (100 voters)"):
  return plot_experiment_pabulib(
    path=path or RESULTS_DIRECTORY_PATH / "experiment_pabulib_integers_oneprofile_n100.csv",
    save=save or PLOTS_DIRECTORY_PATH / "plot_experiment_pabulib_100.png",
    show=show,
    title=title,
  )


if __name__ == "__main__":
  plot_experiment_pabulib_100()
