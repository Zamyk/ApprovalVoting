# ApprovalVoting

This repository presents the results of work on replication of experiments from selected papers regarding approval voting. Our goal is to implement all necessary algorithms and to conduct experiments as described in the paper. When some necessary information is missing we try to use the most logical approach. We also conduct enhanced experiments - all to verify if conclusions presented in the paper hold. We describe our every decision regarding an approach we take conducting particular experiments in corresponding **README.md** files.

## Running experiments

```
uv run python -m manager
```

Opens a tree of papers, experiments and their `run` / `plot` tasks, with the state of each (no data, plotted, plot older than data, ...).

| key | action |
|---|---|
| space | tick / untick |
| enter | open / close a branch |
| `a` / `n` | tick all / none |
| `s` | tick what needs work (no data, partial data, missing or stale plot) |
| `r` | refresh status |
| `g` | go: show the plan, press Enter to start |
| `q` | quit |

Runs go first, then plots. Each task is a separate process, `python -m <module>`, run from the repo root. Run tasks get a low priority (nice 19, `--nice N` to change). Logs are in `.manager/logs/`.

Without the tree:

```
uv run python -m manager list                      # tree with status
uv run python -m manager run 'paper/exp1/*' -y     # by id, glob or prefix
uv run python -m manager run '*:plot' --dry-run    # only show the plan
uv run python -m manager check                     # manifests point at real modules
```

A paper's experiments are listed in `papers/<paper>/tasks.py` (`TASKS`). A new experiment has to be added there to show up.
