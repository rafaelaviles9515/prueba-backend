from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os
from utils.ai import ask_ai_for_suggestions
from utils.data_processor import load_dataframe, build_chart_dataset

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

df_cache = {}  # Simple cache para no recargar el DF en cada petición


@app.route("/api/upload", methods=["POST"])
def upload_file():
    file = request.files.get("file")

    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    df = load_dataframe(filepath)
    df_cache["dataframe"] = df  # Guardar para reusar

    summary = {
        "columns": list(df.columns),
        "dtypes": df.dtypes.astype(str).to_dict(),
        "describe": df.describe(include="all").fillna("").to_dict()
    }

    ai_response = ask_ai_for_suggestions(summary)

    return jsonify({
        "status": "success",
        "suggestions": ai_response
    })


@app.route("/api/chart-data", methods=["POST"])
def chart_data():
    params = request.get_json()

    df = df_cache.get("dataframe")

    if df is None:
        return jsonify({"error": "No dataset loaded"}), 400

    result = build_chart_dataset(df, params)

    return jsonify(result)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
