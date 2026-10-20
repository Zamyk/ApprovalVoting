from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
RESULT = HERE / "results" / "results_gaussian_iterations.csv"
SAVE = HERE / "plots" / "gaussian_seq_iterations.png"


def plot(show=True, path=None, save=None):
    grouped = pd.read_csv(path or RESULT)
    plt.figure(figsize=(8, 4))
    for d_val in grouped["d"].unique():
        subset = grouped[grouped["d"] == d_val].sort_values("alpha")
        line, = plt.plot(subset["alpha"], subset["mean"], label=f"d = {d_val}")
        plt.fill_between(
            subset["alpha"],
            subset["min"].clip(lower=0, upper=1),
            subset["max"].clip(lower=0, upper=1),
            color=line.get_color(),
            alpha=0.15,
        )
    plt.axvline(x=0.5, color="black", linestyle="--", label="S-PAV")
    plt.title("Second finalist, Gaussian distribution (min-max over iterations)")
    plt.xlabel(r"$\alpha$")
    plt.ylabel("distance between finalists")
    plt.ylim(0, 1.0)
    plt.xlim(0, 1.0)
    plt.legend()
    plt.grid(False)
    plt.tight_layout()
    out = Path(save) if save else SAVE
    plt.savefig(out, dpi=150, bbox_inches="tight")
    if show:
        plt.show()
    return out


if __name__ == "__main__":
    plot()
