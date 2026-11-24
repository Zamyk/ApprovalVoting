from . import RESULTS_DIRECTORY_PATH, PLOTS_DIRECTORY_PATH
import os
import pandas as pd
import matplotlib.pyplot as plt

def plot_all_rules_grid():
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

    # Utworzenie siatki 3x4 (zwiększona szerokość do 16 cali)
    fig, axes = plt.subplots(3, 4, figsize=(16, 12))
    axes = axes.flatten()

    for idx, rule in enumerate(rules_info):
        ax = axes[idx]
        
        # Oczekiwana ścieżka do pliku
        file_name = f"experiment_1_datasets-2_{rule['suffix']}.csv"
        file_path = RESULTS_DIRECTORY_PATH / file_name

        if os.path.exists(file_path):
            try:
                df = pd.read_csv(file_path)
                
                # Rysowanie szarych punktów o pełnej intensywności (bez alpha)
                ax.scatter(df['a'], df['y_r'], color='gray', s=8, edgecolors='none')
            except Exception as e:
                # W razie błędu odczytu (np. pusty plik)
                ax.set_facecolor('#ffe6e6')
                ax.text(0.5, 0.5, 'Błąd pliku', color='red', 
                        ha='center', va='center', transform=ax.transAxes, fontsize=12)
        else:
            # Jeśli plik nie istnieje -> lekko czerwone tło (#ffe6e6 / lightpink)
            ax.set_facecolor('#ffe6e6')
            ax.text(0.5, 0.5, 'Brak danych', color='red', 
                    ha='center', va='center', transform=ax.transAxes, fontsize=12, fontweight='bold')

        # Formatting osi i siatki (zgodny z układem z oryginalnego obrazu)
        ax.set_xlim(0.0, 1.0)
        ax.set_ylim(0.0, 1.0)
        ax.set_xticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
        ax.set_yticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
        ax.set_xticklabels(['0.0', '0.2', '0.4', '0.6', '0.8', '1.0'], fontsize=8)
        ax.set_yticklabels(['0.0', '0.2', '0.4', '0.6', '0.8', '1.0'], fontsize=8)
        
        # Siatka w kropki
        ax.grid(True, linestyle=':', color='gray', alpha=0.6)

        # Podpis pod każdym subwykresem (nazwa reguły)
        ax.set_xlabel(rule['title'], fontsize=14, labelpad=10)

    # Dostosowanie odstępów między wykresami
    plt.tight_layout()
    plt.subplots_adjust(hspace=0.4, wspace=0.3)

    # Zapisanie wykresu zbiorczego
    output_name = 'plot_experiment_1_datasets-2_all_rules.png'
    plt.savefig(PLOTS_DIRECTORY_PATH / output_name, bbox_inches='tight', dpi=300)
    print(f"Plot saved as '{output_name}'")


if __name__ == "__main__":
    plot_all_rules_grid()