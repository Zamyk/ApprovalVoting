"""Experiments of this paper, for the manager (``uv run python -m manager``).

Runs and plots go through ``cli.py`` (the modules here import each other by plain name, so
they cannot be started with ``-m`` directly). Paths are relative to the repository root.
"""

from manager.spec import Task, experiment

PAPER = "approval_with_runoff"
TITLE = "Approval with Runoff (sequential approval voting)"
FAMILY_TITLES = {
    "1d": "One-dimensional Euclidean elections (triangle, Gaussian)",
    "2d": "Two-dimensional Euclidean elections",
    "real": "Real elections (Grenoble 2017, Warszawa 2023)",
}

CLI = "papers.approval_with_runoff.cli"
DIR = "papers/approval_with_runoff"


def euclidean(family, variant, name, results, figures, **kwargs):
    """Slow computation: a run task writes ``results/<file>``, a plot task reads it."""
    return experiment(
        PAPER, family, variant,
        run=CLI, plot=CLI, run_args=("compute", name), plot_args=("plot", name),
        data=[f"{DIR}/results/{r}" for r in results],
        figures=[f"{DIR}/plots/{f}" for f in figures],
        **kwargs,
    )


def fast(family, variant, name, results, figure):
    """Plot-only task: the computation takes seconds, so the plot task does it itself."""
    return [Task(f"{PAPER}/{family}/{variant}:plot", "plot", PAPER, family, variant, CLI,
                 writes=(f"{DIR}/plots/{figure}",), args=("plot", name),
                 note=f"computes {results} (seconds) and plots it")]


def election(variant, name, data, figure):
    """Plot-only task: the input is a data file shipped in the repository."""
    return [Task(f"{PAPER}/real/{variant}:plot", "plot", PAPER, "real", variant, CLI,
                 reads=(f"{DIR}/data/{data}",), writes=(f"{DIR}/plots/{figure}",),
                 args=("plot", name))]


TASKS = [
    # ---- 1D ------------------------------------------------------------------
    *fast("1d", "triangle-sample", "triangle", "results_triangle.csv", "triangle_seq_original.png"),
    *fast("1d", "gaussian-sample", "gaussian", "results_gaussian.csv", "gaussian_seq_original.png"),
    *fast("1d", "triangle-iterations", "triangle_iterations", "results_triangle_iterations.csv", "triangle_seq_iterations.png"),
    *fast("1d", "gaussian-iterations", "gaussian_iterations", "results_gaussian_iterations.csv", "gaussian_seq_iterations.png"),
    *euclidean("1d", "triangle-av", "triangle_av",
               ["results_triangle_av_winner.csv", "results_triangle_av_second.csv"],
               ["triangle_av_winner_iterations.png", "triangle_av_second_iterations.png"]),
    *euclidean("1d", "gaussian-av", "gaussian_av",
               ["results_gaussian_av_winner.csv", "results_gaussian_av_second.csv"],
               ["gaussian_av_winner_iterations.png", "gaussian_av_second_iterations.png"]),
    # ---- 2D ------------------------------------------------------------------
    *fast("2d", "triangular-sample", "triangular2d", "results_triangular2d.csv", "triangular2d_seq.png"),
    *fast("2d", "cone-sample", "cone2d", "results_cone2d.csv", "cone2d_seq.png"),
    *fast("2d", "gaussian-sample", "gaussian2d", "results_gaussian2d.csv", "gaussian2d_seq.png"),
    *euclidean("2d", "triangular-iterations", "triangular2d_iterations",
               ["results_triangular2d_iterations.csv"], ["triangular2d_seq_iterations.png"]),
    *euclidean("2d", "cone-iterations", "cone2d_iterations",
               ["results_cone2d_iterations.csv"], ["cone2d_seq_iterations.png"]),
    *euclidean("2d", "gaussian-iterations", "gaussian2d_iterations",
               ["results_gaussian2d_iterations.csv"], ["gaussian2d_seq_iterations.png"]),
    # ---- real elections (no run step, data is in the repo) ---------------------
    *election("grenoble-seqav", "grenoble_seqav", "GrenobleData_2017_Presid+.csv", "grenoble_seq.png"),
    *election("grenoble-av", "grenoble_av", "GrenobleData_2017_Presid+.csv", "grenoble_av.png"),
    *election("warszawa-seqav", "warszawa_seqav", "Poland_Warszawa_2023.pb", "warszawa_seq.png"),
    *election("warszawa-av", "warszawa_av", "Poland_Warszawa_2023.pb", "warszawa_av.png"),
]
