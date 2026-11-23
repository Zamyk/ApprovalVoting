from . import RESULTS_DIRECTORY_PATH, PLOTS_DIRECTORY_PATH
import os
import pandas as pd
import matplotlib.pyplot as plt


def plot_all_rules_grid_with_voters():
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

  # Utworzenie siatki 3x4 (zwiększona szerokość dla 4 kolumn i paska kolorów)
  fig, axes = plt.subplots(3, 4, figsize=(17, 12))
  axes = axes.flatten()

  scat = None  # Zmienna do przechowywania obiektu scatter (potrzebna do paska kolorów)

  for idx, rule in enumerate(rules_info):
    ax = axes[idx]

    # Oczekiwana ścieżka do pliku
    file_name = f"experiment_1_{rule['suffix']}.csv"
    file_path = RESULTS_DIRECTORY_PATH / file_name

    if os.path.exists(file_path):
      try:
        df = pd.read_csv(file_path)
        df = df.sample(frac=1).reset_index(drop=True)

        # Rysowanie punktów, gdzie kolor (c) zależy od kolumny 'n_voters'
        scat = ax.scatter(
            df["a"],
            df["y_r"],
            c=df["n_voters"],
            cmap="viridis",
            s=8,
            edgecolors="none",
        )
      except Exception:
        # W razie błędu odczytu
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
      # Jeśli plik nie istnieje -> lekko czerwone tło
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

    # Siatka w kropki
    ax.grid(True, linestyle=":", color="gray", alpha=0.6)

    # Podpis pod każdym subwykresem
    ax.set_xlabel(rule["title"], fontsize=14, labelpad=10)

  # Dodanie wspólnego paska kolorów (colorbar), jeśli udało się narysować wykres
  if scat is not None:
    fig.subplots_adjust(right=0.9, hspace=0.4, wspace=0.3)
    cbar_ax = fig.add_axes([0.92, 0.15, 0.02, 0.7])  # [left, bottom, width, height]
    cbar = fig.colorbar(scat, cax=cbar_ax)
    cbar.set_label("Number of voters", fontsize=12)
  else:
    plt.tight_layout()
    plt.subplots_adjust(hspace=0.4, wspace=0.3)

  # Zapisanie wykresu zbiorczego
  output_name = "plot_experiment_1_all_rules_voters.png"
  plt.savefig(PLOTS_DIRECTORY_PATH / output_name, bbox_inches="tight", dpi=300)
  print(f"Plot saved as '{output_name}'")


if __name__ == "__main__":
  plot_all_rules_grid_with_voters()