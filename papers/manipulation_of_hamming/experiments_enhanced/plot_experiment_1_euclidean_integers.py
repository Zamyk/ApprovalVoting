import argparse

from ._plot_common import plot_m_pair_figure


def plot_experiment_1_euclidean_integers(start_idx=None, end_idx=None):
    plot_m_pair_figure(
        ("experiment_1_euclidean_integers_normal", "experiment_1_euclidean_integers_triangle"),
        ("1D Euclidean (Normal)", "1D Euclidean (Triangle)"),
        "Ratio of Manipulation",
        "plot_experiment_1_euclidean_integers",
        start_idx, end_idx,
        aggregate=True, indexed=False, band_alpha=0.08, black_text=True,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot Experiment 1 Euclidean results.")
    parser.add_argument("start", type=int, nargs="?", default=None, help="Start file index (e.g. 0)")
    parser.add_argument("end", type=int, nargs="?", default=None, help="End file index (e.g. 49)")
    args = parser.parse_args()

    plot_experiment_1_euclidean_integers(args.start, args.end)
