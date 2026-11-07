from . import RESULTS_DIRECTORY_PATH, PLOTS_DIRECTORY_PATH
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.patches as mpatches

def plot_all_rules_grid_shuffled():
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
    fig, axes = plt.subplots(3, 3, figsize=(14, 12))
    axes = axes.flatten()

    # Krok 1: Przejrzenie plików, aby zebrać wszystkie unikalne metody generacji (dla spójnej palety kolorów)
    all_gen_methods = set()
    for rule in rules_info:
        file_path = RESULTS_DIRECTORY_PATH / f"experiment_1_{rule['suffix']}.csv"
        if os.path.exists(file_path):
            try:
                df = pd.read_csv(file_path)
                if 'file' in df.columns:
                    for filename in df['file']:
                        if 'gen_' in filename and '_candidates' in filename:
                            method = filename.split('gen_')[1].split('_candidates')[0]
                            all_gen_methods.add(method)
            except Exception:
                pass

    # Przypisanie unikalnego koloru dla każdej metody generacji
    sorted_methods = sorted(list(all_gen_methods))
    color_palette = cm.get_cmap('tab10', max(len(sorted_methods), 1))
    method_to_color = {method: color_palette(i) for i, method in enumerate(sorted_methods)}

    for idx, rule in enumerate(rules_info):
        ax = axes[idx]
        file_path = RESULTS_DIRECTORY_PATH / f"experiment_1_{rule['suffix']}.csv"

        if os.path.exists(file_path):
            try:
                df = pd.read_csv(file_path)
                
                # Krok 2: Losowe przemieszanie (wymieszanie) wierszy w DataFrame
                df = df.sample(frac=1).reset_index(drop=True)

                if 'file' in df.columns:
                    methods = []
                    for filename in df['file']:
                        try:
                            m = filename.split('gen_')[1].split('_candidates')[0]
                            methods.append(m)
                        except Exception:
                            methods.append('unknown')
                    df['gen_method'] = methods

                    # Przygotowanie listy kolorów dla każdego punktu w losowej kolejności
                    colors = [method_to_color.get(m, 'gray') for m in df['gen_method']]

                    # Rysowanie wszystkich punktów naraz w przemieszanej kolejności
                    ax.scatter(
                        df['a'], df['y_r'], 
                        color=colors, 
                        s=8, 
                        edgecolors='none'
                    )
                else:
                    ax.scatter(df['a'], df['y_r'], color='gray', s=8, edgecolors='none')

            except Exception as e:
                ax.set_facecolor('#ffe6e6')
                ax.text(0.5, 0.5, 'Błąd pliku', color='red', 
                        ha='center', va='center', transform=ax.transAxes, fontsize=12)
        else:
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
        ax.grid(True, linestyle=':', color='gray', alpha=0.6)
        ax.set_xlabel(rule['title'], fontsize=14, labelpad=10)

    # Stworzenie elementów do legendy zbiorczej na podstawie unikalnych metod
    legend_handles = [
        mpatches.Patch(color=method_to_color[m], label=m) 
        for m in sorted_methods
    ]

    if legend_handles:
        fig.subplots_adjust(right=0.8, hspace=0.4, wspace=0.3)
        fig.legend(
            handles=legend_handles, 
            loc='center left', 
            bbox_to_anchor=(0.82, 0.5), 
            title="Sposób generacji",
            fontsize=10,
            title_fontsize=11,
            frameon=False
        )
    else:
        plt.tight_layout()
        plt.subplots_adjust(hspace=0.4, wspace=0.3)

    # Zapisanie wykresu zbiorczego
    output_name = 'plot_experiment_1_all_gen.png'
    plt.savefig(PLOTS_DIRECTORY_PATH / output_name, bbox_inches='tight', dpi=300)
    print(f"Plot saved as '{output_name}'")


if __name__ == "__main__":
    plot_all_rules_grid_shuffled()