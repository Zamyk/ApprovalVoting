"""Command-line entry point used by the manager (``papers/approval_with_runoff/tasks.py``).

The modules of this paper import each other by plain name (``import euclidean``), so they
cannot be started as ``python -m papers.approval_with_runoff.<module>``. This module puts its
own directory on ``sys.path`` first and then dispatches:

    python -m papers.approval_with_runoff.cli compute <name>
    python -m papers.approval_with_runoff.cli plot <name>

``compute`` names are the keys of ``COMPUTE``, ``plot`` names are the keys of ``PLOT``
(plot modules, matching the figure they write).
"""

import importlib
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import matplotlib

matplotlib.use("Agg")   # never open a window from a manager task


def _sample(generator_name, csv_module):
    def run():
        import euclidean, generators
        generator = getattr(generators, generator_name)
        kwargs = {"n_candidates": euclidean.N_CANDIDATES_2D} if "2d" in csv_module else {}
        euclidean.run_sample(generator, **kwargs).to_csv(_result(csv_module), index=False)
    return run


def _iterations(generator_name, csv_module):
    def run():
        import euclidean, generators
        generator = getattr(generators, generator_name)
        kwargs = {"n_candidates": euclidean.N_CANDIDATES_2D} if "2d" in csv_module else {}
        euclidean.run_iterations(generator, **kwargs).to_csv(_result(csv_module), index=False)
    return run


def _av(generator_name, winner_module, second_module):
    def run():
        import euclidean, generators
        winner, second = euclidean.run_av_iterations(getattr(generators, generator_name))
        winner.to_csv(_result(winner_module), index=False)
        second.to_csv(_result(second_module), index=False)
    return run


def _result(module_name):
    return importlib.import_module(module_name).RESULT


COMPUTE = {
    "triangle": _sample("generate_profile_triangular", "plot_triangle"),
    "gaussian": _sample("generate_profile_gaussian", "plot_gaussian"),
    "triangle_iterations": _iterations("generate_profile_triangular", "plot_triangle_iterations"),
    "gaussian_iterations": _iterations("generate_profile_gaussian", "plot_gaussian_iterations"),
    "triangle_av": _av("generate_profile_triangular", "plot_triangle_av_winner", "plot_triangle_av_second"),
    "gaussian_av": _av("generate_profile_gaussian", "plot_gaussian_av_winner", "plot_gaussian_av_second"),
    "triangular2d": _sample("generate_profile_triangular_2d", "plot_triangular2d"),
    "cone2d": _sample("generate_profile_cone_2d", "plot_cone2d"),
    "gaussian2d": _sample("generate_profile_gaussian_2d", "plot_gaussian2d"),
    "triangular2d_iterations": _iterations("generate_profile_triangular_2d", "plot_triangular2d_iterations"),
    "cone2d_iterations": _iterations("generate_profile_cone_2d", "plot_cone2d_iterations"),
    "gaussian2d_iterations": _iterations("generate_profile_gaussian_2d", "plot_gaussian2d_iterations"),
}

# plot name -> modules whose `plot(show=False)` write the figure(s)
PLOT = {
    **{name: (f"plot_{name}",) for name in [
        "triangle", "gaussian", "triangle_iterations", "gaussian_iterations",
        "triangular2d", "cone2d", "gaussian2d",
        "triangular2d_iterations", "cone2d_iterations", "gaussian2d_iterations",
    ]},
    "triangle_av": ("plot_triangle_av_winner", "plot_triangle_av_second"),
    "gaussian_av": ("plot_gaussian_av_winner", "plot_gaussian_av_second"),
    "grenoble_seqav": ("grenoble_seqav",), "grenoble_av": ("grenoble_av",),
    "warszawa_seqav": ("warszawa_seqav",), "warszawa_av": ("warszawa_av",),
}

# computed inside the plot task: each takes seconds (slow ones are separate manager run tasks)
FAST = {"triangle", "gaussian", "triangle_iterations", "gaussian_iterations",
        "triangular2d", "cone2d", "gaussian2d"}


def main(argv):
    if len(argv) != 2 or argv[0] not in ("compute", "plot"):
        print(__doc__)
        return 2
    kind, name = argv
    table = COMPUTE if kind == "compute" else PLOT
    if name not in table:
        print(f"unknown {kind} {name!r}; choose from: {', '.join(table)}")
        return 2
    if kind == "compute":
        print(f"compute {name}", flush=True)
        table[name]()
    else:
        if name in FAST:   # cheap enough to recompute on every plot, no CSV step in the manager
            COMPUTE[name]()
        for module in table[name]:
            print(importlib.import_module(module).plot(show=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
