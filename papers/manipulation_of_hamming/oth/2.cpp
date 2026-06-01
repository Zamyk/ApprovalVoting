#include <iostream>
#include <vector>
#include <cmath>
#include <algorithm>
#include <numeric>
#include <iomanip>
#include <random>
#include <future>
#include <thread>

using namespace std;

// Calculates the Hamming distance between two binary vectors (as integers)
inline int hammingDistance(int x, int y) {
    return __builtin_popcount(x ^ y);
}

// Resolute Lexicographical Tie-Breaking as specified in the paper
inline bool prefersLexicographically(int outcomeA, int outcomeB) {
    return outcomeA > outcomeB; 
}

// OWA Winner Determination Engine
int getWinner(int m, const vector<int>& profile, const vector<int>& weights) {
    int num_voters = profile.size();
    int best_outcome = 0;
    int min_score = 1e9;
    int num_outcomes = 1 << m;

    for (int outcome = 0; outcome < num_outcomes; ++outcome) {
        vector<int> distances(num_voters);
        for (int i = 0; i < num_voters; ++i) {
            distances[i] = hammingDistance(outcome, profile[i]);
        }
        sort(distances.rbegin(), distances.rend()); 

        int score = 0;
        for (int i = 0; i < num_voters; ++i) {
            score += weights[i] * distances[i];
        }
        
        if (score < min_score) {
            min_score = score;
            best_outcome = outcome;
        } else if (score == min_score) {
            if (prefersLexicographically(outcome, best_outcome)) {
                best_outcome = outcome;
            }
        }
    }
    return best_outcome;
}

// Parameterization where i_zeros is the number of trailing zeros
pair<vector<double>, vector<int>> generateFiWeights(int n, int i_zeros) {
    vector<double> w(n, 0.0);
    int num_ones = n - i_zeros;
    for (int j = 0; j < num_ones; ++j) {
        w[j] = 1.0 / num_ones; 
    }

    vector<int> iw(n);
    for (int j = 0; j < num_ones; ++j) {
        iw[j] = 1; 
    }
    return {w, iw};
}

// Computes exact orness: \frac{1}{n-1} \sum_{j=1}^n \frac{n-j}{n-1} w_j
double calculateOrness(const vector<double>& w) {
    int n = w.size();
    if (n <= 1) return 0.5;
    double orness = 0;
    for (int j = 0; j < n; ++j) {
        orness += (double)(n - 1 - j) / (n - 1) * w[j];
    }
    return orness;
}

// Checks if any voter can successfully manipulate
bool isManipulable(int m, const vector<int>& profile, const vector<int>& weights) {
    int n = profile.size();
    int true_winner = getWinner(m, profile, weights);
    int num_outcomes = 1 << m;

    for (int i = 0; i < n; ++i) {
        int true_dist = hammingDistance(true_winner, profile[i]);

        for (int false_ballot = 0; false_ballot < num_outcomes; ++false_ballot) {
            if (false_ballot == profile[i]) continue;

            vector<int> modified_profile = profile;
            modified_profile[i] = false_ballot;

            int new_winner = getWinner(m, modified_profile, weights);
            int new_dist = hammingDistance(new_winner, profile[i]);

            if (new_dist < true_dist) {
                return true; 
            }
        }
    }
    return false;
}

// Worker function to handle a chunk of the election profiles in parallel
int countManipulableChunk(int m, const vector<vector<int>>& sampled_elections, 
                          const vector<int>& weights, int start_idx, int end_idx) {
    int local_count = 0;
    for (int e = start_idx; e < end_idx; ++e) {
        if (isManipulable(m, sampled_elections[e], weights)) {
            local_count++;
        }
    }
    return local_count;
}

int main() {
    int n = 25;                  // 25 Voters
    int num_elections = 10000;   // 10^4 iterations
    mt19937 rng(42);             

    // Detect hardware threads available
    unsigned int num_threads = thread::hardware_concurrency();
    if (num_threads == 0) num_threads = 4; // fallback

    cout << "m,orness,manipulability" << endl;
    cout << fixed << setprecision(6);

    for (int m : {3, 4, 5}) {
        int num_outcomes = 1 << m;
        uniform_int_distribution<int> dist(0, num_outcomes - 1);        

        // Sweeping i from 0 (Minisum) up to n-1 (Minimax)
        for (int i_zeros = 0; i_zeros <= n - 1; ++i_zeros) {
            vector<vector<int>> sampled_elections(num_elections, vector<int>(n));
            for (int e = 0; e < num_elections; ++e) {
                for (int i = 0; i < n; ++i) {
                    sampled_elections[e][i] = dist(rng);
                }
            }

            auto [weights, iweights] = generateFiWeights(n, i_zeros);            
            double orness = calculateOrness(weights);

            // Parallel distribution of the loop tasks
            vector<future<int>> futures;
            int chunk_size = num_elections / num_threads;

            for (unsigned int t = 0; t < num_threads; ++t) {
                int start_idx = t * chunk_size;
                // Ensure the last thread handles any remainder due to integer division
                int end_idx = (t == num_threads - 1) ? num_elections : (start_idx + chunk_size);

                futures.push_back(async(launch::async, countManipulableChunk, 
                                        m, ref(sampled_elections), ref(iweights), start_idx, end_idx));
            }

            // Gather and combine results from all async threads
            int total_manipulable_count = 0;
            for (auto& fut : futures) {
                total_manipulable_count += fut.get();
            }

            double ratio = (double)total_manipulable_count / num_elections;
            cout << m << "," << orness << "," << ratio << endl;
        }
    }

    return 0;
}