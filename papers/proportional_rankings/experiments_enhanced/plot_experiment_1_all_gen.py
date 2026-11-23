from . import RESULTS_DIRECTORY_PATH, PLOTS_DIRECTORY_PATH
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def _extract_gen_method(filename):
  if (
      isinstance(filename, str)
      and "gen_" in filename
      and "_candidates" in filename
  ):
    return filename.split("gen_")[1].split("_candidates")[0]
  return "unknown"


def plot_all_rules_grid_shuffled():
  # Definicja 12 reguł (3 wiersze x 4 kolumny)
  rules_info = [
      {"title": "AV", "suffix": "av"},
      {"title": "Greedy CC", "suffix": "greedycc"},
      {"title": "Phragmén", "suffix": "phragmen"},
      {"title": "MES", "suffix": "mes"},
      {"title": "5/4-Geometric\nRule", "suffix": "5-4-geometric"},
      {"title": "2-Geometric\nRule", "suffix": "2-geometric"},
      {"title": "10-Geometric\nRule", "suffix": "10-geometric"},
      {"title": "PAV", "suffix": "pav"},
      {"title": "SeqPAV", "suffix": "seqpav"},
      {"title": "Reverse SeqPAV", "suffix": "revseqpav"},
      {"title": "Best-of", "suffix": "bestof"},
      {"title": "Peters", "suffix": "peters"},
  ]

  # Utworzenie siatki 3x4
  fig, axes = plt.subplots(3, 4, figsize=(17, 12))
  axes = axes.flatten()

  # Krok 1: Przejrzenie plików, aby zebrać wszystkie unikalne metody generacji
  all_gen_methods = set()
  for rule in rules_info:
    file_path = RESULTS_DIRECTORY_PATH / f"experiment_1_{rule['suffix']}.csv"
    if os.path.exists(file_path):
      try:
        df = pd.read_csv(file_path)
        if "file" in df.columns:
          for filename in df["file"]:
            method = _extract_gen_method(filename)
            if method != "unknown":
              all_gen_methods.add(method)
      except Exception:
        pass

  # Przypisanie unikalnego koloru dla każdej metody generacji
  sorted_methods = sorted(all_gen_methods)
  cmap_name = "tab20" if len(sorted_methods) > 10 else "tab10"
  color_palette = plt.get_cmap(cmap_name, max(len(sorted_methods), 1))
  method_to_color = {
      method: color_palette(i) for i, method in enumerate(sorted_methods)
  }

  for idx, rule in enumerate(rules_info):
    ax = axes[idx]
    file_path = RESULTS_DIRECTORY_PATH / f"experiment_1_{rule['suffix']}.csv"

    if os.path.exists(file_path):
      try:
        df = pd.read_csv(file_path)

        # Krok 2: Losowe przemieszanie wierszy w DataFrame
        df = df.sample(frac=1).reset_index(drop=True)

        if "file" in df.columns:
          df["gen_method"] = df["file"].apply(_extract_gen_method)
          colors = [
              method_to_color.get(m, "gray") for m in df["gen_method"]
          ]
          ax.scatter(
              df["a"], df["y_r"], color=colors, s=8, edgecolors="none"
          )
        else:
          ax.scatter(
              df["a"], df["y_r"], color="gray", s=8, edgecolors="none"
          )

      except Exception:
        ax.set_facecolor("#ffe6e6")
        ax.text(
            0.5,
            0.5,
            "Błąd pliku",
            color="red",
            ha="center",
            va="center",
            transform=ax.transAxes,
            fontsize=12,
        )
    else:
      ax.set_facecolor("#ffe6e6")
      ax.text(
          0.5,
          0.5,
          "Brak danych",
          color="red",
          ha="center",
          va="center",
          transform=ax.transAxes,
          fontsize=12,
          fontweight="bold",
      )

    # Formatowanie osi i siatki
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(0.0, 1.0)
    ax.set_xticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_xticklabels(["0.0", "0.2", "0.4", "0.6", "0.8", "1.0"], fontsize=8)
    ax.set_yticklabels(["0.0", "0.2", "0.4", "0.6", "0.8", "1.0"], fontsize=8)
    ax.grid(True, linestyle=":", color="gray", alpha=0.6)
    ax.set_xlabel(rule["title"], fontsize=14, labelpad=10)

  # Legenda zbiorcza na podstawie unikalnych metod
  legend_handles = [
      mpatches.Patch(color=method_to_color[m], label=m) for m in sorted_methods
  ]

  if legend_handles:
    fig.subplots_adjust(right=0.78, hspace=0.4, wspace=0.3)
    fig.legend(
        handles=legend_handles,
        loc="center left",
        bbox_to_anchor=(0.80, 0.5),
        title="Generation Method",
        fontsize=10,
        title_fontsize=11,
        frameon=False,
    )
  else:
    plt.tight_layout()
    plt.subplots_adjust(hspace=0.4, wspace=0.3)

  output_name = "plot_experiment_1_all_rules_gen.png"
  plt.savefig(PLOTS_DIRECTORY_PATH / output_name, bbox_inches="tight", dpi=300)
  print(f"Plot saved as '{output_name}'")


if __name__ == "__main__":
  plot_all_rules_grid_shuffled()