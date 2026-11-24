from ._plot_common import plot_m_pair_figure


def plot_experiment_1_integers_oneprofile():
    plot_m_pair_figure(
        ("experiment_1_integers_oneprofile_uniform", "experiment_1_integers_oneprofile_biased"),
        ("Uniform Elections", "Biased Elections"),
        "Ratio of Manipulation (altered definition)",
        "plot_experiment_1_integers_oneprofile",
        aggregate=False,
    )


if __name__ == "__main__":
    plot_experiment_1_integers_oneprofile()
