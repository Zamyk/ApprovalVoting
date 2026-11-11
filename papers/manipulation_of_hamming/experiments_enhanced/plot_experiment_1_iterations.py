import argparse

from ._plot_common import plot_m_pair_figure


def plot_experiment_1_iterations(start_idx=None, end_idx=None):
    plot_m_pair_figure(
        ("experiment_1_iterations_uniform", "experiment_1_iterations_biased"),
        ("Uniform Elections", "Biased Elections"),
        "Ratio of Manipulation",
        "plot_experiment_1_iterations",
        start_idx, end_idx,
        aggregate=True, indexed=True, band_alpha=0.08, black_text=True,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot aggregated Experiment 1 iteration results.")
    parser.add_argument("start", type=int, nargs="?", default=None, help="Start file index (e.g. 0)")
    parser.add_argument("end", type=int, nargs="?", default=None, help="End file index (e.g. 24)")
    args = parser.parse_args()

    plot_experiment_1_iterations(args.start, args.end)
