"""Command-line entry point used by the manager (``papers/approval_with_runoff/tasks.py``).

The modules of this paper import each other by plain name (``import euclidean``), so they
cannot be started as ``python -m papers.approval_with_runoff.<module>``. This module puts its
own directory on ``sys.path`` first and then dispatches:

    python -m papers.approval_with_runoff.cli compute <name>
    python -m papers.approval_with_runoff.cli plot <name>

``compute`` names are the synthetic experiments in ``synthetic.EXPERIMENTS``. ``plot`` names
are those plus the real elections in ``elections.PLOT_NAMES``.
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import matplotlib

matplotlib.use("Agg")   # never open a window from a manager task

import elections
import synthetic


def main(argv):
    if len(argv) != 2 or argv[0] not in ("compute", "plot"):
        print(__doc__)
        return 2
    kind, name = argv
    names = synthetic.EXPERIMENTS if kind == "compute" else {**synthetic.EXPERIMENTS, **elections.PLOT_NAMES}
    if name not in names:
        print(f"unknown {kind} {name!r}; choose from: {', '.join(names)}")
        return 2
    if kind == "compute":
        print(f"compute {name}", flush=True)
        synthetic.compute(name)
    elif name in elections.PLOT_NAMES:
        print(elections.plot(name), flush=True)
    else:
        for out in synthetic.plot(name):
            print(out, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
