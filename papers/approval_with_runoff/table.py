from approval_with_runoff import S_Phr, alpha_AV, alpha_seqAV, seq_components
from french_elections import ELECTIONS, load_election
from posters import POSTERS, load_poster


def mav(profile):
    _, counts, with_winner = seq_components(profile)
    return alpha_seqAV(counts, with_winner, 0)


def ccav(profile):
    return alpha_AV(profile, 1)


def sccav(profile):
    _, counts, with_winner = seq_components(profile)
    return alpha_seqAV(counts, with_winner, 1)


def pav(profile):
    return alpha_AV(profile, 0.5)


def spav(profile):
    _, counts, with_winner = seq_components(profile)
    return alpha_seqAV(counts, with_winner, 0.5)


def sphr(profile):
    _, counts, with_winner = seq_components(profile)
    return S_Phr(counts, with_winner)


RULES = [
    ("MAV", mav),
    ("CCAV", ccav),
    ("S-CCAV", sccav),
    ("PAV", pav),
    ("S-PAV", spav),
    ("S-Phr", sphr),
]

LABELS = {
    "strasbourg": "2017-Strasbourg",
    "grenoble": "2017-Grenoble",
    "hsc": "2017-HSC",
    "crolles": "2017-Crolles",
}


def table(names, profiles, codes, rules):
    columns = "c" * len(rules)
    print(r"\begin{tabular}{|l|" + columns + "|}")
    print(r"\hline")
    print("Rule & " + " & ".join(label for label, _ in rules) + r" \\")
    print(r"\hline")
    for name, profile, code in zip(names, profiles, codes):
        cells = [LABELS.get(name, name)]
        for _, rule in rules:
            first, second = rule(profile)
            cells.append(f"{code[first]}/{code[second]}")
        print(" & ".join(cells) + r" \\")
        print(r"\hline")
    print(r"\end{tabular}")


POSTER_LABELS = {
    "a": "Best-Poster-A",
    "b": "Best-Poster-B",
}


def table2(names, profiles, codes, rules):
    columns = "c" * len(rules)
    print(r"\begin{tabular}{|l|" + columns + "|}")
    print(r"\hline")
    print("Rule & " + " & ".join(label for label, _ in rules) + r" \\")
    print(r"\hline")
    for name, profile, _code in zip(names, profiles, codes):
        cells = [POSTER_LABELS.get(name, name)]
        for _, rule in rules:
            first, second = rule(profile)
            cells.append(f"\\#{first + 1}/\\#{second + 1}")
        print(" & ".join(cells) + r" \\")
        print(r"\hline")
    print(r"\end{tabular}")


if __name__ == "__main__":
    names = []
    profiles = []
    codes = []
    for name in LABELS:
        profile, code = load_election(ELECTIONS[name])
        names.append(name)
        profiles.append(profile)
        codes.append(code)
    table(names, profiles, codes, RULES)

    names = []
    profiles = []
    codes = []
    for name in POSTER_LABELS:
        profile, code = load_poster(POSTERS[name])
        names.append(name)
        profiles.append(profile)
        codes.append(code)
    print()
    table2(names, profiles, codes, RULES)
