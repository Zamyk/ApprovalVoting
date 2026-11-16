"""Run ticked tasks one after another, each in its own process.

Why a process per task: several experiments patch shared code at import time
(integer Hamming weights, the "new manipulation" function). Running them in one
interpreter would let one experiment silently change another.

All runs go first, then all plots, so a plot never reads data from before the
run it was ticked together with. A plot is skipped if its data is missing or
its run failed (so it can't quietly use old data).
"""

import fnmatch
import os
import subprocess
import sys
import time
from datetime import datetime

from rich.console import Console
from rich.markup import escape
from rich.table import Table

from .spec import ROOT
from .status import matches


def select(tasks, patterns, kind=None):
    """Tasks whose id matches a glob, or lies under a prefix like ``paper/family``."""
    chosen = []
    for task in tasks:
        if kind and task.kind != kind:
            continue
        if any(fnmatch.fnmatch(task.id, p) or task.id.startswith(p.rstrip("/") + "/") for p in patterns):
            chosen.append(task)
    return chosen


def plan_order(tasks, registry_order):
    """Runs first, then plots, each in manifest order."""
    ordered = sorted(tasks, key=lambda t: registry_order[t.id])
    return [t for t in ordered if t.kind == "run"] + [t for t in ordered if t.kind == "plot"]


def fmt_duration(seconds):
    seconds = int(seconds)
    hours, rest = divmod(seconds, 3600)
    minutes, secs = divmod(rest, 60)
    if hours:
        return f"{hours}h{minutes:02d}m"
    if minutes:
        return f"{minutes}m{secs:02d}s"
    return f"{secs}s"


def print_plan(plan, console):
    table = Table(title=f"{len(plan)} task(s), in this order", show_header=True, header_style="bold")
    table.add_column("#", justify="right")
    table.add_column("kind")
    table.add_column("task")
    table.add_column("module", style="dim")
    for i, task in enumerate(plan, 1):
        table.add_row(str(i), task.kind, task.id, task.module)
    console.print(table)


def _command(task):
    return [sys.executable, "-m", task.module, *task.args]


# subprocess.BELOW_NORMAL_PRIORITY_CLASS only exists on Windows
BELOW_NORMAL_PRIORITY_CLASS = getattr(subprocess, "BELOW_NORMAL_PRIORITY_CLASS", 0x00004000)


def _priority_options(nice):
    """Popen keyword arguments that lower the priority of a task (and of the workers it starts).

    Unix: ``nice`` is the nice level. Windows has no such scale, only priority classes, so any
    ``nice > 0`` means "below normal".
    """
    if not nice:
        return {}
    if os.name == "nt":
        return {"creationflags": BELOW_NORMAL_PRIORITY_CLASS}
    return {"preexec_fn": lambda: os.nice(nice)}


def _terminate(proc):
    """Stop a task and the worker processes it started."""
    if os.name == "nt":
        subprocess.run(["taskkill", "/PID", str(proc.pid), "/T", "/F"],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        proc.terminate()


PROGRESS_EVERY = 60     # seconds between progress lines while a task runs


def _last_line(log_path):
    """Last non-empty line of a task log (what the experiment printed most recently)."""
    try:
        with open(log_path, "rb") as f:
            f.seek(0, os.SEEK_END)
            f.seek(max(0, f.tell() - 4096))
            lines = f.read().decode(errors="replace").replace("\r", "\n").splitlines()
    except OSError:
        return ""
    return next((line.strip() for line in reversed(lines) if line.strip()), "")


def _wait(proc, log_path, started, console):
    """Wait for the process; every PROGRESS_EVERY seconds print the log's newest line if it changed."""
    shown = ""
    while True:
        try:
            return proc.wait(timeout=PROGRESS_EVERY)
        except subprocess.TimeoutExpired:
            line = _last_line(log_path)
            if line and line != shown:
                shown = line
                console.print(f"    [dim]{fmt_duration(time.monotonic() - started)}[/]  {escape(line)}",
                              highlight=False)


def _tail_hint(log_path):
    if os.name == "nt":
        return f"Get-Content -Wait {log_path}"
    return f"tail -f {log_path}"


def execute(tasks, registry_order, *, nice=19, dry_run=False, show_plan=True, console=None):
    """Run the tasks; returns a process exit code (0 only if everything succeeded)."""
    console = console or Console()
    plan = plan_order(tasks, registry_order)
    if show_plan:
        print_plan(plan, console)
    if dry_run or not plan:
        return 0

    log_dir = ROOT / ".manager" / "logs" / datetime.now().strftime("%Y%m%d-%H%M%S")
    log_dir.mkdir(parents=True)
    console.print(f"logs: {log_dir}\n")

    failed_data = set()      # data patterns whose run failed in this session
    ok, failed, skipped = [], [], []
    interrupted = False

    for i, task in enumerate(plan, 1):
        head = f"[{i}/{len(plan)}] {task.kind:<4} {task.id}"

        if task.kind == "plot":
            missing = [p for p in task.reads if not matches(p)]
            if missing:
                console.print(f"{head}  [yellow]skipped[/]: no data for {', '.join(missing)}")
                skipped.append(task)
                continue
            if failed_data & set(task.reads):
                console.print(f"{head}  [yellow]skipped[/]: its run failed")
                skipped.append(task)
                continue

        log_path = log_dir / (task.id.replace("/", "__").replace(":", "__") + ".log")
        env = {**os.environ, "PYTHONUNBUFFERED": "1", "PYTHONIOENCODING": "utf-8"}
        if task.kind == "plot":
            env["MPLBACKEND"] = "Agg"      # never block on plt.show()
        priority = _priority_options(nice) if task.kind == "run" else {}

        console.print(f"{head}  running...  ({_tail_hint(log_path.relative_to(ROOT))})")
        started = time.monotonic()
        with open(log_path, "w") as log:
            proc = subprocess.Popen(_command(task), cwd=ROOT, env=env, stdout=log,
                                    stderr=subprocess.STDOUT, **priority)
            try:
                code = _wait(proc, log_path, started, console)
            except KeyboardInterrupt:
                _terminate(proc)
                try:
                    proc.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    proc.kill()
                interrupted = True
                code = None
        elapsed = fmt_duration(time.monotonic() - started)

        if interrupted:
            console.print(f"    [red]interrupted[/] after {elapsed}")
            failed.append(task)
            break
        if code != 0:
            console.print(f"    [red]failed[/] (exit {code}) after {elapsed}; last lines of the log:")
            for line in log_path.read_text(errors="replace").splitlines()[-12:]:
                console.print(f"      {line}", markup=False, highlight=False)
            failed.append(task)
            if task.kind == "run":
                failed_data.update(task.writes)
            continue

        no_output = [p for p in task.writes if not matches(p)]
        if no_output:
            console.print(f"    [yellow]finished[/] in {elapsed}, but nothing matches: {', '.join(no_output)}")
        else:
            console.print(f"    [green]done[/] in {elapsed}")
        ok.append(task)

    not_started = len(plan) - len(ok) - len(failed) - len(skipped)
    console.print(f"\n[green]{len(ok)} ok[/], [red]{len(failed)} failed[/], "
                  f"[yellow]{len(skipped)} skipped[/]"
                  + (f", {not_started} not started" if not_started else ""))
    return 0 if not (failed or skipped or not_started) else 1
