from . import RESULTS_DIRECTORY_PATH
from .experiment_pabulib import N_JOBS, SEED, run_experiment_pabulib

N_VOTERS = 100
N_ITERATIONS = 20000


def run_experiment_pabulib_100(
  path=None, n_voters=N_VOTERS, n_iterations=N_ITERATIONS, seed=SEED, n_jobs=N_JOBS, verbose=True
):
  """Same as experiment_pabulib, but each profile is 100 voters sampled uniformly
  (without replacement) from the full pabulib election."""
  path = path or RESULTS_DIRECTORY_PATH / f"experiment_pabulib_integers_oneprofile_n{n_voters}"
  return run_experiment_pabulib(
    path=path,
    n_voters=n_voters,
    n_iterations=n_iterations,
    seed=seed,
    n_jobs=n_jobs,
    verbose=verbose,
  )


if __name__ == "__main__":
  run_experiment_pabulib_100()
