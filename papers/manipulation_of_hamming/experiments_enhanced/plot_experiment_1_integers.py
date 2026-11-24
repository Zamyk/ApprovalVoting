from ._plot_common import plot_m_pair_figure


def plot_experiment_1_integers():
    plot_m_pair_figure(
        ("experiment_1_integers_uniform", "experiment_1_integers_biased"),
        ("Uniform Elections", "Biased Elections"),
        "Ratio of Manipulation (altered definition)",
        "plot_experiment_1_integers",
        aggregate=False,
    )


if __name__ == "__main__":
    plot_experiment_1_integers()
