import random

def hamming_distance(c1, c2):
    return bin(c1 ^ c2).count('1')

def get_resolute_winner(votes, m):
    best_score = float('inf')
    winner = -1

    for committee in range((1 << m) - 1, -1, -1):
        score = max(hamming_distance(committee, v) for v in votes)
        if score < best_score:
            best_score = score
            winner = committee
    return winner

def is_manipulable(votes, m):
    sincere_winner = get_resolute_winner(votes, m)

    for voter_idx in range(len(votes)):
        true_pref = votes[voter_idx]
        sincere_dist = hamming_distance(sincere_winner, true_pref)

        for alt_ballot in range(1 << m):
            votes[voter_idx] = alt_ballot
            manip_winner = get_resolute_winner(votes, m)
            votes[voter_idx] = true_pref

            if hamming_distance(manip_winner, true_pref) < sincere_dist:
                return True
    return False

N_VOTERS = 25
TRIALS = 1000
M_CANDIDATES = [3, 4, 5]

print(f"Results for n={N_VOTERS} voters (100 trials per m):")
print("-" * 40)
print(f"{'Candidates (m)':<15} | {'Manipulability (%)':<15}")
print("-" * 40)

for m in M_CANDIDATES:
    manip_count = 0
    for _ in range(TRIALS):
        profile = [random.randint(0, (1 << m) - 1) for _ in range(N_VOTERS)]
        if is_manipulable(profile, m):
            manip_count += 1
    print(f"{m:<15} | {manip_count / (TRIALS / 100):>18}%")