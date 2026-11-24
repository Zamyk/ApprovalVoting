from pathlib import Path
import numpy as np

DATA = Path(__file__).resolve().parent / "data"

POSTERS = {
    "a": DATA / "00033-00000002.cat",
    "b": DATA / "00033-00000003.cat",
}


def load_poster(path):
    n_alternatives = None
    codes = []
    ballots = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line.startswith("# NUMBER ALTERNATIVES:"):
                n_alternatives = int(line.split(":")[1])
                codes = [str(i) for i in range(1, n_alternatives + 1)]
                continue
            if line.startswith("# ALTERNATIVE NAME"):
                left, name = line.split(":", 1)
                index = int(left.rsplit(" ", 1)[-1])
                codes[index - 1] = name.strip()
                continue
            if not line or line.startswith("#"):
                continue
            count, groups = line.split(":", 1)
            approved = groups.split("},{")[0].replace("{", "").replace("}", "")
            ballot = np.zeros(n_alternatives, dtype=int)
            if approved.strip():
                for candidate in approved.split(","):
                    ballot[int(candidate) - 1] = 1
            ballots.extend([ballot] * int(count))
    return np.vstack(ballots), codes
