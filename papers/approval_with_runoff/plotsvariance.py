from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# 1. Find all results files dynamically
current_dir = Path(__file__).resolve().parent
file_paths = list(current_dir.glob("results*.csv"))

if not file_paths:
    raise FileNotFoundError("No files matching 'results*.csv' found in the directory.")

# 2. Load and combine all DataFrames
df_list = [pd.read_csv(fp) for fp in file_paths]
combined_df = pd.concat(df_list, ignore_index=True)

# 3. Group by parameters to calculate Mean, Min, and Max
# We aggregate 'winner' to find the average along with the absolute minimum and maximum bounds
grouped = (
    combined_df.groupby(['d', 'alpha'])['winner']
    .agg(['mean', 'min', 'max'])
    .reset_index()
)

# Plotting
plt.figure(figsize=(8, 4))

# 4. Plot each 'd' value with its min-max range band
for d_val in grouped['d'].unique():
    subset = grouped[grouped['d'] == d_val]
    
    # Plot the mean line
    line, = plt.plot(subset['alpha'], subset['mean'], label=f'd = {d_val}')
    
    # Set the upper and lower bounds directly to the minimum and maximum values
    lower_bound = subset['min']
    upper_bound = subset['max']
    
    # Add the shaded min-max band using the line's color
    plt.fill_between(
        subset['alpha'], 
        lower_bound.clip(lower=0, upper=1),  # Clip to stay within plot bounds
        upper_bound.clip(lower=0, upper=1), 
        color=line.get_color(), 
        alpha=0.15  # Transparency of the band
    )

plt.axvline(x=0.5, color='black', linestyle='--', label='S-PAV')
plt.title('Position of the second finalist for different values of d (Min-Max Range)')
plt.xlabel('$\\alpha$')
plt.ylabel('distance to center')
plt.ylim(0, 1.0)
plt.xlim(0, 1.0)
plt.legend()
plt.grid(False)
plt.show()