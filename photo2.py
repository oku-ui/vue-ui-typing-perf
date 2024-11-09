import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# General style settings
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("Set2")

# Data validation and cleaning
def validate_data(df):
    if df.isnull().values.any():
        print("Warning: Missing values found in the dataset! Filling missing values with the mean...")
        df = df.fillna(df.mean())
    return df

# Heatmap
def create_heatmap(data, ax, title):
    sns.heatmap(data.corr(), annot=True, cmap="coolwarm", fmt=".2f", ax=ax, cbar=True)
    ax.set_title(f"{title} - Correlation Heatmap", fontsize=14)

# Swarmplot
def create_swarmplot(data, ax, title):
    sns.swarmplot(data=data, ax=ax, palette="husl", size=5)
    ax.set_title(f"{title} - Swarmplot", fontsize=14)
    ax.set_ylabel("Completion Time (ms)")

# Line plot
def create_lineplot(data, ax, title):
    for col in data.columns:
        ax.plot(data.index, data[col], marker="o", label=col)
    ax.set_title(f"{title} - Line Plot", fontsize=14)
    ax.set_xlabel("Samples")
    ax.set_ylabel("Completion Time (ms)")
    ax.legend(loc="best", fontsize=10)

# Select top two fastest libraries
def select_top_two_libraries(data):
    mean_times = data.mean().sort_values()
    return mean_times.head(5).index.tolist()

# Main visualization function
def create_combined_visualization(files):
    for file, title, _ in files:
        # Load and validate data
        df = pd.read_csv(file, sep='\t')
        data = df.iloc[:, 1:]
        data = validate_data(data)

        # Main visualizations (Boxplot and Violin Plot)
        fig, axes = plt.subplots(2, 2, figsize=(14, 12))
        fig.suptitle(f"{title} - Visualizations", fontsize=16, fontweight='bold')

        # Heatmap
        create_heatmap(data, axes[0, 0], title)

        # Swarmplot
        create_swarmplot(data, axes[0, 1], title)

        # Line plot
        create_lineplot(data, axes[1, 0], title)

        # Top 2 fastest libraries analysis
        top_two = select_top_two_libraries(data)
        filtered_data = data[top_two]

        # Bar Plot
        sns.barplot(data=filtered_data, ax=axes[1, 1], palette="pastel", ci="sd")
        axes[1, 1].set_title(f"{title} - Top 2 Bar Plot", fontsize=14)
        axes[1, 1].set_ylabel("Completion Time (ms)")
        axes[1, 1].set_xlabel("Frameworks")

        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.savefig(f"temp/{title}_combined_analysis.png", dpi=300, bbox_inches="tight")
        plt.close()

        print(f"Visualizations for {title} completed.")
        print(f"Top 2 fastest libraries: {top_two}")

# File information
files = [
    ('temp/setup_function_completion.tsv', 'Setup Function Completion', 'setup_performance'),
    ('temp/global_completion.tsv', 'Global Completion', 'global_performance'),
    ('temp/path_completion.tsv', 'Path Completion', 'path_performance')
]

# Run the combined visualization
create_combined_visualization(files)

print("All visualizations are complete!")