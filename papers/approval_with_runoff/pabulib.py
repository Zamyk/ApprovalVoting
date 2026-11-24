from pathlib import Path

from papers.utils.pabulib import load_pabulib, short_name

DATA = Path(__file__).resolve().parent / "data"

INSTANCES = {
    "warszawa_2023": DATA / "Poland_Warszawa_2023.pb",
}


def load_instance(name):
  return load_pabulib(INSTANCES[name])
