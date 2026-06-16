import argparse
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# Zakładam, że te ścieżki są importowane z Twojego projektu
# Jeśli uruchamiasz to jako skrypt, upewnij się, że __init__.py lub struktura folderów na to pozwala
from . import RESULTS_DIRECTORY_PATH, PLOTS_DIRECTORY_PATH

def load_and_aggregate_data(directory_path, prefix, start_idx, end_idx):
    """
    Ładuje pliki z danego zakresu indeksów i agreguje statystyki
    (średnia, wariancja, min, max) dla każdej kombinacji 'm' i 'orness'.
    """
    all_dfs = []
    
    for i in range(start_idx, end_idx + 1):
        file_path = directory_path / f'experiment_1_{prefix}_{i}.csv'
        if file_path.exists():
            all_dfs.append(pd.read_csv(file_path))
        else:
            print(f"Ostrzeżenie: Plik {file_path.name} nie istnieje. Pomijam.")
            
    if not all_dfs:
        raise FileNotFoundError(f"Nie znaleziono żadnych plików dla prefiksu '{prefix}' w podanym zakresie.")
        
    # Łączymy wszystkie pliki w jeden duży DataFrame
    combined_df = pd.concat(all_dfs, ignore_index=True)
    
    # Grupowanie po parametrach 'm' oraz 'orness' i wyliczanie statystyk
    aggregated = combined_df.groupby(['m', 'orness']).agg(
        mean_manipulability=('manipulability', 'mean'),
        min_manipulability=('manipulability', 'min'),
        max_manipulability=('manipulability', 'max')
    ).reset_index()
    
    return aggregated

def plot_experiment_1(start_idx, end_idx):
    # === JEDNA WSTAWKA DO ZMIANY KOLORU NA CZERWONY ===
    plt.rcParams.update({
        'text.color': 'black',          # Kolor napisów (np. legenda)
        'axes.labelcolor': 'black',     # Kolor opisów osi X i Y
        'axes.edgecolor': 'black',      # Kolor ramek wykresu
        'xtick.color': 'black',         # Kolor wartości i kresek osi X
        'ytick.color': 'black',         # Kolor wartości i kresek osi Y
        'axes.titlecolor': 'black'      # Kolor tytułu wykresu
    })
    # =================================================

    # Ładowanie i agregacja danych z wielu plików
    df_uniform = load_and_aggregate_data(RESULTS_DIRECTORY_PATH, 'uniform', start_idx, end_idx)
    df_biased = load_and_aggregate_data(RESULTS_DIRECTORY_PATH, 'biased', start_idx, end_idx)

    # Inicjalizacja wykresu
    fig, axes = plt.subplots(1, 2, figsize=(10, 4), sharey=True)

    # Style linii dla zachowania czarno-białego stylu wydruku
    line_styles = {
        5: (0, (5, 5)),  # Przerywana gruba
        4: (0, (3, 4)),  # Przerywana cienka
        3: (0, (1, 2))   # Kropkowana
    }

    line_widths = {
        5: 1.8,
        4: 1.2,
        3: 1.2
    }

    def plot_subplot(ax, df, title, is_biased=False):
        # Sortujemy 'm' malejąco, aby legenda była w kolejności m=5, 4, 3
        for m in sorted(df['m'].unique(), reverse=True):
            subset = df[df['m'] == m].sort_values('orness')
            
            ls = line_styles.get(m, '-')
            lw = line_widths.get(m, 1.5)
            
            # 1. Rysowanie linii średniej (główna oś wykresu)
            ax.plot(subset['orness'], subset['mean_manipulability'], 
                    label=f'm={m}', color='black', linestyle=ls, linewidth=lw)
            
            # 2. Zaznaczanie obszaru min-max (Wariancja / Zakres eksperymentów)
            # alpha=0.1 daje delikatne tło, które nie zaburzy czarno-białego stylu
            ax.fill_between(subset['orness'], 
                            subset['min_manipulability'], 
                            subset['max_manipulability'], 
                            color='black', alpha=0.08)

        # Formatowanie osi i wyglądu (zgodnie z Twoim oryginalnym kodem)
        ax.set_title(title, fontsize=14)
        ax.set_xlim(0.5, 1.0)
        ax.set_ylim(0, 1.0)
        ax.set_xticks([0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
        ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
        
        ax.tick_params(axis='both', which='major', direction='in', right=True, top=False, labelsize=12)
        ax.set_xticklabels(['0.5', '0.6', '0.7', '0.8', '0.9', '1'])
        if not is_biased:
            ax.set_yticklabels(['0', '0.25', '0.5', '0.75', '1'])
        
    # Plotowanie
    plot_subplot(axes[0], df_uniform, 'Uniform Elections')
    plot_subplot(axes[1], df_biased, 'Biased Elections', is_biased=True)

    # Etykiety osi
    axes[0].set_ylabel('Ratio of Manipulation', fontsize=14, labelpad=10)
    fig.supxlabel('Orness Measure', fontsize=14, y=-0.05)

    # Połączenie wykresów (brak przerwy między kolumnami)
    plt.subplots_adjust(wspace=0.05)

    # Legenda na zewnątrz po prawej stronie
    handles, labels = axes[1].get_legend_handles_labels()
    axes[1].legend(handles, labels, loc='center left', bbox_to_anchor=(1.02, 0.5), 
                frameon=False, fontsize=12, handlelength=2.5)

    # Zapis pliku
    output_name = f'plot_experiment_1_{start_idx}_to_{end_idx}.png'
    plt.savefig(PLOTS_DIRECTORY_PATH / output_name, bbox_inches='tight', dpi=300)
    print(f"Plot saved successfully as '{output_name}'")


if __name__ == "__main__":
    # Konfiguracja parsera argumentów linii komend
    parser = argparse.ArgumentParser(description="Generuj wykres z zagregowanych plików eksperymentów.")
    parser.add_argument("start", type=int, help="Początkowy indeks pliku (np. 0)")
    parser.add_argument("end", type=int, help="Końcowy indeks pliku (np. 24)")
    
    args = parser.parse_args()
    
    # Wywołanie głównej funkcji z przekazanymi parametrami
    plot_experiment_1(args.start, args.end)