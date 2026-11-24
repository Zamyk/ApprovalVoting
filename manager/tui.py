"""Interactive tree: paper -> family -> variant -> run / plot. Tick, then start."""

from dataclasses import dataclass

from rich.text import Text
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Footer, Header, Static, Tree

from .spec import Task
from .status import task_status

COLORS = {"done": "green", "missing": "red", "blocked": "red",
          "partial": "yellow", "ready": "yellow", "stale": "yellow"}


@dataclass
class Group:
    title: str
    level: str        # paper | family | variant


def tasks_under(node):
    if isinstance(node.data, Task):
        return [node.data]
    return [t for child in node.children for t in tasks_under(child)]


def all_nodes(node):
    yield node
    for child in node.children:
        yield from all_nodes(child)


class TaskTree(Tree[object]):
    def action_toggle_node(self) -> None:
        """Space ticks (enter still opens/closes a branch)."""
        node = self.cursor_node
        if node is not None:
            self.app.toggle_tick(node)


class ManagerApp(App[list]):
    TITLE = "Experiment manager"
    CSS = """
    #tree { height: 1fr; }
    #details { height: 8; border: round $primary; padding: 0 1; }
    #summary { height: 1; padding: 0 1; text-style: bold; }
    """
    BINDINGS = [
        Binding("a", "tick_all", "All"),
        Binding("n", "tick_none", "None"),
        Binding("s", "tick_needed", "Needs work"),
        Binding("e", "expand_all", "Expand"),
        Binding("c", "collapse_all", "Collapse"),
        Binding("r", "refresh_status", "Refresh"),
        Binding("g", "go", "Go"),
        Binding("q", "quit", "Quit"),
    ]

    def __init__(self, registry):
        super().__init__()
        self.registry = registry
        self.tasks = registry.tasks
        self.by_id = {t.id: t for t in self.tasks}
        self.ticked = set()
        self.status = {t.id: task_status(t) for t in self.tasks}

    # ---- layout ---------------------------------------------------------
    def compose(self) -> ComposeResult:
        yield Header()
        yield TaskTree("experiments", id="tree")
        yield Static(id="details")
        yield Static(id="summary")
        yield Footer()

    def on_mount(self) -> None:
        self.sub_title = "space: tick   enter: open/close   arrows: move"
        tree = self.query_one(TaskTree)
        tree.show_root = False

        structure = {}
        for task in self.tasks:
            structure.setdefault(task.paper, {}).setdefault(task.family, {}).setdefault(
                task.variant, []).append(task)

        titles = self.registry
        for paper, families in structure.items():
            paper_node = tree.root.add(
                "", data=Group(titles.paper_titles.get(paper, paper), "paper"), expand=True)
            for family, variants in families.items():
                family_node = paper_node.add(
                    "", data=Group(titles.family_titles.get((paper, family), family), "family"),
                    expand=True)
                for variant, tasks in variants.items():
                    variant_node = family_node.add("", data=Group(variant, "variant"), expand=False)
                    for task in tasks:
                        variant_node.add_leaf("", data=task)
        self.refresh_labels()
        tree.focus()

    # ---- labels ---------------------------------------------------------
    def box(self, tasks):
        pool = [t for t in tasks if not t.broken] or tasks
        ticked = sum(t.id in self.ticked for t in pool)
        if ticked == len(pool):
            return "[x]"
        return "[-]" if ticked else "[ ]"

    def label(self, node):
        data = node.data
        if isinstance(data, Task):
            status = self.status[data.id]
            text = Text(f"{self.box([data])} {data.kind:<4} ")
            text.append(status.text, style=COLORS[status.state])
            if data.broken:
                text.append("   ! broken", style="yellow")
            return text

        tasks = tasks_under(node)
        text = Text(f"{self.box(tasks)} {data.title}", style="" if data.level == "variant" else "bold")
        if data.level == "variant":
            if not node.is_expanded:           # opened variants show the same info below
                summary = "   ".join(f"{t.kind}: {self.status[t.id].text}" for t in tasks)
                text.append("   " + summary, style="dim")
        else:
            text.append(f"   ({len(tasks)} tasks)", style="dim")
        return text

    def refresh_labels(self):
        tree = self.query_one(TaskTree)
        for node in all_nodes(tree.root):
            if node is not tree.root:
                node.set_label(self.label(node))
        runs = sum(1 for i in self.ticked if self.by_id[i].kind == "run")
        plots = len(self.ticked) - runs
        self.query_one("#summary", Static).update(
            f"Ticked: {runs} run(s), {plots} plot(s)   |   g: start   q: quit")
        if tree.cursor_node is not None:
            self.show_details(tree.cursor_node)

    def show_details(self, node):
        data = node.data
        text = Text()
        if data is None:                       # the hidden root
            self.query_one("#details", Static).update(text)
            return
        if isinstance(data, Task):
            status = self.status[data.id]
            text.append(data.id + "\n", style="bold")
            text.append("status : ")
            text.append(status.text + "\n", style=COLORS[status.state])
            text.append(f"command: python -m {data.module} {' '.join(data.args)}\n")
            if data.reads:
                text.append("reads  : " + ", ".join(data.reads) + "\n")
            if data.writes:
                text.append("writes : " + ", ".join(data.writes) + "\n")
            if data.note:
                text.append("note   : " + data.note + "\n")
            if data.broken:
                text.append("broken : " + data.broken + "\n", style="yellow")
        else:
            tasks = tasks_under(node)
            ticked = sum(t.id in self.ticked for t in tasks)
            text.append(data.title + "\n", style="bold")
            text.append(f"{len(tasks)} task(s), {ticked} ticked\n")
            text.append("space ticks everything below; enter opens/closes\n", style="dim")
        self.query_one("#details", Static).update(text)

    def on_tree_node_highlighted(self, event: Tree.NodeHighlighted) -> None:
        self.show_details(event.node)

    def on_tree_node_expanded(self, event: Tree.NodeExpanded) -> None:
        if event.node.data is not None:        # not the hidden root
            event.node.set_label(self.label(event.node))

    def on_tree_node_collapsed(self, event: Tree.NodeCollapsed) -> None:
        if event.node.data is not None:
            event.node.set_label(self.label(event.node))

    # ---- ticking --------------------------------------------------------
    def toggle_tick(self, node):
        if isinstance(node.data, Task):
            ids = {node.data.id}
        else:
            ids = {t.id for t in tasks_under(node) if not t.broken}
        if ids <= self.ticked:
            self.ticked -= ids
        else:
            self.ticked |= ids
        self.refresh_labels()

    def action_tick_all(self) -> None:
        self.ticked = {t.id for t in self.tasks if not t.broken}
        self.refresh_labels()

    def action_tick_none(self) -> None:
        self.ticked = set()
        self.refresh_labels()

    def action_tick_needed(self) -> None:
        """Tick what needs doing; a plot follows its run when the run is ticked."""
        wanted = {t.id for t in self.tasks if not t.broken and self.status[t.id].needs_work}
        for task in self.tasks:
            if task.kind == "plot" and not task.broken:
                run_id = task.id.rsplit(":", 1)[0] + ":run"
                if run_id in wanted:
                    wanted.add(task.id)
        self.ticked = wanted
        self.refresh_labels()

    def action_expand_all(self) -> None:
        for node in all_nodes(self.query_one(TaskTree).root):
            node.expand()

    def action_collapse_all(self) -> None:
        tree = self.query_one(TaskTree)
        for node in all_nodes(tree.root):
            if node is not tree.root:
                node.collapse()

    def action_refresh_status(self) -> None:
        self.status = {t.id: task_status(t) for t in self.tasks}
        self.refresh_labels()
        self.notify("Status refreshed")

    def action_go(self) -> None:
        if not self.ticked:
            self.notify("Nothing ticked", severity="warning")
            return
        self.exit([t for t in self.tasks if t.id in self.ticked])
