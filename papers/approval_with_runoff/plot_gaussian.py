from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
RESULT = HERE / "results" / "results_gaussian.csv"
SAVE = HERE / "plots" / "gaussian_seq_original.png"


def plot(show=True, path=None, save=None):
    df = pd.read_csv(path or RESULT)
    plt.figure(figsize=(8, 4))
    for d_val in df["d"].unique():
        subset = df[df["d"] == d_val].sort_values("alpha")
        plt.plot(subset["alpha"], subset["distance"], label=f"d = {d_val}")
    plt.axvline(x=0.5, color="black", linestyle="--", label="S-PAV")
    plt.title("Position of the second finalist, Gaussian distribution")
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
