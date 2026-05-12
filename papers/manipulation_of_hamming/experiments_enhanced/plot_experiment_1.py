from . import RESULTS_DIRECTORY_PATH, PLOTS_DIRECTORY_PATH
import pandas as pd
import matplotlib.pyplot as plt

def plot_experiment_1():
    # Load both datasets directly
    # Ensure 'uniform.csv' and 'biased.csv' are in the same directory as the script
    df_uniform = pd.read_csv(RESULTS_DIRECTORY_PATH / 'experiment_1_uniform.csv')
    df_biased = pd.read_csv(RESULTS_DIRECTORY_PATH / 'experiment_1_biased.csv')

    # Initialize the figure with 1 row and 2 columns, sharing the y-axis
    fig, axes = plt.subplots(1, 2, figsize=(10, 4), sharey=True)

    # Define line styles and widths for different 'm' values to match the black-and-white print style
    line_styles = {
        5: (0, (5, 5)),  # Thicker standard dashed
        4: (0, (3, 4)),  # Thinner, tighter dashed
        3: (0, (1, 2))   # Dotted
    }

    line_widths = {
        5: 1.8,
        4: 1.2,
        3: 1.2
    }

    def plot_subplot(ax, df, title, is_biased=False):
        # Sort 'm' values descending so the legend displays m=5, m=4, m=3 from top to bottom
        for m in sorted(df['m'].unique(), reverse=True):
            subset = df[df['m'] == m].sort_values('orness')
            
            # Apply specific style and width, fallback to solid line if 'm' is something else
            ls = line_styles.get(m, '-')
            lw = line_widths.get(m, 1.5)
            
            # Plotting with black lines and no markers
            ax.plot(subset['orness'], subset['manipulability'], 
                    label=f'm={m}', color='black', linestyle=ls, linewidth=lw)

        # Set titles (Adding a slight pink background to the 'Biased' title to match your image)
        if is_biased:
            ax.set_title(title, fontsize=14)
        else:
            ax.set_title(title, fontsize=14)

        # Format axis limits and ticks
        ax.set_xlim(0.5, 1.0)
        ax.set_ylim(0, 1.0)
        ax.set_xticks([0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
        ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
        
        # Configure ticks to point inward (direction='in') as seen in the reference image
        ax.tick_params(axis='both', which='major', direction='in', right=True, top=False, labelsize=12)
        ax.set_xticklabels(['0.5', '0.6', '0.7', '0.8', '0.9', '1'])
        if not is_biased:
            ax.set_yticklabels(['0', '0.25', '0.5', '0.75', '1'])
        
    # Plot data on respective subplots
    plot_subplot(axes[0], df_uniform, 'Uniform Elections')
    plot_subplot(axes[1], df_biased, 'Biased Elections', is_biased=True)

    # Set common X and Y labels
    axes[0].set_ylabel('Ratio of Manipulation', fontsize=14, labelpad=10)
    # Use fig.supxlabel for a perfectly centered x-axis label across both subplots
    fig.supxlabel('Orness Measure', fontsize=14, y=-0.05)

    # Remove the space between the two subplots to join the axes
    plt.subplots_adjust(wspace=0.05)

    # Extract legend handles from the second plot and place a single legend outside the axes
    handles, labels = axes[1].get_legend_handles_labels()
    axes[1].legend(handles, labels, loc='center left', bbox_to_anchor=(1.02, 0.5), 
                frameon=False, fontsize=12, handlelength=2.5)

    # Save and display (bbox_inches='tight' prevents the outside legend from getting cut off)
    output_name = 'plot_experiment_1_uniform_and_biased.png'
    plt.savefig(PLOTS_DIRECTORY_PATH / output_name, bbox_inches='tight', dpi=300)
    print(f"Plot saved as '{output_name}'")


if __name__ == "__main__":
    plot_experiment_1()
    