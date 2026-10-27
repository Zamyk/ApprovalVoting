from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

from approval_with_runoff import pair_lines, pairs_winning_somewhere, seq_components


def _save(fig_path, show):
  out = Path(fig_path)
  out.parent.mkdir(parents=True, exist_ok=True)
  plt.tight_layout()
  plt.savefig(out, dpi=150, bbox_inches="tight")
  if show:
    plt.show()
  else:
    plt.close()
  return out


def plot_seq_scores(ballots, labels, title, save, show=True, top_n=None):
  winner, counts, with_winner = seq_components(ballots)
  alphas = np.linspace(0, 1, 200)
  if top_n is None:
    keep = {i for i in range(len(labels)) if i != winner}
  else:
    keep = set([int(i) for i in np.argsort(-counts) if i != winner][:top_n])

  plt.figure(figsize=(8, 4.5))
  for i in range(len(labels)):
    if i == winner or i not in keep:
      continue
    plt.plot(alphas, counts[i] - alphas * with_winner[i], label=labels[i])

  plt.axvline(x=0.5, color="black", linestyle="--", label="S-PAV")
  plt.title(title)
  plt.xlabel(r"$\alpha$")
  plt.ylabel(r"$S(c) - \alpha S(winner \cap c)$")
  plt.xlim(0, 1)
  plt.legend(loc="center left", bbox_to_anchor=(1.02, 0.5), fontsize=8)
  plt.grid(False)
  return _save(save, show)


def plot_av_pairs(
  ballots,
  labels,
  title,
  save,
  show=True,
  top_n=10,
  win_scan=None,
  min_annotated=0,
):
  rows, cols, intercept, overlap = pair_lines(ballots)
  average = intercept - 0.5 * overlap
  ranked = np.argsort(-average)
  keep = set(ranked[:top_n].tolist())
  if win_scan is None:
    winners = set(pairs_winning_somewhere(intercept, overlap)) & keep
  else:
    scan = ranked[: max(top_n, win_scan)]
    winners = set(pairs_winning_somewhere(intercept[scan], overlap[scan]))
    winners = {int(scan[i]) for i in winners} & keep

  annotated = set(winners)
  if min_annotated > 0:
    for k in ranked:
      if len(annotated) >= min_annotated:
        break
      if int(k) in keep:
        annotated.add(int(k))

  alphas = np.linspace(0, 1, 200)
  plt.figure(figsize=(8, 4.5))
  for k in sorted(keep - annotated):
    plt.plot(alphas, intercept[k] - alphas * overlap[k], color="0.75", linewidth=0.8, zorder=1)
  for k in sorted(annotated):
    label = f"{labels[rows[k]]}/{labels[cols[k]]}"
    plt.plot(alphas, intercept[k] - alphas * overlap[k], label=label, zorder=2)

  plt.axvline(x=0.5, color="black", linestyle="--", label="PAV")
  plt.title(title)
  plt.xlabel(r"$\alpha$")
  plt.ylabel(r"$S(i)+S(j)-\alpha S(i \cap j)$")
  plt.xlim(0, 1)
  plt.legend(loc="center left", bbox_to_anchor=(1.02, 0.5), fontsize=8)
  plt.grid(False)
  return _save(save, show)
