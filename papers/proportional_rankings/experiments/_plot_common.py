"""Shared plotting helpers for scatter grid figures."""

import math
import matplotlib.cm as cm
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import pandas as pd

from . import PLOTS_DIRECTORY_PATH, RESULTS_DIRECTORY_PATH


def use_black_text():
    plt.rcParams.update({
        "text.color": "black",
        "axes.labelcolor": "black",
        "axes.edgecolor": "black",
        "xtick.color": "black",
        "ytick.color": "black",
        "axes.titlecolor": "black",
    })


def _save(file_name):
    out_path = PLOTS_DIRECTORY_PATH / file_name
    plt.savefig(out_path, bbox_inches="tight", dpi=300)
    print(f"Plot saved as '{file_name}'")
    return out_path


def style_scatter_axis(ax, xlabel):
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(0.0, 1.0)
    ticks = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    labels = ["0.0", "0.2", "0.4", "0.6", "0.8", "1.0"]
    ax.set_xticks(ticks)
    ax.set_yticks(ticks)
    ax.set_xticklabels(labels, fontsize=8)
    ax.set_yticklabels(labels, fontsize=8)
    ax.grid(True, linestyle=":", color="gray", alpha=0.6)
    ax.set_xlabel(xlabel, fontsize=14, labelpad=10)


def _render_status_box(ax, message, bold=False):
    ax.set_facecolor("#ffe6e6")
    ax.text(
        0.5, 0.5, message, color="red",
        ha="center", va="center", transform=ax.transAxes,
        fontsize=12, fontweight="bold" if bold else "normal",
    )


def extract_gen_method(filename, default="unknown"):
    """Extract generation method name from a file string like '...gen_<method>_candidates...'."""
    if not isinstance(filename, str):
        return default
    if "gen_" in filename and "_candidates" in filename:
        return filename.split("gen_", 1)[1].split("_candidates", 1)[0]
    return default


def _create_grid_layout(nrows, ncols, grid_figsize, bottom_space_inches, hspace, wspace):
    """Create a grid keeping `grid_figsize` (in inches) for the main grid and adding space below."""
    grid_w, grid_h = grid_figsize
    total_h = grid_h + bottom_space_inches
    fig = plt.figure(figsize=(grid_w, total_h))

    gs = gridspec.GridSpec(
        2, 1,
        height_ratios=[grid_h, bottom_space_inches],
        hspace=0.18,
    )
    sub_gs = gridspec.GridSpecFromSubplotSpec(
        nrows, ncols,
        subplot_spec=gs[0],
        hspace=hspace,
        wspace=wspace,
    )
    axes = [fig.add_subplot(sub_gs[r, c]) for r in range(nrows) for c in range(ncols)]
    return fig, axes, gs[1]


def draw_scatter_panel(ax, file_path, title, *, x_col="a", y_col="y_r",
                       point_size=8, color="gray"):
    """Draw one scatter panel with a single color or a status box."""
    if file_path.exists():
        try:
            df = pd.read_csv(file_path)
            ax.scatter(df[x_col], df[y_col], color=color, s=point_size, edgecolors="none")
        except Exception:
            _render_status_box(ax, "Błąd pliku", bold=False)
    else:
        _render_status_box(ax, "Brak danych", bold=True)

    style_scatter_axis(ax, title)


def plot_scatter_grid(panels, out_name, *, nrows=3, ncols=3, figsize=(12, 12),
                      x_col="a", y_col="y_r", point_size=8, color="gray",
                      hspace=0.4, wspace=0.3, black_text=False, show=False):
    """Plot a grid of scatter panels with a uniform point color."""
    if black_text:
        use_black_text()

    fig, axes = plt.subplots(nrows, ncols, figsize=figsize)
    axes_flat = axes.flatten() if hasattr(axes, "flatten") else [axes]

    for idx, ax in enumerate(axes_flat):
        if idx < len(panels):
            title, file_name = panels[idx]
            draw_scatter_panel(
                ax,
                RESULTS_DIRECTORY_PATH / file_name,
                title,
                x_col=x_col,
                y_col=y_col,
                point_size=point_size,
                color=color,
            )
        else:
            ax.set_visible(False)

    plt.tight_layout()
    plt.subplots_adjust(hspace=hspace, wspace=wspace)
    out_path = _save(out_name)

    if show:
        plt.show()
    else:
        plt.close(fig)

    return out_path


def plot_scatter_colorbar_grid(panels, out_name, *, color_col, colorbar_label,
                               nrows=3, ncols=3, grid_figsize=(12, 12),
                               bottom_space_inches=0.65, x_col="a", y_col="y_r",
                               cmap="viridis", point_size=8, shuffle=True,
                               hspace=0.4, wspace=0.3, black_text=False, show=False):
    """Plot a scatter grid colored by a numeric column with a compact colorbar below."""
    if black_text:
        use_black_text()

    loaded_dfs = {}
    all_values = []

    for idx, (_, file_name) in enumerate(panels):
        file_path = RESULTS_DIRECTORY_PATH / file_name
        if file_path.exists():
            try:
                df = pd.read_csv(file_path)
                if shuffle:
                    df = df.sample(frac=1).reset_index(drop=True)
                vals = pd.to_numeric(df[color_col], errors="coerce").dropna()
                if not vals.empty:
                    all_values.append(vals)
                loaded_dfs[idx] = ("ok", df)
            except Exception:
                loaded_dfs[idx] = ("error", None)
        else:
            loaded_dfs[idx] = ("missing", None)

    vmin = float(pd.concat(all_values).min()) if all_values else None
    vmax = float(pd.concat(all_values).max()) if all_values else None

    fig, axes, bottom_spec = _create_grid_layout(
        nrows, ncols, grid_figsize, bottom_space_inches, hspace, wspace
    )
    scat = None

    for idx, ax in enumerate(axes):
        if idx < len(panels):
            title, _ = panels[idx]
            status, payload = loaded_dfs[idx]
            if status == "ok":
                df = payload
                scat = ax.scatter(
                    df[x_col],
                    df[y_col],
                    c=df[color_col],
                    cmap=cmap,
                    vmin=vmin,
                    vmax=vmax,
                    s=point_size,
                    edgecolors="none",
                )
            elif status == "error":
                _render_status_box(ax, "Błąd pliku", bold=False)
            else:
                _render_status_box(ax, "Brak danych", bold=True)

            style_scatter_axis(ax, title)
        else:
            ax.set_visible(False)

    if scat is not None:
        # Thin horizontal bar (~1/3 of standard thick bar) placed near the top of the bottom area.
        cbar_sub = gridspec.GridSpecFromSubplotSpec(
            3, 1,
            subplot_spec=bottom_spec,
            height_ratios=[0.2, 0.22, 0.58],
            hspace=0.1,
        )
        cbar_ax = fig.add_subplot(cbar_sub[1, 0])
        cbar = fig.colorbar(scat, cax=cbar_ax, orientation="horizontal")
        cbar.ax.tick_params(labelsize=8, length=3)
        cbar.set_label(colorbar_label, fontsize=11, labelpad=4)

    out_path = _save(out_name)
    if show:
        plt.show()
    else:
        plt.close(fig)

    return out_path


def plot_scatter_methods_grid(panels, out_name, *, file_col="file",
                              legend_title="Generation Method", nrows=3, ncols=3,
                              grid_figsize=(12, 12), bottom_space_inches=0.95,
                              x_col="a", y_col="y_r", cmap_name="tab10",
                              point_size=8, shuffle=True, hspace=0.4, wspace=0.3,
                              black_text=False, show=False):
    """Plot a shuffled scatter grid colored by generation method with a compact legend below."""
    if black_text:
        use_black_text()

    all_methods = set()
    dfs_by_idx = {}

    for idx, (_, file_name) in enumerate(panels):
        file_path = RESULTS_DIRECTORY_PATH / file_name
        if file_path.exists():
            try:
                df = pd.read_csv(file_path)
                if shuffle:
                    df = df.sample(frac=1).reset_index(drop=True)
                if file_col in df.columns:
                    methods = [extract_gen_method(fname) for fname in df[file_col]]
                    df = df.copy()
                    df["_gen_method"] = methods
                    all_methods.update(m for m in methods if m != "unknown")
                dfs_by_idx[idx] = ("ok", df)
            except Exception:
                dfs_by_idx[idx] = ("error", None)
        else:
            dfs_by_idx[idx] = ("missing", None)

    sorted_methods = sorted(all_methods)
    palette = cm.get_cmap(cmap_name, max(len(sorted_methods), 1))
    method_to_color = {m: palette(i) for i, m in enumerate(sorted_methods)}

    fig, axes, bottom_spec = _create_grid_layout(
        nrows, ncols, grid_figsize, bottom_space_inches, hspace, wspace
    )

    for idx, ax in enumerate(axes):
        if idx < len(panels):
            title, _ = panels[idx]
            status, payload = dfs_by_idx[idx]
            if status == "ok":
                df = payload
                if "_gen_method" in df.columns:
                    colors = [method_to_color.get(m, "gray") for m in df["_gen_method"]]
                    ax.scatter(df[x_col], df[y_col], color=colors, s=point_size, edgecolors="none")
                else:
                    ax.scatter(df[x_col], df[y_col], color="gray", s=point_size, edgecolors="none")
            elif status == "error":
                _render_status_box(ax, "Błąd pliku", bold=False)
            else:
                _render_status_box(ax, "Brak danych", bold=True)

            style_scatter_axis(ax, title)
        else:
            ax.set_visible(False)

    if sorted_methods:
        legend_sub = gridspec.GridSpecFromSubplotSpec(1, 1, subplot_spec=bottom_spec)
        legend_ax = fig.add_subplot(legend_sub[0, 0])
        legend_ax.axis("off")

        handles = [
            mpatches.Patch(color=method_to_color[m], label=m)
            for m in sorted_methods
        ]
        # Arrange into 2 rows (e.g. 2 columns for up to 4 items, or ceil(n/2) columns).
        ncol_2rows = max(1, math.ceil(len(handles) / 2))
        legend_ax.legend(
            handles=handles,
            loc="center",
            ncol=ncol_2rows,
            title=legend_title,
            fontsize=9.5,
            title_fontsize=10.5,
            frameon=False,
            columnspacing=1.5,
            handlelength=1.6,
        )

    out_path = _save(out_name)
    if show:
        plt.show()
    else:
        plt.close(fig)

    return out_path