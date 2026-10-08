import argparse
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

from . import RESULTS_DIRECTORY_PATH, PLOTS_DIRECTORY_PATH


def load_and_aggregate_data(directory_path, prefix, start_idx=None, end_idx=None):
    """
    Loads Euclidean experiment 1 CSVs. Supports both a single file and a range of index files.
    """
    all_dfs = []
    if start_idx is not None and end_idx is not None:
        for i in range(start_idx, end_idx + 1):
            file_path = directory_path / f"experiment_1_euclidean_{prefix}_{i}.csv"
            if file_path.exists():
                all_dfs.append(pd.read_csv(file_path))
            else:
                print(f"Warning: File {file_path.name} not found. Skipping.")
    else:
        # Try unindexed file first, then look for indexed files
        single_file = directory_path / f"experiment_1_euclidean_{prefix}.csv"
        if single_file.exists():
            all_dfs.append(pd.read_csv(single_file))
        else:
            indexed_files = sorted(directory_path.glob(f"experiment_1_euclidean_{prefix}_*.csv"))
            for f in indexed_files:
                all_dfs.append(pd.read_csv(f))

    if not all_dfs:
        raise FileNotFoundError(f"No files found for prefix 'experiment_1_euclidean_{prefix}' in {directory_path}")

    combined_df = pd.concat(all_dfs, ignore_index=True)
    aggregated = (
        combined_df.groupby(["m", "orness"])
        .agg(
            mean_manipulability=("manipulability", "mean"),
            min_manipulability=("manipulability", "min"),
            max_manipulability=("manipulability", "max"),
        )
        .reset_index()
    )
    return aggregated


def plot_experiment_1_euclidean(start_idx=None, end_idx=None):
    plt.rcParams.update({
        "text.color": "black",
        "axes.labelcolor": "black",
        "axes.edgecolor": "black",
        "xtick.color": "black",
        "ytick.color": "black",
        "axes.titlecolor": "black",
    })

    df_normal = load_and_aggregate_data(RESULTS_DIRECTORY_PATH, "normal", start_idx, end_idx)
    df_triangle = load_and_aggregate_data(RESULTS_DIRECTORY_PATH, "triangle", start_idx, end_idx)

    fig, axes = plt.subplots(1, 2, figsize=(10, 4), sharey=True)

    line_styles = {
        5: (0, (5, 5)),
        4: (0, (3, 4)),
        3: (0, (1, 2)),
    }
    line_widths = {
        5: 1.8,
        4: 1.2,
        3: 1.2,
    }

    def plot_subplot(ax, df, title, is_right=False):
        for m in sorted(df["m"].unique(), reverse=True):
            subset = df[df["m"] == m].sort_values("orness")
            ls = line_styles.get(m, "-")
            lw = line_widths.get(m, 1.5)

            ax.plot(
                subset["orness"],
                subset["mean_manipulability"],
                label=f"m={m}",
                color="black",
                linestyle=ls,
                linewidth=lw,
            )
            ax.fill_between(
                subset["orness"],
                subset["min_manipulability"],
                subset["max_manipulability"],
                color="black",
                alpha=0.08,
            )

        ax.set_title(title, fontsize=14)
        ax.set_xlim(0.5, 1.0)
        ax.set_ylim(0, 1.0)
        ax.set_xticks([0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
        ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
        ax.tick_params(axis="both", which="major", direction="in", right=True, top=False, labelsize=12)
        ax.set_xticklabels(["0.5", "0.6", "0.7", "0.8", "0.9", "1"])
        if not is_right:
            ax.set_yticklabels(["0", "0.25", "0.5", "0.75", "1"])

    plot_subplot(axes[0], df_normal, "1D Euclidean (Normal)")
    plot_subplot(axes[1], df_triangle, "1D Euclidean (Triangle)", is_right=True)

    axes[0].set_ylabel("Ratio of Manipulation", fontsize=14, labelpad=10)
    fig.supxlabel("Orness Measure", fontsize=14, y=-0.05)
    plt.subplots_adjust(wspace=0.05)

    handles, labels = axes[1].get_legend_handles_labels()
    axes[1].legend(handles, labels, loc="center left", bbox_to_anchor=(1.02, 0.5), frameon=False, fontsize=12, handlelength=2.5)

    if start_idx is not None and end_idx is not None:
        output_name = f"plot_experiment_1_euclidean_{start_idx}_to_{end_idx}.png"
    else:
        output_name = "plot_experiment_1_euclidean.png"

    plt.savefig(PLOTS_DIRECTORY_PATH / output_name, bbox_inches="tight", dpi=300)
    print(f"Plot saved successfully as '{output_name}'")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot Experiment 1 Euclidean results.")
    parser.add_argument("start", type=int, nargs="?", default=None, help="Start file index (e.g. 0)")
    parser.add_argument("end", type=int, nargs="?", default=None, help="End file index (e.g. 49)")
    args = parser.parse_args()

    plot_experiment_1_euclidean(args.start, args.end)
