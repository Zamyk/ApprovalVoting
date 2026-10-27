from pathlib import Path
from plot_seq import plot_sample

HERE = Path(__file__).resolve().parent
RESULT = HERE / "results" / "results_cone2d.csv"
SAVE = HERE / "plots" / "cone2d_seq.png"


def plot(show=True, path=None, save=None):
  return plot_sample(
    RESULT,
    save or SAVE,
    "Second finalist, 2D radial cone (one sample)",
    show=show,
    path=path,
  )


if __name__ == "__main__":
  plot()
