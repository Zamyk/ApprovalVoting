from pathlib import Path

RESULTS_DIRECTORY_PATH = Path(__file__).resolve().parent / "results"
RESULTS_DIRECTORY_PATH.mkdir(exist_ok=True)

PLOTS_DIRECTORY_PATH = Path(__file__).resolve().parent / "plots"
PLOTS_DIRECTORY_PATH.mkdir(exist_ok=True)
# (p, phi)-resampling experiments: p and (file tag, phi) pairs, shared by runs, plots and tasks.py.
# No dots in the tag: Path.with_suffix would treat ".25" as an extension.
RESAMPLING_P = 0.5
RESAMPLING_PHIS = [("phi025", 0.25), ("phi05", 0.5), ("phi075", 0.75)]
