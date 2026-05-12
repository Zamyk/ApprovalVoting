from pathlib import Path

RESULTS_DIRECTORY_PATH = Path(__file__).resolve().parent / "results"
RESULTS_DIRECTORY_PATH.mkdir(exist_ok=True)

PLOTS_DIRECTORY_PATH = Path(__file__).resolve().parent / "plots"
PLOTS_DIRECTORY_PATH.mkdir(exist_ok=True)