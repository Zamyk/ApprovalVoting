"""Shared plotting code for the hamming experiments.

Almost every figure in this folder is one of three layouts:

* m-lines pair: two side-by-side panels, one line per ``m`` against orness
  (experiment 1 family).
* f-lines pair: two side-by-side panels, one line per voting rule ``f``
  against the number of voters ``n`` (experiment 2 Euclidean family).
* f-lines single: one panel of the same kind of lines (experiment 2 family).

The per-experiment scripts only name their input CSVs, titles, labels and
output file. The data can be either many runs (aggregated to mean/min/max)
or a single CSV plotted as-is.
"""

import pandas as pd
import matplotlib.pyplot as plt

from . import PLOTS_DIRECTORY_PATH, RESULTS_DIRECTORY_PATH

# Horizontal gap between the two panels of a pair figure.
PAIR_WSPACE = 0.2

M_LINE_STYLES = {5: (0, (5, 5)), 4: (0, (3, 4)), 3: (0, (1, 2))}
M_LINE_WIDTHS = {5: 1.8, 4: 1.2, 3: 1.2}

F_STYLES = {
    "f_2n_3": {"ls": (0, (4, 3)), "lw": 2.2, "label": r"$\mathbf{f^{2n/3}}$"},
    "Borda": {"ls": (0, (1, 2)), "lw": 2.2, "label": r"$\mathbf{Borda}$"},
    "f_n_2": {"ls": (0, (5, 5)), "lw": 1.2, "label": r"$\mathbf{f^{n/2}}$"},
    "f_n_3": {"ls": (0, (1, 3)), "lw": 1.2, "label": r"$\mathbf{f^{n/3}}$"},
}


def use_black_text():
    plt.rcParams.update({
        "text.color": "black",
        "axes.labelcolor": "black",
        "axes.edgecolor": "black",
        "xtick.color": "black",
        "ytick.color": "black",
        "axes.titlecolor": "black",
    })


def output_name(base, start_idx=None, end_idx=None):
    if start_idx is not None and end_idx is not None:
        return f"{base}_{start_idx}_to_{end_idx}.png"
    return f"{base}.png"


def load_runs(stem, start_idx=None, end_idx=None, *, group_cols, indexed=True):
    """Load one or many run CSVs from the results folder and aggregate per group.

    With a range, reads ``<stem>_<i>.csv`` for each ``i`` (or ``<stem>.csv``
    when ``indexed`` is False). Without a range, reads ``<stem>.csv`` if it
    exists, otherwise every ``<stem>_*.csv`` (only when ``indexed``).

    Returns the columns ``group_cols`` plus ``mean_manipulability``,
    ``min_manipulability`` and ``max_manipulability``.
    """
    directory = RESULTS_DIRECTORY_PATH
    all_dfs = []
    if start_idx is not None and end_idx is not None:
        for i in range(start_idx, end_idx + 1):
            file_path = directory / (f"{stem}_{i}.csv" if indexed else f"{stem}.csv")
            if file_path.exists():
                all_dfs.append(pd.read_csv(file_path))
            else:
                print(f"Warning: File {file_path.name} not found. Skipping.")
    else:
        single_file = directory / f"{stem}.csv"
        if single_file.exists():
            all_dfs.append(pd.read_csv(single_file))
        elif indexed:
            for f in sorted(directory.glob(f"{stem}_*.csv")):
                all_dfs.append(pd.read_csv(f))

    if not all_dfs:
        raise FileNotFoundError(f"No files found for '{stem}' in {directory}")

    combined = pd.concat(all_dfs, ignore_index=True)
    return (
        combined.groupby(group_cols)
        .agg(
            mean_manipulability=("manipulability", "mean"),
            min_manipulability=("manipulability", "min"),
            max_manipulability=("manipulability", "max"),
        )
        .reset_index()
    )


def _load_side(stem, start_idx, end_idx, *, group_cols, aggregate, indexed):
    if aggregate:
        return load_runs(stem, start_idx, end_idx, group_cols=group_cols, indexed=indexed)
    return pd.read_csv(RESULTS_DIRECTORY_PATH / f"{stem}.csv")


def _save(file_name):
    plt.savefig(PLOTS_DIRECTORY_PATH / file_name, bbox_inches="tight", dpi=300)
    print(f"Plot saved as '{file_name}'")


def draw_m_lines(ax, df, y_col, band, group_col="m"):
    """One black line per group, styled by m.

    ``group_col="m"`` draws one line per m, labelled ``m=<m>``. ``group_col="label"``
    draws one line per dataset, labelled with its name, larger m first.
    ``band`` is ``(low_col, high_col, alpha)`` for shading, or None.
    """
    if group_col == "label":
        keys = sorted(df["label"].unique(), key=lambda s: -int(df.loc[df["label"] == s, "m"].iloc[0]))
    else:
        keys = sorted(df["m"].unique(), reverse=True)

    for key in keys:
        subset = df[df[group_col] == key].sort_values("orness")
        m = int(subset["m"].iloc[0])
        ax.plot(
            subset["orness"],
            subset[y_col],
            label=key if group_col == "label" else f"m={m}",
            color="black",
            linestyle=M_LINE_STYLES.get(m, "-"),
            linewidth=M_LINE_WIDTHS.get(m, 1.5),
        )
        if band:
            low, high, alpha = band
            ax.fill_between(subset["orness"], subset[low], subset[high], color="black", alpha=alpha)


def style_orness_axis(ax, ylabels=True):
    ax.set_xlim(0.5, 1.0)
    ax.set_ylim(0, 1.0)
    ax.set_xticks([0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.tick_params(axis="both", which="major", direction="in", right=True, top=False, labelsize=12)
    ax.set_xticklabels(["0.5", "0.6", "0.7", "0.8", "0.9", "1"])
    if ylabels:
        ax.set_yticklabels(["0", "0.25", "0.5", "0.75", "1"])


def draw_f_lines(ax, df, y_col, band):
    """One line per voting rule ``f`` against ``n``. ``band`` is ``(low_col, high_col, alpha)``."""
    for rule in sorted(df["f"].unique(), reverse=True):
        subset = df[df["f"] == rule].sort_values("n")
        style = F_STYLES.get(rule, {"ls": "-", "lw": 1.5, "label": rule})
        ax.plot(
            subset["n"],
            subset[y_col],
            color="black",
            linestyle=style["ls"],
            linewidth=style["lw"],
            label=style["label"],
        )
        if band:
            low, high, alpha = band
            ax.fill_between(subset["n"], subset[low], subset[high], color="black", alpha=alpha)


def _band(aggregate, band_alpha, low, high):
    return (low, high, band_alpha) if aggregate and band_alpha else None


def plot_m_panels(panels, ylabel, out, *, y_col="manipulability", band=None,
                  black_text=False, show=False):
    """Row of m-lines panels in the experiment 1 layout, one per ``(df, title)``.

    The first panel has the y label and tick labels, the others share its y axis.
    The legend sits to the right of the last panel. Saves to ``out`` and returns it.
    """
    if black_text:
        use_black_text()

    fig, axes = plt.subplots(1, len(panels), figsize=(5 * len(panels), 4), sharey=True, squeeze=False)
    axes = axes[0]
    for i, (ax, (df, title)) in enumerate(zip(axes, panels)):
        draw_m_lines(ax, df, y_col, band)
        ax.set_title(title, fontsize=14)
        style_orness_axis(ax, ylabels=(i == 0))

    axes[0].set_ylabel(ylabel, fontsize=14, labelpad=10)
    if len(panels) == 1:
        axes[0].set_xlabel("Orness Measure", fontsize=14, labelpad=10)
    else:
        fig.supxlabel("Orness Measure", fontsize=14, y=-0.05)
    plt.subplots_adjust(wspace=PAIR_WSPACE)

    handles, labels = axes[-1].get_legend_handles_labels()
    axes[-1].legend(handles, labels, loc="center left", bbox_to_anchor=(1.02, 0.5),
                    frameon=False, fontsize=12, handlelength=2.5)

    fig.savefig(out, dpi=300, bbox_inches="tight")
    print(f"Plot saved as '{out}'")
    if show:
        plt.show()
    else:
        plt.close(fig)
    return out


def plot_m_pair_figure(stems, titles, ylabel, base, start_idx=None, end_idx=None, *,
                       aggregate=True, indexed=True, band_alpha=None, black_text=False):
    """Two side-by-side m-lines panels vs orness.

    ``stems`` are the left and right data stems. With ``aggregate`` they are run
    files aggregated over ``m``/``orness``; otherwise they are plain CSVs whose
    ``manipulability`` column is drawn as-is.
    """
    if black_text:
        use_black_text()

    try:
        left = _load_side(stems[0], start_idx, end_idx, group_cols=["m", "orness"],
                          aggregate=aggregate, indexed=indexed)
        right = _load_side(stems[1], start_idx, end_idx, group_cols=["m", "orness"],
                           aggregate=aggregate, indexed=indexed)
    except FileNotFoundError as e:
        print(f"Skipping {base}: {e}")
        return

    y_col = "mean_manipulability" if aggregate else "manipulability"
    band = _band(aggregate, band_alpha, "min_manipulability", "max_manipulability")

    plot_m_panels([(left, titles[0]), (right, titles[1])], ylabel,
                  PLOTS_DIRECTORY_PATH / output_name(base, start_idx, end_idx),
                  y_col=y_col, band=band)


def plot_f_pair_figure(stems, titles, base, start_idx=None, end_idx=None, *,
                       indexed=True, band_alpha=0.06, black_text=True):
    """Two side-by-side f-lines panels vs number of voters, both with y tick labels."""
    if black_text:
        use_black_text()

    try:
        left = _load_side(stems[0], start_idx, end_idx, group_cols=["f", "n"],
                          aggregate=True, indexed=indexed)
        right = _load_side(stems[1], start_idx, end_idx, group_cols=["f", "n"],
                           aggregate=True, indexed=indexed)
    except FileNotFoundError as e:
        print(f"Skipping {base}: {e}")
        return

    band = _band(True, band_alpha, "min_manipulability", "max_manipulability")

    fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)
    for ax, df, title, is_right in ((axes[0], left, titles[0], False),
                                    (axes[1], right, titles[1], True)):
        draw_f_lines(ax, df, "mean_manipulability", band)
        ax.set_title(title, fontsize=16, pad=15)
        ax.set_xlabel("Number of Voters", fontsize=14, labelpad=10)
        ax.set_xlim(df["n"].min(), df["n"].max())
        ax.set_ylim(0.0, 1.0)
        ax.set_yticks([0.0, 0.25, 0.5, 0.75, 1.0])
        ax.tick_params(axis="both", which="major", direction="in", labelsize=13, length=6,
                       right=False, top=False)
        if not is_right:
            ax.set_ylabel("Ratio of Manipulation", fontsize=14, labelpad=10)

    plt.subplots_adjust(wspace=PAIR_WSPACE)

    handles, labels = axes[1].get_legend_handles_labels()
    axes[1].legend(handles, labels, loc="center left", bbox_to_anchor=(1.02, 0.5),
                   frameon=False, fontsize=15, handlelength=3)

    _save(output_name(base, start_idx, end_idx))


def plot_f_single_figure(stem, base, start_idx=None, end_idx=None, *, title="Uniform Elections",
                         aggregate=False, indexed=True, band_alpha=None, black_text=False):
    """Single f-lines panel vs number of voters."""
    if black_text:
        use_black_text()

    try:
        df = _load_side(stem, start_idx, end_idx, group_cols=["f", "n"],
                        aggregate=aggregate, indexed=indexed)
    except FileNotFoundError as e:
        print(f"Skipping {base}: {e}")
        return

    y_col = "mean_manipulability" if aggregate else "manipulability"
    band = _band(aggregate, band_alpha, "min_manipulability", "max_manipulability")

    fig, ax = plt.subplots(figsize=(8, 5))
    draw_f_lines(ax, df, y_col, band)

    ax.set_title(title, fontsize=16, pad=15)
    ax.set_xlabel("Number of Voters", fontsize=14, labelpad=10)
    ax.set_ylabel("Ratio of Manipulation", fontsize=14, labelpad=10)
    ax.set_xlim(df["n"].min(), df["n"].max())
    ax.set_ylim(0.3, 1.0)
    ax.set_yticks([0.3, 0.5, 0.7, 0.9])
    ax.tick_params(axis="both", which="major", direction="in", labelsize=13, length=6,
                   right=False, top=False)
    ax.legend(loc="center left", bbox_to_anchor=(1.0, 0.5), frameon=False, fontsize=15,
              handlelength=3)

    plt.tight_layout()
    _save(output_name(base, start_idx, end_idx))


def plot_m_grid(panels, ylabel, out, *, figsize, group_col="m", y_col="manipulability",
                band=None, legend_fontsize=12, ylabel_labelpad=10, tight_bbox=False,
                show=False, black_text=False):
    """One row of m-lines panels sharing the y axis, with a legend outside on the right.

    ``panels`` is a list of ``(df, title)``. The y label and tick labels are only
    on the first panel. ``out`` is the full output path.
    """
    if black_text:
        use_black_text()

    fig, axes = plt.subplots(1, len(panels), figsize=figsize, sharey=True,
                             layout="constrained", squeeze=False)
    axes = axes[0]
    for i, (ax, (df, title)) in enumerate(zip(axes, panels)):
        draw_m_lines(ax, df, y_col=y_col, band=band, group_col=group_col)
        if title:
            ax.set_title(title, fontsize=14)
        style_orness_axis(ax, ylabels=(i == 0))

    axes[0].set_ylabel(ylabel, fontsize=14, labelpad=ylabel_labelpad)
    if len(panels) == 1:
        # one panel: label under that axis (a figure-level label would also centre on the legend)
        axes[0].set_xlabel("Orness Measure", fontsize=14, labelpad=10)
    else:
        fig.supxlabel("Orness Measure", fontsize=14)

    handles, labels = axes[-1].get_legend_handles_labels()
    fig.legend(handles, labels, loc="outside right center", frameon=False,
               fontsize=legend_fontsize, handlelength=2.5)

    if tight_bbox:
        fig.savefig(out, dpi=300, bbox_inches="tight")
    else:
        fig.savefig(out, dpi=300)
    print(f"Plot saved as '{out}'")
    if show:
        plt.show()
    else:
        plt.close(fig)
    return out
