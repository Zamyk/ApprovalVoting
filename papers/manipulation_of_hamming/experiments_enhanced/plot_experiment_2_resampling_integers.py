from . import RESAMPLING_P as P, RESAMPLING_PHIS as PHIS
from ._plot_common import plot_f_single_figure


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
