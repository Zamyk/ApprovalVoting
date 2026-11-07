from . import RESULTS_DIRECTORY_PATH, PLOTS_DIRECTORY_PATH
import os
import pandas as pd
import matplotlib.pyplot as plt

def plot_all_rules_grid_with_candidates():
    # Definicja 9 reguł (wyświetlana nazwa oraz przyrostek w nazwie pliku)
    rules_info = [
        {"title": "AV", "suffix": "av"},
        {"title": "Greedy CC", "suffix": "greedycc"},
        {"title": "Phragmén", "suffix": "phragmen"},
        {"title": "5/4-Geometric\nRule", "suffix": "5_4_geometric"},
        {"title": "2-Geometric\nRule", "suffix": "2_geometric"},
        {"title": "10-Geometric\nRule", "suffix": "10_geometric"},
        {"title": "SeqPAV", "suffix": "seqpav"},
        {"title": "Reverse SeqPAV", "suffix": "reverse_seqpav"},
        {"title": "Best-of", "suffix": "best_of"},
    ]

    # Utworzenie siatki 3x3
    fig, axes = plt.subplots(3, 3, figsize=(13, 12))
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
                
                # Rysowanie punktów, gdzie kolor (c) zależy od kolumny 'candidates'
                scat = ax.scatter(
                    df['a'], df['y_r'], 
                    c=df['candidates'], 
                    cmap='viridis', 
                    s=8, 
                    edgecolors='none'
                )
            except Exception as e:
                # W razie błędu odczytu
                ax.set_facecolor('#ffe6e6')
                ax.text(0.5, 0.5, 'Błąd pliku', color='red', 
                        ha='center', va='center', transform=ax.transAxes, fontsize=12)
        else:
            # Jeśli plik nie istnieje -> lekko czerwone tło
            ax.set_facecolor('#ffe6e6')
            ax.text(0.5, 0.5, 'Brak danych', color='red', 
                    ha='center', va='center', transform=ax.transAxes, fontsize=12, fontweight='bold')

        # Formatting osi i siatki
        ax.set_xlim(0.0, 1.0)
        ax.set_ylim(0.0, 1.0)
        ax.set_xticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
        ax.set_yticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
        ax.set_xticklabels(['0.0', '0.2', '0.4', '0.6', '0.8', '1.0'], fontsize=8)
        ax.set_yticklabels(['0.0', '0.2', '0.4', '0.6', '0.8', '1.0'], fontsize=8)
        
        # Siatka w kropki
        ax.grid(True, linestyle=':', color='gray', alpha=0.6)

        # Podpis pod każdym subwykresem
        ax.set_xlabel(rule['title'], fontsize=14, labelpad=10)

    # Dodanie wspólnego paska kolorów (colorbar), jeśli udało się narysować jakikolwiek wykres
    if scat is not None:
        fig.subplots_adjust(right=0.9, hspace=0.4, wspace=0.3)
        cbar_ax = fig.add_axes([0.92, 0.15, 0.02, 0.7])  # [left, bottom, width, height]
        cbar = fig.colorbar(scat, cax=cbar_ax)
        cbar.set_label('Liczba kandydatów (candidates)', fontsize=12)
    else:
        plt.tight_layout()
        plt.subplots_adjust(hspace=0.4, wspace=0.3)

    # Zapisanie wykresu zbiorczego
    output_name = 'plot_experiment_1_all_rules_candidates.png'
    plt.savefig(PLOTS_DIRECTORY_PATH / output_name, bbox_inches='tight', dpi=300)
    print(f"Plot saved as '{output_name}'")


if __name__ == "__main__":
    plot_all_rules_grid_with_candidates()