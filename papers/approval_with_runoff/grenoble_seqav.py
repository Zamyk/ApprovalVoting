from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

from approval_with_runoff import seq_components
from french_elections import ELECTIONS, load_election

SAVE = Path(__file__).resolve().parent / "plots" / "grenoble_seq.png"


def plot(show=True, save=None):
    ballots, codes = load_election(ELECTIONS["grenoble"])
    winner, counts, with_winner = seq_components(ballots)
    alphas = np.linspace(0, 1, 200)

    plt.figure(figsize=(8, 4.5))
    for i, code in enumerate(codes):
        if i == winner:
            continue
        score = counts[i] - alphas * with_winner[i]
        plt.plot(alphas, score, label=f"{code}")

    plt.axvline(x=0.5, color="black", linestyle="--", label="S-PAV")
    plt.title(f"Grenoble 2017, second-place score (winner: {codes[winner]})")
    plt.xlabel(r"$\alpha$")
    plt.ylabel(r"$S(c) - \alpha S(winner \cap c)$")
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
