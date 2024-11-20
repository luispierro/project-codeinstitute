from flask import Flask, render_template, request, redirect, send_file
import pandas as pd
import os
app = Flask(__name__)
# Global variable to hold insights
insights = []
@app.route("/")
def home():
    return render_template("index.html")
@app.route("/upload", methods=["POST"])
def upload_file():
    global insights
    file = request.files.get("file")
    if file:
        # Save the uploaded file temporarily
        filepath = os.path.join("uploads", file.filename)
        os.makedirs("uploads", exist_ok=True)
        file.save(filepath)
        # Process the file
        df = pd.read_csv(filepath)
        insights = analyze_data(df)
        return render_template("index.html", insights=insights)
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
    return insights
if __name__ == "__main__":
    app.run(debug=True)