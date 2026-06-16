from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# Load the existing file directly
df = pd.read_csv(Path(__file__).resolve().parent / "results.csv")

# Plotting
plt.figure(figsize=(8, 4))
for d_val in df['d'].unique():
    subset = df[df['d'] == d_val]
    plt.plot(subset['alpha'], subset['winner'], label=f'd = {d_val}')

plt.axvline(x=0.5, color='black', linestyle='--', label='S-PAV')
plt.title('Position of the second finalist for different values of d')
plt.xlabel('$\\alpha$')
plt.ylabel('distance to center')
plt.ylim(0, 1.0)
plt.xlim(0, 1.0)
plt.legend()
plt.grid(False)
plt.show()