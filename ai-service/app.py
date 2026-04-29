from flask import Flask, jsonify
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import blueprints
from routes.describe import describe_bp
from routes.recommend import recommend_bp
from routes.report import report_bp

# Create app
app = Flask(__name__)

# Root route
@app.route("/")
def home():
    return "AI Service is running"

# Health check
@app.route("/health")
def health():
    return jsonify({"status": "ok"})

# Register all routes
app.register_blueprint(describe_bp)
app.register_blueprint(recommend_bp)
app.register_blueprint(report_bp)

# Run server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)