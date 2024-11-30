from flask import Flask, render_template, request, send_file
from models import SurveyAnalysis
import os
import pandas as pd

app = Flask(__name__)
survey_analysis = SurveyAnalysis()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files.get("file")
    if file:
        if not file.filename.endswith(".csv"):
            return "Invalid file type. Please upload a CSV file.", 400

        filepath = os.path.join("uploads", file.filename)
        os.makedirs("uploads", exist_ok=True)
        file.save(filepath)

        df = pd.read_csv(filepath)
        survey_analysis.analyze_data(df)

        return render_template(
            "insights.html",
            insights=survey_analysis.insights,
            heatmap_path=survey_analysis.heatmap_path
        )
    else:
        return "No file uploaded", 400

@app.route("/download")
def download_insights():
    # Same logic for downloading the PDF
    pass

if __name__ == "__main__":
    app.run(debug=True)