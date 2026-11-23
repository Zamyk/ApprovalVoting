"""Registry of the real-election experiments (French 2017 approval experiments, PaBuLib).

Each election gets two plots, both from the shipped data file (no run step):

* ``<name>_seqav``: score of every candidate for the second place under alpha-seqAV,
  written to ``plots/<name>_seq.png``.
* ``<name>_av``: score of the pairs under alpha-AV, written to ``plots/<name>_av.png``.

``cli.py`` dispatches on these names and ``tasks.py`` builds the manager tasks from them.
"""

from pathlib import Path

from approval_with_runoff import seq_components
from french_elections import load_election
from papers.utils.pabulib import load_pabulib, short_name
from plot_election import plot_av_pairs, plot_seq_scores

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
PLOTS = HERE / "plots"


def _french(path):
  ballots, codes = load_election(path)
  return ballots, codes, codes


def _pabulib(path, seq_len=42, av_len=28):
  ballots, codes, names = load_pabulib(path)
  return ballots, [short_name(n, seq_len) for n in names], [short_name(n, av_len) for n in names]


# name -> data file, title, loader, seqAV options, AV options
# seq ``top_n``: plot only the top_n candidates by approvals (None = all).
# av ``top_n``: pairs with the highest score at alpha = 0.5; ``win_scan``: how many of the best
# pairs are searched for pairs selected at some alpha (None = all); ``min_annotated``: label at
# least this many pairs.
ELECTIONS = {
    "grenoble": dict(file="GrenobleData_2017_Presid+.csv", title="Grenoble 2017", load=_french,
                     seq={}, av=dict(top_n=10)),
    "warszawa": dict(file="Poland_Warszawa_2023.pb", title="Warszawa 2023", load=_pabulib,
                     seq=dict(top_n=12), av=dict(top_n=10, win_scan=40, min_annotated=6)),
    "gdynia": dict(file="Poland_Gdynia_2024.pb", title="Gdynia 2024", load=_pabulib,
                   seq=dict(top_n=12), av=dict(top_n=10, min_annotated=6)),
    "lodz": dict(file="Poland_Lodz_2026.pb", title="Łódź 2026", load=_pabulib,
                 seq=dict(top_n=12), av=dict(top_n=10, win_scan=40, min_annotated=6)),
    "poznan": dict(file="Poland_Poznan_2023_1_-_Nowe_Winogrady_Polnoc_Nowe_Winogrady_Poludnie_Nowe_Winogrady_Wschod_Stare_Winogrady.pb",
                   title="Poznań 2023 (district 1, Winogrady)", load=_pabulib,
                   seq=dict(top_n=12), av=dict(top_n=10, min_annotated=6)),
}

PLOT_NAMES = {f"{name}_{rule}": (name, rule) for name in ELECTIONS for rule in ("seqav", "av")}


def figure(name, rule):
  return PLOTS / f"{name}_{'seq' if rule == 'seqav' else 'av'}.png"


def plot(plot_name, show=False):
  name, rule = PLOT_NAMES[plot_name]
  election = ELECTIONS[name]
  ballots, seq_labels, av_labels = election["load"](DATA / election["file"])
  if rule == "seqav":
    top_n = election["seq"].get("top_n")
    winner, _, _ = seq_components(ballots)
    shown = "" if top_n is None else f", top {top_n} by approvals"
    title = f"{election['title']}, second-place score (winner: {seq_labels[winner]}{shown})"
    return plot_seq_scores(ballots, seq_labels, title, figure(name, rule), show=show, top_n=top_n)
  options = election["av"]
  title = f"{election['title']}, pair score ({options['top_n']} highest average)"
  return plot_av_pairs(ballots, av_labels, title, figure(name, rule), show=show, **options)
