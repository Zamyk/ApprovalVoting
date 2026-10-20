import numpy as np


def approval_counts(profile):
  return np.asarray(profile, dtype=np.int32).sum(axis=0)


def coapprovals(profile, winner):
  with_winner = np.asarray(profile[profile[:, winner] == 1], dtype=np.int32).sum(axis=0)
  with_winner[winner] = 0
  return with_winner


def seq_components(profile):
  counts = approval_counts(profile)
  winner = int(np.argmax(counts))
  return winner, counts, coapprovals(profile, winner)


def seq_scores(counts, with_winner, alpha, winner):
  scores = counts.astype(float) - alpha * with_winner
  scores[winner] = -np.inf
  return scores


def alpha_seqAV(counts, with_winner, alpha):
  winner = int(np.argmax(counts))
  scores = seq_scores(counts, with_winner, alpha, winner)
  return winner, int(np.argmax(scores))

def S_Phr(counts, with_winner):
  winner = int(np.argmax(counts))
  scores = np.full(len(counts), np.inf)
  ok = np.flatnonzero((counts > 0) & (np.arange(len(counts)) != winner))
  scores[ok] = (1 + with_winner[ok] / counts[winner]) / counts[ok]
  return winner, int(np.argmin(scores))

def pair_intersections(profile):
  ballots = np.asarray(profile, dtype=np.float32)
  return ballots.T @ ballots


def pair_lines(profile, counts=None, both=None):
  if counts is None:
    counts = approval_counts(profile)
  if both is None:
    both = pair_intersections(profile)
  rows, cols = np.triu_indices(len(counts), k=1)
  intercept = counts[rows] + counts[cols]
  overlap = both[rows, cols]
  return rows, cols, intercept.astype(float), overlap.astype(float)


def alpha_AV(profile, alpha, counts=None, both=None):
  rows, cols, intercept, overlap = pair_lines(profile, counts, both)
  scores = intercept - alpha * overlap
  best = int(np.argmax(scores))
  return int(rows[best]), int(cols[best])


def pairs_winning_somewhere(intercept, overlap, eps=1e-6):
  breaks = [0.0, 1.0]
  for i in range(len(intercept)):
    for j in range(i + 1, len(intercept)):
      gap = overlap[j] - overlap[i]
      if abs(gap) <= eps:
        continue
      alpha = (intercept[j] - intercept[i]) / gap
      if 0 < alpha < 1:
        breaks.append(float(alpha))
  breaks = np.array(sorted(set(breaks)))
  samples = np.unique(np.concatenate([breaks, (breaks[:-1] + breaks[1:]) / 2]))
  winners = set()
  for alpha in samples:
    scores = intercept - alpha * overlap
    best = scores.max()
    winners.update(np.flatnonzero(scores >= best - eps).tolist())
  return sorted(winners)
