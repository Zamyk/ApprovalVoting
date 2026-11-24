from ._plot_common import plot_scatter_grid

RULES_PANELS = [
    ("AV", "experiment_1_av.csv"),
    ("Greedy CC", "experiment_1_greedycc.csv"),
    ("Phragmén", "experiment_1_phragmen.csv"),
    ("MES", "experiment_1_mes.csv"),
    ("5/4-Geometric\nRule", "experiment_1_5-4-geometric.csv"),
    ("2-Geometric\nRule", "experiment_1_2-geometric.csv"),
    ("10-Geometric\nRule", "experiment_1_10-geometric.csv"),
    ("PAV", "experiment_1_pav.csv"),
    ("SeqPAV", "experiment_1_seqpav.csv"),
    ("Reverse SeqPAV", "experiment_1_revseqpav.csv"),
    ("Best-of", "experiment_1_bestof.csv"),
    ("Peters", "experiment_1_peters.csv"),
]


def plot_experiment_1_addrules():
    plot_scatter_grid(
        RULES_PANELS,
        "plot_experiment_1_addrules.png",
        nrows=3,
        ncols=4,
        figsize=(16, 12),
        x_col="a",
        y_col="y_r",
        point_size=8,
        hspace=0.4,
        wspace=0.3,
    )


if __name__ == "__main__":
    plot_experiment_1_addrules()