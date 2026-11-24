from ._plot_common import plot_scatter_methods_grid

RULES_PANELS = [
    ("AV", "experiment_1_datasets-2_av.csv"),
    ("Greedy CC", "experiment_1_datasets-2_greedycc.csv"),
    ("Phragmén", "experiment_1_datasets-2_phragmen.csv"),
    ("5/4-Geometric\nRule", "experiment_1_datasets-2_5-4-geometric.csv"),
    ("2-Geometric\nRule", "experiment_1_datasets-2_2-geometric.csv"),
    ("10-Geometric\nRule", "experiment_1_datasets-2_10-geometric.csv"),
    ("SeqPAV", "experiment_1_datasets-2_seqpav.csv"),
    ("Reverse SeqPAV", "experiment_1_datasets-2_revseqpav.csv"),
    ("Best-of", "experiment_1_datasets-2_bestof.csv"),
]


def plot_experiment_1_datasets_2_generators():
    plot_scatter_methods_grid(
        RULES_PANELS,
        "plot_experiment_1_datasets_2_generators.png",
        legend_title="Generation Method",
        nrows=3,
        ncols=3,
        grid_figsize=(12, 12),
        bottom_space_inches=0.95,
    )


if __name__ == "__main__":
    plot_experiment_1_datasets_2_generators()