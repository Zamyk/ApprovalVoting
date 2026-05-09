import pandas as pd
import matplotlib.pyplot as plt


name = input()
df = pd.read_csv(name)

# Initialize the plot
plt.figure(figsize=(10, 6))

for m in df['m'].unique():
    subset = df[df['m'] == m]
    # Sorting by orness to ensure the line is drawn correctly
    subset = subset.sort_values('orness')
    plt.plot(subset['orness'], subset['manipulability'], label=f'm = {m} candidates', marker='o', markersize=4)

# Formatting the chart
plt.title('title')
plt.xlabel('Orness')
plt.ylabel('Manipulability Ratio')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.ylim(0, 1.05)

plt.savefig(f'{name}_manipulability_plot.png')
print(f"Plot saved as '{name}_manipulability_plot.png'")