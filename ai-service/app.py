from flask import Flask
from routes.describe import describe_bp
from routes.recommend import recommend_bp
from routes.report import report_bp

app = Flask(__name__)

@app.route("/")
def home():
    return "AI Service is running"

@app.route("/health")
def health():
    return {"status": "ok"}

# Register all routes
app.register_blueprint(describe_bp)
app.register_blueprint(recommend_bp)
app.register_blueprint(report_bp)

if __name__ == "__main__":
    app.run(port=5000)