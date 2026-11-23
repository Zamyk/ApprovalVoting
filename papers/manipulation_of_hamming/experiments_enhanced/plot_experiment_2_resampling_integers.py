from . import RESAMPLING_P as P, RESAMPLING_PHIS as PHIS
from ._plot_common import plot_f_single_figure


def plot_experiment_2_resampling_integers():
    """One figure per phi, each in the experiment 2 layout."""
    for tag, phi in PHIS:
        plot_f_single_figure(
            f"experiment_2_resampling_integers_{tag}",
            f"plot_experiment_2_resampling_integers_{tag}",
            title=rf"$p={P}$, $\varphi={phi}$",
            # values reach 0, so the default 0.3-1.0 range would clip the curves
            ylim=(0.0, 1.0), yticks=(0.0, 0.2, 0.4, 0.6, 0.8, 1.0),
        )


if __name__ == "__main__":
    plot_experiment_2_resampling_integers()
