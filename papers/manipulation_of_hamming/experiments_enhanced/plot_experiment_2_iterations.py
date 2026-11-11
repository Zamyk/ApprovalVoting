import argparse

from ._plot_common import plot_f_single_figure


def plot_experiment_2_iterations(start_idx=None, end_idx=None):
    plot_f_single_figure(
        "experiment_2_iterations", "plot_experiment_2_iterations", start_idx, end_idx,
        aggregate=True, indexed=True, band_alpha=0.06, black_text=True,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot aggregated Experiment 2 iteration results.")
    parser.add_argument("start", type=int, nargs="?", default=None, help="Start file index (e.g. 0)")
    parser.add_argument("end", type=int, nargs="?", default=None, help="End file index (e.g. 24)")
    args = parser.parse_args()

    plot_experiment_2_iterations(args.start, args.end)
