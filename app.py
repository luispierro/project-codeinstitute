from flask import Flask, render_template, request, redirect, send_file
from fpdf import FPDF
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
        # Check the file extension
        if not file.filename.endswith(".csv"):
            return "Invalid file type. Please upload a CSV file.", 400

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

    """
    Generates a correlation heatmap from a DataFrame's numeric columns

    :param df: DataFrame containing the data
    :param output_path: Path to save the generated heatmap image
    """
    # Select only numeric columns
    numeric_df = df.select_dtypes(include=["number"])

    # Calculate the correlation matrix
    correlation_matrix = numeric_df.corr()

    # Create the heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", annot_kws={"size": 8})


    # Save the heatmap as a static image
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path)
    plt.close() 

@app.route("/download")
def download_insights():
    """Export the insights and the correlation heatmap to a PDF file."""
    pdf_filepath = os.path.join("downloads", "report.pdf")
    os.makedirs("downloads", exist_ok=True)

    # Initialize the PDF
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Add a title to the PDF
    pdf.set_font("Arial", style="B", size=16)
    pdf.cell(0, 10, "Insights and Correlation Heatmap", ln=True, align="C")
    pdf.ln(10)

    # Write the insights to the PDF
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, "Insights:", ln=True)
    pdf.ln(5)
    for insight in insights:
        pdf.multi_cell(0, 10, insight)
        pdf.ln(2)
    
    # Add the correlation heatmap to the PDF
    heatmap_path = os.path.join("static", "correlation_matrix.png") 
    if os.path.exists(heatmap_path):
        pdf.set_font("Arial", style="B", size=14)
        pdf.cell(0, 10, "Correlation Heatmap:", ln=True)
        pdf.ln(10)
        pdf.image(heatmap_path, x=10, y=None, w=190) 
    else:
        pdf.ln(10)
        pdf.cell(0, 10, "Correlation heatmap image not found.", ln=True)
    
    # Save the PDF
    pdf.output(pdf_filepath)
    
    # Return the PDF as a downloadable file
    return send_file(pdf_filepath, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)