import itertools

from generators import approval_ic_profile_generator
from rules import OrderedWeightedHamming

voters = 25

def get_orness(election):
    n = len(election.weights)
    answer = 0

    for i, w in enumerate(election.weights):
        answer += w * (n - (i + 1))

    return answer / (n - 1)

def can_voter_manipulate(i, profile, weights):
    candidates = profile.candidates

    scores = profile.df.drop(columns=['Weight', 'Voter Set']).fillna(0)

    elected = set((OrderedWeightedHamming(profile=profile, weights=weights).get_elected() or (set(),))[0])

    def get_dist(preference, result):
        pref_set = {c for c, v in preference.items() if bool(v)}
        result_set = set(result)
        return len(pref_set.symmetric_difference(result_set))

    true_dist = get_dist(scores.iloc[i], elected)

    for k in range(len(candidates) + 1):
        for vote in itertools.combinations(candidates, k):
            manipulated_profile = profile.change_vote(i, vote)
            elected = set((OrderedWeightedHamming(profile=manipulated_profile, weights=weights).get_elected() or (set(),))[0])
            dist = get_dist(scores.iloc[i], elected)
            if dist < true_dist:
                return True
    return False

def get_manipulability_ratio(profile, weights):
    for i in range(voters):
        if can_voter_manipulate(i, profile, weights):
            return 1
    return 0


ans = 0
for i in range(100):
    profile = approval_ic_profile_generator(["A", "B", "C", "D"], voters)
    ans += get_manipulability_ratio(profile, weights="minimax")

print(ans / 100)