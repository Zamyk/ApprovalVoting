import numpy as np
from votekit.pref_profile.approval_profile import ApprovalProfile
from votekit.elections.election_types.approval.hamming import OrderedWeightedHamming
from votekit.ballot_generator.std_generator.approval_impartial_culture import approval_ic_profile_generator
from votekit.ballot import ApprovalBallot

def get_orness(weights):
    n = len(weights)
    if n <= 1:
        return 0
    answer = 0
    for i, w in enumerate(weights):
        answer += w * (n - (i + 1))
    return answer / (n - 1)

def get_elected_committee(profile, weights_type="minisum"):
    election = OrderedWeightedHamming(profile=profile, weights=weights_type)
    elected_tuple = election.get_elected()
    if not elected_tuple:
        return np.array([0 for c in profile.candidates])

    return np.array([c in elected_tuple[0] for c in profile.candidates])

def get_hamming_dist(ballot_vec, committee):
    return np.sum(ballot_vec != committee)

def can_voter_manipulate(voter_idx, profile, weights_type="minimax"):
    candidates = profile.candidates
    n_cands = len(candidates)
    
    preference = profile.votes[voter_idx].copy()
    
    true_elected = get_elected_committee(profile, weights_type)
    true_dist = get_hamming_dist(preference, true_elected)    
    
    for mask in range(1 << n_cands):
        new_vote_vec = np.array([(mask >> i) & 1 for i in range(n_cands)], dtype=bool)        
            
        profile.votes[voter_idx] = new_vote_vec
        manipulated_elected = get_elected_committee(profile, weights_type)
        dist = get_hamming_dist(preference, manipulated_elected)
        profile.votes[voter_idx] = preference.copy()
        
        if dist < true_dist:
            return True
            
    return False

def get_manipulability_ratio(candidates, n_voters, weights_type="minimax", n_iterations=100):
    manipulable_count = 0
    for _ in range(n_iterations):
        profile = approval_ic_profile_generator(candidates, n_voters)
        
        is_manipulable = False
        for i in range(n_voters):
            if can_voter_manipulate(i, profile, weights_type):
                is_manipulable = True
                break
        
        if is_manipulable:
            manipulable_count += 1
            
    return manipulable_count / n_iterations

if __name__ == "__main__":
    candidates = ["A", "B", "C"]
    n_voters = 25
    
    print(f"Running experiments with {len(candidates)} candidates and {n_voters} voters...")
    
    for fi in range(n_voters):        
        ratio = get_manipulability_ratio(candidates, n_voters, weights_type=("f", fi), n_iterations=100)
        print(f"Manipulability ratio for {fi}: {ratio:.4f}")