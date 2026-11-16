import argparse
import glob
import os
import subprocess
import sys
from datetime import datetime

from rich.console import Console
from rich.tree import Tree as RichTree

from .runner import execute, plan_order, print_plan, select
from .spec import ROOT, load_registry
from .status import task_status

COLORS = {"done": "green", "missing": "red", "blocked": "red",
          "partial": "yellow", "ready": "yellow", "stale": "yellow"}


def build_parser():
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--dry-run", action="store_true", help="show the plan, run nothing")
    common.add_argument("--yes", "-y", action="store_true", help="don't ask before starting")
    common.add_argument("--nice", type=int, default=19, help="nice level for run tasks (default 19)")
    common.add_argument("--detach", "-d", action="store_true",
                        help="start in the background and return (survives closing the terminal / ssh)")

    parser = argparse.ArgumentParser(
        prog="manager", description="Tick what to run and plot. No subcommand: interactive tree.")
    parser.add_argument("--papers-dir", action="append", metavar="DIR",
                        help="directory holding <paper>/tasks.py manifests (repeatable; default: papers)")
    sub = parser.add_subparsers(dest="cmd")
    sub.add_parser("tui", parents=[common], help="interactive tree (default)")
    sub.add_parser("list", help="print the tree with status")
    sub.add_parser("check", help="verify that manifests point at real modules")
    run = sub.add_parser("run", parents=[common], help="run tasks by id, glob or prefix")
    run.add_argument("patterns", nargs="+", metavar="PATTERN",
                     help="e.g. 'manipulation_of_hamming/exp1/*' or '*:plot'")
    run.add_argument("--kind", choices=["run", "plot"], help="only this kind of task")
    return parser


def cmd_list(registry, console):
    tree = RichTree("[bold]experiments[/]")
    papers = {}
    for task in registry.tasks:
        papers.setdefault(task.paper, {}).setdefault(task.family, {}).setdefault(task.variant, []).append(task)
    for paper, families in papers.items():
        pnode = tree.add(f"[bold]{registry.paper_titles.get(paper, paper)}[/]")
        for family, variants in families.items():
            fnode = pnode.add(f"[bold]{registry.family_titles.get((paper, family), family)}[/]")
            for variant, tasks in variants.items():
                vnode = fnode.add(variant)
                for task in tasks:
                    status = task_status(task)
                    flag = "  [yellow]! broken[/]" if task.broken else ""
                    vnode.add(f"{task.kind:<4} [{COLORS[status.state]}]{status.text}[/]{flag}")
    console.print(tree)


def cmd_check(registry, console):
    problems = 0
    for task in registry.tasks:
        path = ROOT / (task.module.replace(".", "/") + ".py")
        if not path.exists():
            console.print(f"[red]missing module[/] {task.id}: {path.relative_to(ROOT)}")
            problems += 1
        elif "__main__" not in path.read_text():
            console.print(f"[red]no __main__ block[/] {task.id}: {path.relative_to(ROOT)}")
            problems += 1
        if task.kind == "run" and not task.writes:
            console.print(f"[red]run task declares no outputs[/] {task.id}")
            problems += 1
        if task.kind == "plot" and not (task.reads and task.writes):
            console.print(f"[red]plot task needs reads and writes[/] {task.id}")
            problems += 1
    broken = [t for t in registry.tasks if t.broken]
    console.print(f"{len(registry.tasks)} task(s) checked, {problems} problem(s), "
                  f"{len(broken)} marked broken")
    return 1 if problems else 0


def start_detached(tasks, args, console):
    """Re-run the selected tasks in a separate session, so closing the terminal does not stop them."""
    out_dir = ROOT / ".manager" / "runs"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / (datetime.now().strftime("%Y%m%d-%H%M%S") + ".out")

    cmd = [sys.executable, "-m", "manager"]
    for directory in args.papers_dir or []:
        cmd += ["--papers-dir", directory]
    cmd += ["run", *[glob.escape(t.id) for t in tasks], "-y", "--nice", str(args.nice)]

    if os.name == "nt":
        # DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP
        options = {"creationflags": getattr(subprocess, "DETACHED_PROCESS", 0x8)
                   | getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0x200)}
    else:
        options = {"start_new_session": True}
    env = {**os.environ, "PYTHONUNBUFFERED": "1", "COLUMNS": "200"}   # no 80-column wrapping in the file
    with open(out, "w") as log:
        proc = subprocess.Popen(cmd, cwd=ROOT, env=env, stdin=subprocess.DEVNULL,
                                stdout=log, stderr=subprocess.STDOUT, **options)

    rel = out.relative_to(ROOT)
    console.print(f"started in the background (pid {proc.pid}), {len(tasks)} task(s)")
    console.print(f"progress: tail -f {rel}" if os.name != "nt" else f"progress: Get-Content -Wait {rel}")
    if os.name != "nt":
        console.print(f"stop everything: kill -- -{proc.pid}")
    return 0


def confirm_and_run(tasks, registry, args, console):
    order = {t.id: i for i, t in enumerate(registry.tasks)}
    plan = plan_order(tasks, order)
    print_plan(plan, console)
    if args.dry_run:
        return 0
    detach = args.detach
    if not args.yes:
        prompt = ("Enter to start in the background, Ctrl-C to abort: " if detach else
                  "Enter: run here   b: run in the background   Ctrl-C: abort: ")
        try:
            answer = input(prompt)
        except (KeyboardInterrupt, EOFError):
            console.print("\naborted")
            return 1
        detach = detach or answer.strip().lower() == "b"
    if detach:
        return start_detached(tasks, args, console)
    return execute(tasks, order, nice=args.nice, show_plan=False, console=console)


def main(argv=None):
    args = build_parser().parse_args(argv)
    # no subcommand = interactive tree with default options
    for name, default in (("dry_run", False), ("yes", False), ("nice", 19), ("detach", False)):
        if not hasattr(args, name):
            setattr(args, name, default)

    console = Console()
    registry = load_registry(args.papers_dir)

    if args.cmd == "list":
        cmd_list(registry, console)
        return 0
    if args.cmd == "check":
        return cmd_check(registry, console)
    if args.cmd == "run":
        tasks = select(registry.tasks, args.patterns, args.kind)
        if not tasks:
            console.print("[red]no task matches[/] " + " ".join(args.patterns))
            return 2
        return confirm_and_run(tasks, registry, args, console)

    from .tui import ManagerApp
    tasks = ManagerApp(registry).run()
    if not tasks:
        console.print("nothing selected")
        return 0
    return confirm_and_run(tasks, registry, args, console)


if __name__ == "__main__":
    raise SystemExit(main())
