"""Is the data there, is the plot there, is the plot older than its data."""

import time
from dataclasses import dataclass

from .spec import ROOT


def matches(pattern):
    return sorted(ROOT.glob(pattern))


def newest(patterns):
    times = [p.stat().st_mtime for pat in patterns for p in matches(pat)]
    return max(times) if times else None


def oldest(patterns):
    times = [p.stat().st_mtime for pat in patterns for p in matches(pat)]
    return min(times) if times else None


def age(timestamp):
    seconds = max(0, time.time() - timestamp)
    if seconds < 60:
        return f"{int(seconds)}s"
    if seconds < 3600:
        return f"{int(seconds // 60)}m"
    if seconds < 86400:
        return f"{int(seconds // 3600)}h"
    return f"{int(seconds // 86400)}d"


@dataclass(frozen=True)
class Status:
    state: str          # done | missing | partial | blocked | ready | stale
    text: str
    needs_work: bool    # worth ticking with "needs work"


def task_status(task):
    if task.kind == "run":
        found = [bool(matches(p)) for p in task.writes]
        if not any(found):
            return Status("missing", "no data", True)
        if not all(found):
            return Status("partial", f"partial data ({sum(found)}/{len(found)})", True)
        return Status("done", f"data {age(newest(task.writes))} old", False)

    if not all(matches(p) for p in task.reads):
        return Status("blocked", "needs data first", False)
    if not all(matches(p) for p in task.writes):
        return Status("ready", "not plotted yet", True)
    if newest(task.reads) > oldest(task.writes):
        return Status("stale", "plot older than data", True)
    return Status("done", f"plotted {age(oldest(task.writes))} ago", False)
