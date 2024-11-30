import os
import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("Agg")  # Use a non-interactive backend for rendering

class SurveyAnalysis:
    def __init__(self):
        self.insights = []
        self.heatmap_path = "static/correlation_matrix.png"

    def analyze_data(self, df):
        """Generate basic insights and heatmap from survey data."""
        self.insights = []

        # Total number of responses
        self.insights.append(f"Total Responses: {len(df)}")

        # Numeric columns: calculate averages
        numeric_columns = df.select_dtypes(include=["number"]).columns
        for col in numeric_columns:
            avg = df[col].mean()
            self.insights.append(f"Average {col}: {avg:.2f}")

        # Categorical columns: find the most common response
        categorical_columns = df.select_dtypes(include=["object"]).columns
        for col in categorical_columns:
            most_common = df[col].mode()[0]
            self.insights.append(f"Most common response for '{col}': {most_common}")

        # Generate correlation heatmap
        self.generate_correlation_heatmap(df)

    def generate_correlation_heatmap(self, df):
        """Generates a correlation heatmap and saves it as an image."""
        numeric_df = df.select_dtypes(include=["number"])
        correlation_matrix = numeric_df.corr()

        plt.figure(figsize=(10, 8))
        sns.heatmap(
            correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f",
            annot_kws={"size": 8}
        )
        os.makedirs(os.path.dirname(self.heatmap_path), exist_ok=True)
        plt.savefig(self.heatmap_path)
        plt.close()