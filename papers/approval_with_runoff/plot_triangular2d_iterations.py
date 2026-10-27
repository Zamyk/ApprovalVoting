from pathlib import Path
from plot_seq import plot_iterations

HERE = Path(__file__).resolve().parent
RESULT = HERE / "results" / "results_triangular2d_iterations.csv"
SAVE = HERE / "plots" / "triangular2d_seq_iterations.png"


def plot(show=True, path=None, save=None):
  return plot_iterations(
    RESULT,
    save or SAVE,
    "Second finalist, 2D product-triangular (min-max over iterations)",
    show=show,
    path=path,
  )


if __name__ == "__main__":
  plot()
