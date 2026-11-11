from ._plot_common import plot_m_pair_figure


def plot_experiment_1_newmanipulation():
    plot_m_pair_figure(
        ("experiment_1_newmanipulation_uniform", "experiment_1_newmanipulation_biased"),
        ("Uniform Elections", "Biased Elections"),
        "Ratio of VotersManipulation",
        "plot_experiment_1_newmanipulation",
        aggregate=False,
    )


if __name__ == "__main__":
    plot_experiment_1_newmanipulation()
