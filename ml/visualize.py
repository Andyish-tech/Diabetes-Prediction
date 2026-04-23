import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def generate_visualizations():
    print("Loading data for visualization...")
    # Load dataset
    data_path = os.path.join(os.path.dirname(__file__), '..', 'diabetes.csv')
    df = pd.read_csv(data_path)

    # Set up styling
    sns.set_theme(style="whitegrid", palette="muted")
    
    # Save directory
    save_dir = r"C:\Users\mario\.gemini\antigravity\brain\7c88de29-291f-440d-96b4-78559277913a"

    print("Generating Correlation Heatmap...")
    plt.figure(figsize=(10, 8))
    corr = df.corr()
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
    plt.title("Feature Correlation Heatmap", fontsize=16)
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, "heatmap.png"), dpi=300)
    plt.close()

    print("Generating Outcome Distribution plot...")
    plt.figure(figsize=(6, 5))
    ax = sns.countplot(x='Outcome', data=df)
    plt.title("Distribution of Diabetic vs Non-Diabetic Patients", fontsize=14)
    ax.set_xticklabels(["Not Diabetic (0)", "Diabetic (1)"])
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, "outcome_dist.png"), dpi=300)
    plt.close()

    print("Generating Glucose vs Age scatter plot...")
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x='Age', y='Glucose', hue='Outcome', data=df, alpha=0.7)
    plt.title("Glucose Levels vs Age by Outcome", fontsize=14)
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, "glucose_age.png"), dpi=300)
    plt.close()

    print("Generating BMI Distribution Violin Plot...")
    plt.figure(figsize=(8, 6))
    sns.violinplot(x='Outcome', y='BMI', data=df, inner="quartile")
    plt.title("BMI Distribution by Outcome", fontsize=14)
    plt.xticks([0, 1], ["Not Diabetic", "Diabetic"])
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, "bmi_violin.png"), dpi=300)
    plt.close()

    print("Visualizations generated successfully!")

if __name__ == '__main__':
    generate_visualizations()
