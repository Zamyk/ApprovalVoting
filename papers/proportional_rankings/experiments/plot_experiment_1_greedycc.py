from . import RESULTS_DIRECTORY_PATH, PLOTS_DIRECTORY_PATH
import pandas as pd
import matplotlib.pyplot as plt

def plot_scatter_a_yr_greedycc():
    # Wczytaj zbiór danych zawierający kolumny 'a' oraz 'y_r'
    df = pd.read_csv(RESULTS_DIRECTORY_PATH / 'experiment_1_greedycc.csv')

    # Inicjalizacja pojedynczego wykresu
    fig, ax = plt.subplots(figsize=(6, 5))

    # Wykres rozrzutu: brak parametru alpha (lub alpha=1.0) sprawia,
    # że każdy punkt ma od razu maksymalną, stałą szarość.
    ax.scatter(df['a'], df['y_r'], color='gray', s=10, edgecolors='none')

    # Ustawienie zakresów osi od 0.0 do 1.0
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(0.0, 1.0)

    # Definicja podziałki (ticks)
    ax.set_xticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])

    # Włączenie siatki z liniami przerywanymi
    ax.grid(True, linestyle=':', color='gray', alpha=0.7)

    # Etykiety osi
    ax.set_xlabel('a', fontsize=12)
    ax.set_ylabel('y_r', fontsize=12)

    # Konfiguracja parametrów ticków
    ax.tick_params(axis='both', which='major', labelsize=10)

    # Zapisanie wykresu
    output_name = 'plot_scatter_a_yr_greedycc.png'
    plt.savefig(PLOTS_DIRECTORY_PATH / output_name, bbox_inches='tight', dpi=300)
    print(f"Plot saved as '{output_name}'")


if __name__ == "__main__":
    plot_scatter_a_yr_greedycc()