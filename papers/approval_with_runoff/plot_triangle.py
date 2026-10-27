from pathlib import Path
from plot_seq import plot_sample

HERE = Path(__file__).resolve().parent
RESULT = HERE / "results" / "results_triangle.csv"
SAVE = HERE / "plots" / "triangle_seq_original.png"


def plot(show=True, path=None, save=None):
  return plot_sample(
    RESULT,
    save or SAVE,
    "Position of the second finalist, triangular distribution",
    show=show,
    path=path,
  )


if __name__ == "__main__":
  plot()
