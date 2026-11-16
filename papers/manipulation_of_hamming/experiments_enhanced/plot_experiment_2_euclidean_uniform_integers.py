import argparse

from ._plot_common import plot_f_pair_figure


def plot_experiment_2_euclidean_uniform_integers(start_idx=None, end_idx=None):
    plot_f_pair_figure(
        ("experiment_2_euclidean_uniform_integers_normal",
         "experiment_2_euclidean_uniform_integers_triangle"),
        ("1D Euclidean (Normal voters)\nuniform candidates",
         "1D Euclidean (Triangle voters)\nuniform candidates"),
        "plot_experiment_2_euclidean_uniform_integers",
        start_idx, end_idx,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot Experiment 2 Euclidean results.")
    parser.add_argument("start", type=int, nargs="?", default=None, help="Start file index (e.g. 0)")
    parser.add_argument("end", type=int, nargs="?", default=None, help="End file index (e.g. 49)")
    args = parser.parse_args()

    plot_experiment_2_euclidean_uniform_integers(args.start, args.end)
