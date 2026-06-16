import argparse
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# Ścieżki importowane z Twojego projektu
from . import RESULTS_DIRECTORY_PATH, PLOTS_DIRECTORY_PATH

def load_and_aggregate_data_exp2(directory_path, start_idx, end_idx):
    """
    Wczytuje pliki eksperymentu 2 z podanego zakresu indeksów i agreguje statystyki
    (średnia, min, max) dla każdej kombinacji reguły 'f' i liczby wyborców 'n'.
    """
    all_dfs = []
    
    for i in range(start_idx, end_idx + 1):
        file_path = directory_path / f'experiment_2_{i}.csv'
        if file_path.exists():
            all_dfs.append(pd.read_csv(file_path))
        else:
            print(f"Ostrzeżenie: Plik {file_path.name} nie istnieje. Pomijam.")
            
    if not all_dfs:
        raise FileNotFoundError(f"Nie znaleziono żadnych plików 'experiment_2_X.csv' w podanym zakresie.")
        
    # Łączymy wszystkie pliki w jeden DataFrame
    combined_df = pd.concat(all_dfs, ignore_index=True)
    
    # Grupowanie po regule 'f' oraz liczbie wyborców 'n'
    aggregated = combined_df.groupby(['f', 'n']).agg(
        mean_manipulability=('manipulability', 'mean'),
        min_manipulability=('manipulability', 'min'),
        max_manipulability=('manipulability', 'max')
    ).reset_index()
    
    return aggregated

def plot_experiment_2(start_idx, end_idx):
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

    # 1. Wczytanie i agregacja danych z wielu plików
    df_agg = load_and_aggregate_data_exp2(RESULTS_DIRECTORY_PATH, start_idx, end_idx)

    # 2. Inicjalizacja wykresu
    fig, ax = plt.subplots(figsize=(8, 5))

    # 3. Definicja stylów linii (LaTeX dla pogrubionych etykiet szeryfowych)
    style_map = {
        'f_2n_3': {'ls': (0, (4, 3)), 'lw': 2.2, 'label': r'$\mathbf{f^{2n/3}}$'},
        'Borda':  {'ls': (0, (1, 2)), 'lw': 2.2, 'label': r'$\mathbf{Borda}$'},
        'f_n_2':  {'ls': (0, (5, 5)), 'lw': 1.2, 'label': r'$\mathbf{f^{n/2}}$'},
        'f_n_3':  {'ls': (0, (1, 3)), 'lw': 1.2, 'label': r'$\mathbf{f^{n/3}}$'}
    }

    # 4. Pętla po unikalnych regułach głosowania
    unique_f = sorted(df_agg['f'].unique(), reverse=True) 

    for rule in unique_f:
        subset = df_agg[df_agg['f'] == rule].sort_values('n')
        
        style = style_map.get(rule, {'ls': '-', 'lw': 1.5, 'label': rule})
        
        # Rysowanie linii średniej dla ratiio of manipulation
        ax.plot(subset['n'], subset['mean_manipulability'], 
                color='black', 
                linestyle=style['ls'], 
                linewidth=style['lw'], 
                label=style['label'])
        
        # Wypełnienie obszaru pomiędzy wartościami minimalnymi a maksymalnymi
        ax.fill_between(subset['n'], 
                        subset['min_manipulability'], 
                        subset['max_manipulability'], 
                        color='black', alpha=0.06)

    # 5. Stylizowanie wykresu
    ax.set_title('Uniform Elections', fontsize=16, pad=15)
    ax.set_xlabel('Number of Voters', fontsize=14, labelpad=10)
    ax.set_ylabel('Ratio of Manipulation', fontsize=14, labelpad=10)

    # Dynamiczne ustawienie limitów osi X na podstawie danych
    ax.set_xlim(df_agg['n'].min(), df_agg['n'].max())
    ax.set_ylim(0.3, 1.0)
    ax.set_yticks([0.3, 0.5, 0.7, 0.9])

    # Ticki skierowane do wewnątrz (direction='in')
    ax.tick_params(axis='both', which='major', direction='in', 
                labelsize=13, length=6, right=False, top=False)

    # Umieszczenie legendy na zewnątrz wykresu
    ax.legend(loc='center left', bbox_to_anchor=(1.0, 0.5), 
            frameon=False, fontsize=15, handlelength=3)

    plt.tight_layout()
    
    # Zapis pliku z uwzględnieniem przetworzonego zakresu w nazwie
    output_name = f'plot_experiment_2_{start_idx}_to_{end_idx}.png'
    plt.savefig(PLOTS_DIRECTORY_PATH / output_name, bbox_inches='tight', dpi=300)
    print(f"Wykres zapisany pomyślnie jako '{output_name}'")


if __name__ == "__main__":
    # Obsługa argumentów z linii komend
    parser = argparse.ArgumentParser(description="Generuj wykres dla Eksperymentu 2 z wielu plików.")
    parser.add_argument("start", type=int, help="Początkowy indeks pliku (np. 0)")
    parser.add_argument("end", type=int, help="Końcowy indeks pliku (np. 24)")
    
    args = parser.parse_args()
    
    plot_experiment_2(args.start, args.end)