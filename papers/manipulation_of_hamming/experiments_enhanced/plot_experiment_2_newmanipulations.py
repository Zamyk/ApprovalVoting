from ._plot_common import plot_f_single_figure


def plot_experiment_2_newmanipulation():
    # per-voter metric: values are well below the 0.3-1.0 range of the other experiment 2 plots
    plot_f_single_figure("experiment_2_newmanipulation", "plot_experiment_2_newmanipulation",
                         ylim=(0.0, 0.4), yticks=(0.0, 0.1, 0.2, 0.3, 0.4))


if __name__ == "__main__":
    plot_experiment_2_newmanipulation()
