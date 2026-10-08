import argparse
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

from . import RESULTS_DIRECTORY_PATH, PLOTS_DIRECTORY_PATH


def load_and_aggregate_data_exp2(directory_path, prefix, start_idx=None, end_idx=None):
    """
    Loads Euclidean experiment 2 CSVs. Supports both a single file and a range of index files.
    """
    all_dfs = []
    if start_idx is not None and end_idx is not None:
        for i in range(start_idx, end_idx + 1):
            file_path = directory_path / f"experiment_2_euclidean_{prefix}_{i}.csv"
            if file_path.exists():
                all_dfs.append(pd.read_csv(file_path))
            else:
                print(f"Warning: File {file_path.name} not found. Skipping.")
    else:
        single_file = directory_path / f"experiment_2_euclidean_{prefix}.csv"
        if single_file.exists():
            all_dfs.append(pd.read_csv(single_file))
        else:
            indexed_files = sorted(directory_path.glob(f"experiment_2_euclidean_{prefix}_*.csv"))
            for f in indexed_files:
                all_dfs.append(pd.read_csv(f))

    if not all_dfs:
        raise FileNotFoundError(f"No files found for prefix 'experiment_2_euclidean_{prefix}' in {directory_path}")

    combined_df = pd.concat(all_dfs, ignore_index=True)
    aggregated = (
        combined_df.groupby(["f", "n"])
        .agg(
            mean_manipulability=("manipulability", "mean"),
            min_manipulability=("manipulability", "min"),
            max_manipulability=("manipulability", "max"),
        )
        .reset_index()
    )
    return aggregated


def plot_experiment_2_euclidean(start_idx=None, end_idx=None):
    plt.rcParams.update({
        "text.color": "black",
        "axes.labelcolor": "black",
        "axes.edgecolor": "black",
        "xtick.color": "black",
        "ytick.color": "black",
        "axes.titlecolor": "black",
    })

    df_normal = load_and_aggregate_data_exp2(RESULTS_DIRECTORY_PATH, "normal", start_idx, end_idx)
    df_triangle = load_and_aggregate_data_exp2(RESULTS_DIRECTORY_PATH, "triangle", start_idx, end_idx)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)

    style_map = {
        "f_2n_3": {"ls": (0, (4, 3)), "lw": 2.2, "label": r"$\mathbf{f^{2n/3}}$"},
        "Borda":  {"ls": (0, (1, 2)), "lw": 2.2, "label": r"$\mathbf{Borda}$"},
        "f_n_2":  {"ls": (0, (5, 5)), "lw": 1.2, "label": r"$\mathbf{f^{n/2}}$"},
        "f_n_3":  {"ls": (0, (1, 3)), "lw": 1.2, "label": r"$\mathbf{f^{n/3}}$"},
    }

    def plot_subplot(ax, df_agg, title, is_right=False):
        unique_f = sorted(df_agg["f"].unique(), reverse=True)
        for rule in unique_f:
            subset = df_agg[df_agg["f"] == rule].sort_values("n")
            style = style_map.get(rule, {"ls": "-", "lw": 1.5, "label": rule})

            ax.plot(
                subset["n"],
                subset["mean_manipulability"],
                color="black",
                linestyle=style["ls"],
                linewidth=style["lw"],
                label=style["label"],
            )
            ax.fill_between(
                subset["n"],
                subset["min_manipulability"],
                subset["max_manipulability"],
                color="black",
                alpha=0.06,
            )

        ax.set_title(title, fontsize=16, pad=15)
        ax.set_xlabel("Number of Voters", fontsize=14, labelpad=10)
        ax.set_xlim(df_agg["n"].min(), df_agg["n"].max())
        ax.set_ylim(0.0, 1.0)
        ax.set_yticks([0.0, 0.25, 0.5, 0.75, 1.0])
        ax.tick_params(axis="both", which="major", direction="in", labelsize=13, length=6, right=False, top=False)
        if not is_right:
            ax.set_ylabel("Ratio of Manipulation", fontsize=14, labelpad=10)

    plot_subplot(axes[0], df_normal, "1D Euclidean (Normal)")
    plot_subplot(axes[1], df_triangle, "1D Euclidean (Triangle)", is_right=True)

    plt.subplots_adjust(wspace=0.08)

    handles, labels = axes[1].get_legend_handles_labels()
    axes[1].legend(handles, labels, loc="center left", bbox_to_anchor=(1.02, 0.5), frameon=False, fontsize=15, handlelength=3)

    if start_idx is not None and end_idx is not None:
        output_name = f"plot_experiment_2_euclidean_{start_idx}_to_{end_idx}.png"
    else:
        output_name = "plot_experiment_2_euclidean.png"

    plt.savefig(PLOTS_DIRECTORY_PATH / output_name, bbox_inches="tight", dpi=300)
    print(f"Plot saved successfully as '{output_name}'")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot Experiment 2 Euclidean results.")
    parser.add_argument("start", type=int, nargs="?", default=None, help="Start file index (e.g. 0)")
    parser.add_argument("end", type=int, nargs="?", default=None, help="End file index (e.g. 49)")
    args = parser.parse_args()

    plot_experiment_2_euclidean(args.start, args.end)
