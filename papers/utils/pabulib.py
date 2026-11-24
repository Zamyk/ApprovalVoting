from pathlib import Path
import numpy as np

from votekit.ballot import ApprovalBallot
from votekit.pref_profile.approval_profile import ApprovalProfile


def _split_sections(text):
  sections = {}
  current = None
  rows = []
  for raw in text.splitlines():
    line = raw.strip()
    if not line:
      continue
    key = line.upper()
    if key in {"META", "PROJECTS", "VOTES"}:
      if current is not None:
        sections[current] = rows
      current = key
      rows = []
      continue
    rows.append(line)
  if current is not None:
    sections[current] = rows
  return sections


def _parse_table(rows):
  header = [c.strip() for c in rows[0].split(";")]
  data = []
  for row in rows[1:]:
    parts = row.split(";")
    if len(parts) < len(header):
      parts = parts + [""] * (len(header) - len(parts))
    data.append({header[i]: parts[i].strip() for i in range(len(header))})
  return data


def load_pabulib(path):
  """Load a PaBuLib approval file as (ballots, codes, names).

  ballots: (n_voters, n_projects) int8 approval matrix
  codes: project ids as strings
  names: full project names aligned with codes
  """
  text = Path(path).read_text(encoding="utf-8")
  sections = _split_sections(text)
  projects = _parse_table(sections["PROJECTS"])
  votes = _parse_table(sections["VOTES"])

  codes = [p["project_id"] for p in projects]
  names = [p.get("name", codes[i]) for i, p in enumerate(projects)]
  index = {code: i for i, code in enumerate(codes)}

  ballots = np.zeros((len(votes), len(codes)), dtype=np.int8)
  for i, vote in enumerate(votes):
    approved = vote.get("vote", "").strip()
    if not approved:
      continue
    for token in approved.split(","):
      token = token.strip()
      if token in index:
        ballots[i, index[token]] = 1
  return ballots, codes, names


def pabulib_to_votekit(path):
  """Load a PaBuLib file and return a VoteKit ApprovalProfile."""
  ballots, codes, _names = load_pabulib(path)
  candidates = [str(c) for c in codes]
  vk_ballots = tuple(
    ApprovalBallot(approvals=[c for c, a in zip(candidates, row) if a])
    for row in ballots
  )
  return ApprovalProfile(ballots=vk_ballots, candidates=candidates)


def short_name(name, max_len=42):
  name = (name or "").strip()
  if len(name) <= max_len:
    return name
  return name[: max_len - 1].rstrip() + "…"
