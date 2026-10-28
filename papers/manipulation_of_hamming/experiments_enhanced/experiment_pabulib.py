import logging
from datetime import datetime
from pathlib import Path

import numpy as np

from papers.utils.pabulib import pabulib_to_votekit
from papers.utils.votekit_utils import sample_approval_profile
from ..manipulation_of_hamming import get_manipulability_ratio_oneprofile, orness, save_data
from . import RESULTS_DIRECTORY_PATH

DATA = Path(__file__).resolve().parent / "data"

DATASETS = [
  {
    "key": "lodz_wiskitno",
    "path": DATA / "Poland_Lodz_2020_Wiskitno.pb",
    "label": "Łódź Wiskitno (m=3)",
  },
  {
    "key": "gdynia_green",
    "path": DATA / "Poland_Gdynia_2021_Green_Budget.pb",
    "label": "Gdynia Green Budget (m=4)",
  },
  {
    "key": "warszawa_brodno",
    "path": DATA / "Poland_Warszawa_2026_Brodno-Podgrodzie_Zacisze.pb",
    "label": "Warszawa Bródno-Podgrodzie (m=5)",
  },
]

N_VOTERS = 25
N_ITERATIONS = 20000
SEED = 0
N_JOBS = -3


def sample_profiles(profile, n_voters, n_iterations, rng):
  return [sample_approval_profile(profile, n_voters, rng) for _ in range(n_iterations)]


def run_dataset(profile, label, n_voters=N_VOTERS, n_iterations=N_ITERATIONS, seed=SEED, n_jobs=N_JOBS, verbose=True):
  log_level = logging.INFO if verbose else logging.WARNING
  logging.basicConfig(level=log_level, format="%(message)s")
  candidates = list(profile.candidates)
  m = len(candidates)
  rng = np.random.default_rng(seed)
  logging.info(f"{label}: sampling {n_iterations} profiles of {n_voters} from {profile.num_ballots} voters")
  profiles = sample_profiles(profile, n_voters, n_iterations, rng)

  rows = []
  for fi in range(n_voters):
    ratio = get_manipulability_ratio_oneprofile(
      candidates, n_voters, ("f", fi), profiles, n_jobs=n_jobs
    )
    rows.append({
      "label": label,
      "m": m,
      "orness": orness(n_voters, fi),
      "manipulability": ratio,
    })
    logging.info(f"{label}: fi={fi}/{n_voters - 1} orness={rows[-1]['orness']:.3f} manip={ratio:.4f}")
  return rows


def run_experiment_pabulib(
  path=None,
  datasets=None,
  n_voters=N_VOTERS,
  n_iterations=N_ITERATIONS,
  seed=SEED,
  n_jobs=N_JOBS,
  verbose=True,
):
  path = Path(path) if path else RESULTS_DIRECTORY_PATH / "experiment_pabulib"
  datasets = datasets or DATASETS
  print(f"Starting experiment_pabulib | time: {datetime.now()}", flush=True)
  results = []
  for ds in datasets:
    profile = pabulib_to_votekit(ds["path"])
    results.extend(
      run_dataset(
        profile,
        ds["label"],
        n_voters=n_voters,
        n_iterations=n_iterations,
        seed=seed,
        n_jobs=n_jobs,
        verbose=verbose,
      )
    )
  save_data(path.with_suffix(".csv"), results)
  print(f"Completed experiment_pabulib | time: {datetime.now()}", flush=True)
  return path.with_suffix(".csv")


if __name__ == "__main__":
  run_experiment_pabulib()
