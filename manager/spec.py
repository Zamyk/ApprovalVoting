"""What a manifest declares and how the manager finds manifests.

A paper describes its experiments in ``papers/<paper>/tasks.py`` by exposing a
list ``TASKS`` (built with :func:`experiment`). Optional ``TITLE`` and
``FAMILY_TITLES`` give nicer names in the tree. The manager never imports the
experiment code itself, it only runs it as ``python -m <module>``.
"""

import importlib.util
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class Task:
    id: str                    # "<paper>/<family>/<variant>:<kind>", used by selectors
    kind: str                  # "run" or "plot"
    paper: str
    family: str
    variant: str
    module: str                # executed as ``python -m <module>`` from the repo root
    reads: tuple = ()          # glob patterns (relative to the repo root) the task needs
    writes: tuple = ()         # glob patterns the task produces
    args: tuple = ()
    note: str = ""             # shown in the details panel
    broken: str = ""           # reason; such a task is not ticked by "all" / group ticks


def experiment(paper, family, variant, *, run, plot, data, figures, note="", broken="",
               run_args=(), plot_args=()):
    """One experiment: a run task writing ``data`` and a plot task reading it."""
    base = f"{paper}/{family}/{variant}"
    return [
        Task(f"{base}:run", "run", paper, family, variant, run,
             writes=tuple(data), args=tuple(run_args), note=note, broken=broken),
        Task(f"{base}:plot", "plot", paper, family, variant, plot,
             reads=tuple(data), writes=tuple(figures), args=tuple(plot_args), broken=broken),
    ]


@dataclass
class Registry:
    tasks: list = field(default_factory=list)
    paper_titles: dict = field(default_factory=dict)
    family_titles: dict = field(default_factory=dict)   # (paper, family) -> title


def load_registry(papers_dirs=None):
    """Load every ``<dir>/*/tasks.py`` manifest (default: ``<repo>/papers``)."""
    dirs = [Path(d) for d in papers_dirs] if papers_dirs else [ROOT / "papers"]
    registry = Registry()
    seen = set()
    for directory in dirs:
        for manifest in sorted(directory.glob("*/tasks.py")):
            spec = importlib.util.spec_from_file_location(f"_manifest_{manifest.parent.name}", manifest)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            for task in module.TASKS:
                if task.id in seen:
                    raise ValueError(f"duplicate task id {task.id!r} in {manifest}")
                seen.add(task.id)
                registry.tasks.append(task)
            if hasattr(module, "TITLE"):
                registry.paper_titles[manifest.parent.name] = module.TITLE
            for family, title in getattr(module, "FAMILY_TITLES", {}).items():
                registry.family_titles[(manifest.parent.name, family)] = title
    return registry
