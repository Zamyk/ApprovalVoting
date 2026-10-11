from . import RESULTS_DIRECTORY_PATH, PLOTS_DIRECTORY_PATH
import pandas as pd
import matplotlib.pyplot as plt


def plot_experiment_2():
    # 1. Load your CSV file
    df = pd.read_csv(RESULTS_DIRECTORY_PATH / 'experiment_2.csv')

    # 2. Setup the figure
    fig, ax = plt.subplots(figsize=(8, 5))

    # 3. Define the style mapping to match image_747b54.png
    # We use LaTeX for the bold serif labels and specific dash tuples for lines
    style_map = {
        'f_2n_3': {'ls': (0, (4, 3)), 'lw': 2.2, 'label': r'$\mathbf{f^{2n/3}}$'},
        'Borda':  {'ls': (0, (1, 2)), 'lw': 2.2, 'label': r'$\mathbf{Borda}$'},
        'f_n_2':  {'ls': (0, (5, 5)), 'lw': 1.2, 'label': r'$\mathbf{f^{n/2}}$'},
        'f_n_3':  {'ls': (0, (1, 3)), 'lw': 1.2, 'label': r'$\mathbf{f^{n/3}}$'}
    }

    # 4. Loop through the unique voting rules in your 'f' column
    # We sort them to ensure the legend order matches the reference image
    unique_f = sorted(df['f'].unique(), reverse=True) 

    for rule in unique_f:
        subset = df[df['f'] == rule].sort_values('n')
        
        # Get styles from our map; default to a solid line if the name isn't recognized
        style = style_map.get(rule, {'ls': '-', 'lw': 1.5, 'label': rule})
        
        ax.plot(subset['n'], subset['manipulability'], 
                color='black', 
                linestyle=style['ls'], 
                linewidth=style['lw'], 
                label=style['label'])

    # 5. Styling to match the reference image exactly
    ax.set_title('Uniform Elections', fontsize=16, pad=15)
    ax.set_xlabel('Number of Voters', fontsize=14, labelpad=10)
    ax.set_ylabel('Ratio of Manipulation', fontsize=14, labelpad=10)

    # Set limits and ticks based on your data and the reference image
    ax.set_xlim(df['n'].min(), df['n'].max())
    ax.set_ylim(0.3, 1.0)
    ax.set_yticks([0.3, 0.5, 0.7, 0.9])

    # Ticks pointing inward (direction='in')
    ax.tick_params(axis='both', which='major', direction='in', 
                labelsize=13, length=6, right=False, top=False)

    # Legend placement (outside the plot)
    ax.legend(loc='center left', bbox_to_anchor=(1.0, 0.5), 
            frameon=False, fontsize=15, handlelength=3)

    plt.tight_layout()
    plt.savefig(PLOTS_DIRECTORY_PATH / 'plot_experiment_2.png', bbox_inches='tight', dpi=300)


if __name__ == "__main__":
    plot_experiment_2()
    