import random
import pandas as pd

def hamming_distance(c1, c2):
    return bin(c1 ^ c2).count('1')

def get_score(votes, committee, weights):
    distances = sorted([hamming_distance(vote, committee) for vote in votes], reverse=True)
    ans = 0
    for i in range(len(distances)):
        ans += weights[i] * distances[i]
    return ans

def get_resolute_winner(votes, m, weights):
    best_score = float('inf')
    winner = -1

    for committee in range((1 << m) - 1, -1, -1):
        score = get_score(votes, committee, weights)
        if score < best_score:
            best_score = score
            winner = committee
    return winner

def is_manipulable(votes, m, fi):
    weights = [1 / (len(votes) - fi)] * (len(votes) - fi) + [0] * fi

    sincere_winner = get_resolute_winner(votes, m, weights)

    for voter_idx in range(len(votes)):
        true_pref = votes[voter_idx]
        sincere_dist = hamming_distance(sincere_winner, true_pref)

        for alt_ballot in range(1 << m):
            votes[voter_idx] = alt_ballot
            manip_winner = get_resolute_winner(votes, m, weights)
            votes[voter_idx] = true_pref

            if hamming_distance(manip_winner, true_pref) < sincere_dist:
                return True
    return False

def orness(n, fi):
    return (n + fi - 1) / (2 * (n - 1))

def random_profile(n, m):
    return [random.randint(0, (1 << m) - 1) for _ in range(n)]

def biased_profile(n, m):
    p1s = [random.uniform(0, 1) for _ in range(m)]
    p2s = [random.uniform(0, 1) for _ in range(m)]
    p3s = [0.5 for _ in range(m)]

    n1 = (int)(n * 0.4)
    n2 = (int)(n * 0.4)
    n3 = n - n1 - n2

    def biased_vote(ps):
        ans = 0
        for p in ps:
            ans *= 2
            if random.uniform(0, 1) <= p:
                ans += 1            
        return ans

    return [biased_vote(p1s) for _ in range(n1)] + [biased_vote(p2s) for _ in range(n2)] + [biased_vote(p3s) for _ in range(n3)]

def save_data(path, data):
    df = pd.DataFrame(data)
    df.to_csv(path, index=False)

def tests(path, n_voters, trials, m_candidates, gen):
    results = []
    for m in m_candidates:
        for fi in range(n_voters):
            manip_count = 0
            for _ in range(trials):
                profile = gen(n_voters, m)
                if is_manipulable(profile, m, fi):
                    manip_count += 1

            results.append({
                'm': m,
                'orness': orness(n_voters, fi),
                'manipulability': manip_count / trials
            })
        print(f"Completed calculations for m={m}")
    save_data(path, results)

TRIALS = 100
#tests("uniform.csv", 25, TRIALS, [3, 4, 5], gen=random_profile)
tests("biased.csv", 25, TRIALS, [3, 4, 5], gen=biased_profile)