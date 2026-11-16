from pathlib import Path
from plot_seq import plot_iterations

HERE = Path(__file__).resolve().parent
RESULT = HERE / "results" / "results_triangle_iterations.csv"
SAVE = HERE / "plots" / "triangle_seq_iterations.png"


def plot(show=True, path=None, save=None):
  return plot_iterations(
    RESULT,
    save or SAVE,
    "Second finalist, triangular distribution (min-max over iterations)",
    show=show,
    path=path,
  )


if __name__ == "__main__":
  plot()
