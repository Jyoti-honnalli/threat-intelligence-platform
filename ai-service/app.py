from flask import Flask, request, jsonify
from routes.describe import describe_bp
from routes.recommend import recommend_bp
from routes.report import report_bp

from services.groq_client import generate_response
from middleware.input_sanitizer import sanitize_input
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

VALID_TOKEN = "secure-token-123"

app = Flask(__name__)

# Rate limiter setup
limiter = Limiter(get_remote_address, app=app, default_limits=[])

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

@app.route("/test", methods=["POST"])
@limiter.limit("30 per minute")
def test():
    try:
        auth_header = request.headers.get("Authorization")

        if not auth_header or auth_header != f"Bearer {VALID_TOKEN}":
            return jsonify({
                "status": "error",
                "message": "Unauthorized access"
            }), 401

        data = request.get_json()
        prompt = data.get("prompt", "") if data else ""

        clean_prompt, error = sanitize_input(prompt)

        if error:
            return jsonify({
                "status": "error",
                "message": error
            }), 400

        response = generate_response(clean_prompt)

        return jsonify({
            "status": "success",
            "data": {
                "prompt": clean_prompt,
                "response": response
            }
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.after_request
def secure_headers(response):
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self'; "
        "img-src 'self' data:; "
        "object-src 'none'; "
        "frame-ancestors 'none'; "
        "form-action 'self'; "
        "base-uri 'self';"
    )

    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-XSS-Protection"] = "1; mode=block"

    response.headers.pop("Server", None)

    return response


if __name__ == "__main__":
    app.run(port=5000)