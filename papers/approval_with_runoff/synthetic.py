"""Registry of the synthetic Euclidean experiments: what each one computes and plots.

Each experiment has a ``kind``:

* ``sample``: one set of positions, a profile per ``d``. Distance between the two seqAV finalists.
* ``iterations``: ``N_REPS`` position draws. Same quantity, min/max/mean.
* ``av``: ``N_REPS`` position draws. Distance of the first and of the second alpha-AV
  finalist from the AV winner (two outputs).

Every output is ``(result CSV, figure, title)``. ``cli.py`` dispatches on the experiment
names and ``tasks.py`` builds the manager tasks from the same table.
"""

from pathlib import Path

import euclidean
import generators as g
from plot_seq import plot_curves

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
PLOTS = HERE / "plots"

# candidates drawn from the same distribution as the voters
TRIANGLE = g.position_generator(g.triangular_1d)
GAUSSIAN = g.position_generator(g.gaussian_1d)

# 2D voter models: name -> (voter distribution, title)
MODELS_2D = {
    "triangular2d": (g.triangular_2d, "2D product-triangular"),
    "cone2d": (g.cone_2d, "2D radial cone"),
    "gaussian2d": (g.gaussian_2d, "2D Gaussian"),
}
# 2D candidate variants: suffix -> (candidate distribution or None for "same as voters", title)
CANDIDATES_2D = {
    "unif": (g.uniform_2d, "candidates uniform"),
    "same": (None, "candidates ~ voters"),
}


def _out(stem, figure, title):
  return (RESULTS / f"results_{stem}.csv", PLOTS / figure, title)


EXPERIMENTS = {
    "triangle": dict(kind="sample", generator=TRIANGLE, outputs=[
        _out("triangle", "triangle_seq_original.png",
             "Distance between finalists, triangular (candidates ~ voters, one sample)")]),
    "gaussian": dict(kind="sample", generator=GAUSSIAN, outputs=[
        _out("gaussian", "gaussian_seq_original.png",
             "Distance between finalists, Gaussian (candidates ~ voters, one sample)")]),
    "triangle_iterations": dict(kind="iterations", generator=TRIANGLE, outputs=[
        _out("triangle_iterations", "triangle_seq_iterations.png",
             "Distance between finalists, triangular (candidates ~ voters, min-max over iterations)")]),
    "gaussian_iterations": dict(kind="iterations", generator=GAUSSIAN, outputs=[
        _out("gaussian_iterations", "gaussian_seq_iterations.png",
             "Distance between finalists, Gaussian (candidates ~ voters, min-max over iterations)")]),
    "triangle_av": dict(kind="av", generator=TRIANGLE, outputs=[
        _out("triangle_av_winner", "triangle_av_winner_iterations.png",
             "AV first finalist, triangular (candidates ~ voters, min-max over iterations)"),
        _out("triangle_av_second", "triangle_av_second_iterations.png",
             "AV second finalist, triangular (candidates ~ voters, min-max over iterations)")]),
    "gaussian_av": dict(kind="av", generator=GAUSSIAN, outputs=[
        _out("gaussian_av_winner", "gaussian_av_winner_iterations.png",
             "AV first finalist, Gaussian (candidates ~ voters, min-max over iterations)"),
        _out("gaussian_av_second", "gaussian_av_second_iterations.png",
             "AV second finalist, Gaussian (candidates ~ voters, min-max over iterations)")]),
}

for model, (voter_dist, model_title) in MODELS_2D.items():
  for suffix, (candidate_dist, cand_title) in CANDIDATES_2D.items():
    name = f"{model}_{suffix}"
    generator = g.position_generator(voter_dist, candidate_dist)
    common = dict(generator=generator, n_candidates=euclidean.N_CANDIDATES_2D)
    EXPERIMENTS[name] = dict(kind="sample", **common, outputs=[
        _out(name, f"{name}_seq.png", f"Distance between finalists, {model_title} ({cand_title}, one sample)")])
    EXPERIMENTS[f"{name}_iterations"] = dict(kind="iterations", **common, outputs=[
        _out(f"{name}_iterations", f"{name}_seq_iterations.png",
             f"Distance between finalists, {model_title} ({cand_title}, min-max over iterations)")])

RULE_LABEL = {"sample": "S-PAV", "iterations": "S-PAV", "av": "PAV"}
# Every synthetic plot measures from the AV winner (the candidate with the most approvals).
# seqAV: the AV winner is always the first finalist, so this is the distance between finalists.
# AV: both finalists move with alpha, so each one's distance from the AV winner is plotted.
YLABEL = {"sample": "distance between finalists", "iterations": "distance between finalists",
          "av": "distance from AV winner"}
RUNNERS = {
    "sample": lambda gen, **kw: [euclidean.run_sample(gen, **kw)],
    "iterations": lambda gen, **kw: [euclidean.run_iterations(gen, **kw)],
    "av": lambda gen, **kw: list(euclidean.run_av_iterations(gen, **kw)),
}


def compute(name):
  exp = EXPERIMENTS[name]
  kwargs = {"n_candidates": exp["n_candidates"]} if "n_candidates" in exp else {}
  frames = RUNNERS[exp["kind"]](exp["generator"], **kwargs)
  for frame, (result, _, _) in zip(frames, exp["outputs"]):
    result.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(result, index=False)


def plot(name, show=False):
  exp = EXPERIMENTS[name]
  return [
      plot_curves(result, figure, title, show=show,
                  rule_label=RULE_LABEL[exp["kind"]], ylabel=YLABEL[exp["kind"]])
      for result, figure, title in exp["outputs"]
  ]
