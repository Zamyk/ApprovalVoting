"""Experiments for plotting grids, for the manager (``uv run python -m manager``).

Each entry names the module that runs the experiment, the module that plots it,
the CSVs the run writes (and the plot reads) and the figures the plot writes.
Paths are relative to the repository root.
"""

from manager.spec import experiment

PAPER = "proportional_rankings"
TITLE = "Proportional rankings grid plots"
FAMILY_TITLES = {
    "exp1": "Experiment 1: voting rules scatter grids",
}

EXP_MOD = "papers.proportional_rankings.experiments"
EXP_DIR = "papers/proportional_rankings/experiments"
ENH_MOD = "papers.proportional_rankings.experiments_enhanced"
ENH_DIR = "papers/proportional_rankings/experiments_enhanced"

EXP1_RULE_SUFFIXES = [
    "av",
    "greedycc",
    "phragmen",
    "5-4-geometric",
    "2-geometric",
    "10-geometric",
    "seqpav",
    "revseqpav",
    "bestof",
]

EXP1_ADDRULES_SUFFIXES = [
    "av",
    "greedycc",
    "phragmen",
    "mes",
    "5-4-geometric",
    "2-geometric",
    "10-geometric",
    "pav",
    "seqpav",
    "revseqpav",
    "bestof",
    "peters",
]

EXP1_RULE_FILES = [f"experiment_1_{s}.csv" for s in EXP1_RULE_SUFFIXES]
EXP1_DATASETS2_RULE_FILES = [f"experiment_1_datasets-2_{s}.csv" for s in EXP1_RULE_SUFFIXES]

EXP1_ADDRULES_FILES = [f"experiment_1_{s}.csv" for s in EXP1_ADDRULES_SUFFIXES]
EXP1_DATASETS2_ADDRULES_FILES = [f"experiment_1_datasets-2_{s}.csv" for s in EXP1_ADDRULES_SUFFIXES]


def _task(family, variant, mod_base, dir_base, run_stem, plot_stem, data, *, figures=None, **kwargs):
    figures = figures or [f"{plot_stem}.png"]
    return experiment(
        PAPER,
        family,
        variant,
        run=f"{mod_base}.{run_stem}",
        plot=f"{mod_base}.{plot_stem}",
        data=[f"{dir_base}/results/{d}" for d in data],
        figures=[f"{dir_base}/plots/{f}" for f in figures],
        **kwargs,
    )


TASKS = [
    # ---- Experiment 1: experiments/ (3x3, 9 reguł) --------------------------
    *_task("exp1", "all-rules", EXP_MOD, EXP_DIR, "experiment_1", "plot_experiment_1", EXP1_RULE_FILES),
    *_task("exp1", "all-rules-candidates", EXP_MOD, EXP_DIR, "experiment_1", "plot_experiment_1_candidates", EXP1_RULE_FILES),
    *_task("exp1", "all-rules-generators", EXP_MOD, EXP_DIR, "experiment_1", "plot_experiment_1_generators", EXP1_RULE_FILES),
    *_task("exp1", "all-rules-voters", EXP_MOD, EXP_DIR, "experiment_1", "plot_experiment_1_voters", EXP1_RULE_FILES),
    # ---- Experiment 1: experiments/ (3x3, 9 reguł, datasets-2) --------------
    *_task("exp1", "datasets-2", ENH_MOD, ENH_DIR, "experiment_1", "plot_experiment_1_datasets_2", EXP1_DATASETS2_RULE_FILES),
    *_task("exp1", "datasets-2-candidates", ENH_MOD, ENH_DIR, "experiment_1", "plot_experiment_1_datasets_2_candidates", EXP1_DATASETS2_RULE_FILES),
    *_task("exp1", "datasets-2-generators", ENH_MOD, ENH_DIR, "experiment_1", "plot_experiment_1_datasets_2_generators", EXP1_DATASETS2_RULE_FILES),
    *_task("exp1", "datasets-2-voters", ENH_MOD, ENH_DIR, "experiment_1", "plot_experiment_1_datasets_2_voters", EXP1_DATASETS2_RULE_FILES),
    # ---- Experiment 1: experiments_enhanced/ (3x4, 12 reguł, addrules) ------
    *_task("exp1", "addrules", ENH_MOD, ENH_DIR, "experiment_1", "plot_experiment_1_addrules", EXP1_ADDRULES_FILES),
    *_task("exp1", "addrules-candidates", ENH_MOD, ENH_DIR, "experiment_1", "plot_experiment_1_addrules_candidates", EXP1_ADDRULES_FILES),
    *_task("exp1", "addrules-generators", ENH_MOD, ENH_DIR, "experiment_1", "plot_experiment_1_addrules_generators", EXP1_ADDRULES_FILES),
    *_task("exp1", "addrules-voters", ENH_MOD, ENH_DIR, "experiment_1", "plot_experiment_1_addrules_voters", EXP1_ADDRULES_FILES),
    # ---- Experiment 1: experiments_enhanced/ (3x4, 12 reguł, datasets-2 + addrules)
    *_task("exp1", "datasets-2-addrules", ENH_MOD, ENH_DIR, "experiment_1", "plot_experiment_1_datasets_2_addrules", EXP1_DATASETS2_ADDRULES_FILES),
    *_task("exp1", "datasets-2-addrules-candidates", ENH_MOD, ENH_DIR, "experiment_1", "plot_experiment_1_datasets_2_addrules_candidates", EXP1_DATASETS2_ADDRULES_FILES),
    *_task("exp1", "datasets-2-addrules-generators", ENH_MOD, ENH_DIR, "experiment_1", "plot_experiment_1_datasets_2_addrules_generators", EXP1_DATASETS2_ADDRULES_FILES),
    *_task("exp1", "datasets-2-addrules-voters", ENH_MOD, ENH_DIR, "experiment_1", "plot_experiment_1_datasets_2_addrules_voters", EXP1_DATASETS2_ADDRULES_FILES),
]