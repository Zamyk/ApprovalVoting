"""Experiments of this paper, for the manager (``uv run python -m manager``).

Runs and plots go through ``cli.py`` (the modules here import each other by plain name, so
they cannot be started with ``-m`` directly). Paths are relative to the repository root.
"""

from manager.spec import Task, experiment

PAPER = "approval_with_runoff"
TITLE = "Approval with Runoff (sequential approval voting)"
FAMILY_TITLES = {
    "1d": "One-dimensional Euclidean elections (triangle, Gaussian; candidates ~ voters)",
    "2d": "Two-dimensional Euclidean elections (candidates uniform / ~ voters)",
    "real": "Real elections (Grenoble 2017; PaBuLib: Warszawa 2023, Gdynia 2024, Łódź 2026, Poznań 2023)",
}

CLI = "papers.approval_with_runoff.cli"
DIR = "papers/approval_with_runoff"


def euclidean(family, variant, name, results, figures, **kwargs):
    """Synthetic experiment: a run task writes ``results/<file>``, a plot task reads it."""
    return experiment(
        PAPER, family, variant,
        run=CLI, plot=CLI, run_args=("compute", name), plot_args=("plot", name),
        data=[f"{DIR}/results/{r}" for r in results],
        figures=[f"{DIR}/plots/{f}" for f in figures],
        **kwargs,
    )


def election(variant, name, data, figure):
    """Plot-only task: the input is a data file shipped in the repository."""
    return [Task(f"{PAPER}/real/{variant}:plot", "plot", PAPER, "real", variant, CLI,
                 reads=(f"{DIR}/data/{data}",), writes=(f"{DIR}/plots/{figure}",),
                 args=("plot", name))]


TASKS = [
    # ---- 1D ------------------------------------------------------------------
    *euclidean("1d", "triangle-sample", "triangle", ["results_triangle.csv"], ["triangle_seq_original.png"]),
    *euclidean("1d", "gaussian-sample", "gaussian", ["results_gaussian.csv"], ["gaussian_seq_original.png"]),
    *euclidean("1d", "triangle-iterations", "triangle_iterations",
               ["results_triangle_iterations.csv"], ["triangle_seq_iterations.png"]),
    *euclidean("1d", "gaussian-iterations", "gaussian_iterations",
               ["results_gaussian_iterations.csv"], ["gaussian_seq_iterations.png"]),
    *euclidean("1d", "triangle-av", "triangle_av",
               ["results_triangle_av_winner.csv", "results_triangle_av_second.csv"],
               ["triangle_av_winner_iterations.png", "triangle_av_second_iterations.png"]),
    *euclidean("1d", "gaussian-av", "gaussian_av",
               ["results_gaussian_av_winner.csv", "results_gaussian_av_second.csv"],
               ["gaussian_av_winner_iterations.png", "gaussian_av_second_iterations.png"]),
    # ---- 2D: each voter model with uniform candidates (-unif) and candidates ~ voters (-same)
    *[task
      for model, stem in [("triangular", "triangular2d"), ("cone", "cone2d"), ("gaussian", "gaussian2d")]
      for cand in ("unif", "same")
      for task in [
          *euclidean("2d", f"{model}-{cand}-sample", f"{stem}_{cand}",
                     [f"results_{stem}_{cand}.csv"], [f"{stem}_{cand}_seq.png"]),
          *euclidean("2d", f"{model}-{cand}-iterations", f"{stem}_{cand}_iterations",
                     [f"results_{stem}_{cand}_iterations.csv"], [f"{stem}_{cand}_seq_iterations.png"]),
      ]],
    # ---- real elections (no run step, data is in the repo) ---------------------
    *[task
      for name, data in [
          ("grenoble", "GrenobleData_2017_Presid+.csv"),
          ("warszawa", "Poland_Warszawa_2023.pb"),
          ("gdynia", "Poland_Gdynia_2024.pb"),
          ("lodz", "Poland_Lodz_2026.pb"),
          ("poznan", "Poland_Poznan_2023_1_-_Nowe_Winogrady_Polnoc_Nowe_Winogrady_Poludnie_Nowe_Winogrady_Wschod_Stare_Winogrady.pb"),
      ]
      for task in [*election(f"{name}-seqav", f"{name}_seqav", data, f"{name}_seq.png"),
                   *election(f"{name}-av", f"{name}_av", data, f"{name}_av.png")]],
]
