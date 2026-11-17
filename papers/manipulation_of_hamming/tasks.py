"""Experiments of this paper, for the manager (``uv run python -m manager``).

Each entry names the module that runs the experiment, the module that plots it,
the CSVs the run writes (and the plot reads) and the figures the plot writes.
Paths are relative to the repository root.
"""

from manager.spec import experiment
from papers.manipulation_of_hamming.experiments_enhanced import RESAMPLING_PHIS

PHI_TAGS = [tag for tag, _ in RESAMPLING_PHIS]

PAPER = "manipulation_of_hamming"
TITLE = "Manipulation of Hamming-based Approval Voting (Barrot, Lang, Yokoo, AAMAS 2017)"
FAMILY_TITLES = {
    "exp1": "Experiment 1: manipulability vs orness (25 voters)",
    "exp2": "Experiment 2: manipulability vs number of voters",
    "other": "Other models and data",
    "original": "Original experiments (experiments/)",
}

ENHANCED = "papers.manipulation_of_hamming.experiments_enhanced"
ORIGINAL = "papers.manipulation_of_hamming.experiments"
ENH_DIR = "papers/manipulation_of_hamming/experiments_enhanced"
ORIG_DIR = "papers/manipulation_of_hamming/experiments"


def pair(stem, a, b):
    return [f"{stem}_{a}.csv", f"{stem}_{b}.csv"]


def enhanced(family, variant, stem, data, *, plot_stem=None, figures=None, **kwargs):
    """An experiment in experiments_enhanced: ``<stem>.py`` runs it, ``plot_<stem>.py`` plots it."""
    plot_stem = plot_stem or f"plot_{stem}"
    figures = figures or [f"plot_{stem}.png"]
    return experiment(
        PAPER, family, variant,
        run=f"{ENHANCED}.{stem}",
        plot=f"{ENHANCED}.{plot_stem}",
        data=[f"{ENH_DIR}/results/{d}" for d in data],
        figures=[f"{ENH_DIR}/plots/{f}" for f in figures],
        **kwargs,
    )


TASKS = [
    # ---- Experiment 1: orness ------------------------------------------------
    *enhanced("exp1", "integers", "experiment_1_integers",
              pair("experiment_1_integers", "uniform", "biased")),
    *enhanced("exp1", "integers-oneprofile", "experiment_1_integers_oneprofile",
              pair("experiment_1_integers_oneprofile", "uniform", "biased")),
    *enhanced("exp1", "newmanipulation", "experiment_1_newmanipulation",
              pair("experiment_1_newmanipulation", "uniform", "biased")),
    *enhanced("exp1", "newmanipulation-integers", "experiment_1_newmanipulation_integers",
              pair("experiment_1_newmanipulation_integers", "uniform", "biased")),
    *enhanced("exp1", "newmanipulation-integers-oneprofile",
              "experiment_1_newmanipulation_integers_oneprofile",
              pair("experiment_1_newmanipulation_integers_oneprofile", "uniform", "biased")),
    *enhanced("exp1", "euclidean", "experiment_1_euclidean",
              pair("experiment_1_euclidean", "normal", "triangle")),
    *enhanced("exp1", "euclidean-integers", "experiment_1_euclidean_integers",
              pair("experiment_1_euclidean_integers", "normal", "triangle")),
    *enhanced("exp1", "euclidean-integers-oneprofile", "experiment_1_euclidean_integers_oneprofile",
              pair("experiment_1_euclidean_integers_oneprofile", "normal", "triangle")),
    *enhanced("exp1", "iterations", "experiment_1_iterations",
              ["experiment_1_iterations_uniform_*.csv", "experiment_1_iterations_biased_*.csv"],
              note="many repeated runs, plotted as a min-max band"),
    *enhanced("exp1", "resampling-integers-oneprofile", "experiment_1_resampling_integers_oneprofile",
              [f"experiment_1_resampling_integers_oneprofile_{t}.csv" for t in PHI_TAGS],
              figures=[f"plot_experiment_1_resampling_integers_oneprofile_{t}.png" for t in PHI_TAGS],
              note="(p, phi)-resampling, p=0.5; one profile set shared across f; one figure per phi"),
    *enhanced("exp1", "resampling-integers", "experiment_1_resampling_integers",
              [f"experiment_1_resampling_integers_{t}.csv" for t in PHI_TAGS],
              figures=[f"plot_experiment_1_resampling_integers_{t}.png" for t in PHI_TAGS],
              note="(p, phi)-resampling, p=0.5, phi in {0.25, 0.5, 0.75}; one figure per phi"),

    # ---- Experiment 2: number of voters -------------------------------------
    *enhanced("exp2", "integers", "experiment_2_integers", ["experiment_2_integers.csv"]),
    *enhanced("exp2", "newmanipulation", "experiment_2_newmanipulation",
              ["experiment_2_newmanipulation.csv"],
              plot_stem="plot_experiment_2_newmanipulations",
              figures=["plot_experiment_2_newmanipulation.png"]),
    *enhanced("exp2", "newmanipulation-integers", "experiment_2_newmanipulation_integers",
              ["experiment_2_newmanipulation_integers.csv"]),
    *enhanced("exp2", "euclidean", "experiment_2_euclidean",
              pair("experiment_2_euclidean", "normal", "triangle")),
    *enhanced("exp2", "euclidean-integers", "experiment_2_euclidean_integers",
              pair("experiment_2_euclidean_integers", "normal", "triangle")),
    *enhanced("exp2", "euclidean-uniform-integers", "experiment_2_euclidean_uniform_integers",
              pair("experiment_2_euclidean_uniform_integers", "normal", "triangle")),
    *enhanced("exp2", "resampling-integers", "experiment_2_resampling_integers",
              [f"experiment_2_resampling_integers_{t}.csv" for t in PHI_TAGS],
              figures=[f"plot_experiment_2_resampling_integers_{t}.png" for t in PHI_TAGS],
              note="(p, phi)-resampling, p=0.5, phi in {0.25, 0.5, 0.75}; one figure per phi"),
    *enhanced("exp2", "iterations", "experiment_2_iterations", ["experiment_2_iterations_*.csv"],
              note="many repeated runs, plotted as a min-max band"),

    # ---- Other models and data ----------------------------------------------
    *enhanced("other", "ic-probability", "experiment_ic_probability",
              ["experiment_ic_probability.csv"],
              note="impartial culture with approval probability p on the x axis"),
    *enhanced("other", "pabulib-integers-oneprofile", "experiment_pabulib",
              [f"experiment_pabulib_integers_oneprofile_n{n}.csv" for n in (25, 50, 100)],
              plot_stem="plot_experiment_pabulib",
              figures=[f"plot_experiment_pabulib_integers_oneprofile_n{n}.png" for n in (25, 50, 100)],
              note="3 datasets x n = 25, 50, 100 voters x 20000 profiles: very long"),

    # ---- Original code (not the enhanced experiments) -----------------------
    *experiment(
        PAPER, "original", "exp1",
        run=f"{ORIGINAL}.experiment_1", plot=f"{ORIGINAL}.plot_experiment_1",
        data=[f"{ORIG_DIR}/results/experiment_1_uniform.csv",
              f"{ORIG_DIR}/results/experiment_1_biased.csv"],
        figures=[f"{ORIG_DIR}/plots/plot_experiment_1_uniform_and_biased.png"],
    ),
    *experiment(
        PAPER, "original", "exp2",
        run=f"{ORIGINAL}.experiment_2", plot=f"{ORIGINAL}.plot_experiment_2",
        data=[f"{ORIG_DIR}/results/experiment_2.csv"],
        figures=[f"{ORIG_DIR}/plots/plot_experiment_2.png"],
    ),
]
