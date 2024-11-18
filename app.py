from flask import Flask, render_template, request, redirect, send_file
import pandas as pd
import os
app = Flask(__name__)
@app.route("/")
def home():
    return render_template("index.html")
@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files.get("file")
    if file:
        # Save the uploaded file temporarily
        filepath = os.path.join("uploads", file.filename)
        os.makedirs("uploads", exist_ok=True)
        file.save(filepath)
        # Process the file
        df = pd.read_csv(filepath)
        # Return a simple "OK" response and end
        return "OK", 200
    else:
        # Return an error message if no file was uploaded
        return "No file uploaded", 400
    return redirect("/")
if __name__ == "__main__":
    app.run(debug=True)