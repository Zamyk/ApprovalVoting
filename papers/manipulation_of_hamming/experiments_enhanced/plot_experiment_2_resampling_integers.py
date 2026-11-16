from ._plot_common import plot_f_single_figure

P = 0.5
PHIS = [("phi03", 0.3), ("phi05", 0.5), ("phi08", 0.8)]


def plot_experiment_2_resampling_integers():
    """One figure per phi, each in the experiment 2 layout."""
    for tag, phi in PHIS:
        plot_f_single_figure(
            f"experiment_2_resampling_integers_{tag}",
            f"plot_experiment_2_resampling_integers_{tag}",
            title=rf"$p={P}$, $\varphi={phi}$",
        )


if __name__ == "__main__":
    plot_experiment_2_resampling_integers()
