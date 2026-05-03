from flask import Flask, jsonify
from dotenv import load_dotenv

load_dotenv()

from routes.describe import describe_bp
from routes.recommend import recommend_bp
from routes.report import report_bp
from services.groq_client import MODEL_NAME
from services.metrics import get_average_response_time_ms, get_uptime_seconds

app = Flask(__name__)

@app.route("/")
def home():
    return "AI Service is running"

@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "model": MODEL_NAME,
        "avg_response_time_ms": get_average_response_time_ms(),
        "uptime_seconds": get_uptime_seconds()
    })

app.register_blueprint(describe_bp)
app.register_blueprint(recommend_bp)
app.register_blueprint(report_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)