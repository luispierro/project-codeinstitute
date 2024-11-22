from flask import Flask, render_template, request, redirect, send_file
import pandas as pd
import os
import seaborn as sns
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
app = Flask(__name__)
# Global variable to hold insights
insights = []
heatmap_path = "static/correlation_matrix.png"
@app.route("/")
def home():
    return render_template("index.html")
@app.route("/upload", methods=["POST"])
def upload_file():
    global insights
    global heatmap_path
    file = request.files.get("file")
    if file:
        # Save the uploaded file temporarily
        filepath = os.path.join("uploads", file.filename)
        os.makedirs("uploads", exist_ok=True)
        file.save(filepath)

        # Process the file
        df = pd.read_csv(filepath)
        insights = analyze_data(df)
        # Return only the updated insights section
        return render_template("insights.html", insights=insights, heatmap_path=heatmap_path)
    else:
        # Return an error message if no file was uploaded
        return "No file uploaded", 400
def analyze_data(df):
    """Generate basic insights from survey data."""
    insights = []

    # Total number of responses
    insights.append(f"Total Responses: {len(df)}")

    # If there are any numeric columns, calculate averages
    numeric_columns = df.select_dtypes(include=["number"]).columns

    for col in numeric_columns:
        avg = df[col].mean()
        insights.append(f"Average {col}: {avg:.2f}")

    # If there are categorical columns, find the most common response
    categorical_columns = df.select_dtypes(include=["object"]).columns

    for col in categorical_columns:
        most_common = df[col].mode()[0]
        insights.append(f"Most common response for '{col}': {most_common}")

    # Generate the correlation heatmap
        generate_correlation_heatmap(df, heatmap_path)

    return insights
def generate_correlation_heatmap(df, output_path="static/correlation_matrix.png"):
    # Select only numeric columns
    numeric_df = df.select_dtypes(include=["number"])

    # Calculate the correlation matrix
    correlation_matrix = numeric_df.corr()

    # Create the heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")

    # Save the heatmap as a static image
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path)
    plt.close()  # Close the figure to free memory
if __name__ == "__main__":
    app.run(debug=True)