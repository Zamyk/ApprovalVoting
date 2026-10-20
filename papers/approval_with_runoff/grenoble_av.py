from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

from approval_with_runoff import pair_lines, pairs_winning_somewhere
from french_elections import ELECTIONS, load_election

SAVE = Path(__file__).resolve().parent / "plots" / "grenoble_av.png"


def plot(show=True, save=None):
    ballots, codes = load_election(ELECTIONS["grenoble"])
    rows, cols, intercept, overlap = pair_lines(ballots)
    average = intercept - 0.5 * overlap
    keep = set(np.argsort(-average)[:10].tolist())
    winners = set(pairs_winning_somewhere(intercept, overlap)) & keep
    alphas = np.linspace(0, 1, 200)

    plt.figure(figsize=(8, 4.5))
    for k in sorted(keep - winners):
        score = intercept[k] - alphas * overlap[k]
        plt.plot(alphas, score, color="0.75", linewidth=0.8, zorder=1)
    for k in sorted(winners):
        score = intercept[k] - alphas * overlap[k]
        plt.plot(alphas, score, label=f"{codes[rows[k]]}/{codes[cols[k]]}", zorder=2)

    plt.axvline(x=0.5, color="black", linestyle="--", label="PAV")
    plt.title("Grenoble 2017, pair score (10 highest average)")
    plt.xlabel(r"$\alpha$")
    plt.ylabel(r"$S(i)+S(j)-\alpha S(i \cap j)$")
    plt.xlim(0, 1)
    plt.legend(loc="center left", bbox_to_anchor=(1.02, 0.5), fontsize=8)
    plt.grid(False)
    plt.tight_layout()
    out = Path(save) if save else SAVE
    plt.savefig(out, dpi=150, bbox_inches="tight")
    if show:
        plt.show()
    return out


if __name__ == "__main__":
    plot()
