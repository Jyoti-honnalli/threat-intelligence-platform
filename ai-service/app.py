```python
from flask import Flask, jsonify, request
from services.groq_client import generate_response
from middleware.input_sanitizer import sanitize_input
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv

from routes.describe import describe_bp
from routes.recommend import recommend_bp
from routes.report import report_bp

# Load environment variables
load_dotenv()

VALID_TOKEN = "secure-token-123"

# Initialize app
app = Flask(__name__)

# Rate limiter
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["10 per minute"]
)

# Rate limit error handler
@app.errorhandler(429)
def rate_limit_handler(e):
    return jsonify({
        "status": "error",
        "message": "Too many requests. Please try again later."
    }), 429


# Home route
@app.route("/")
def home():
    return "AI Service Running"


# Main AI endpoint
@app.route("/test", methods=["POST"])
@limiter.limit("30 per minute")
def test():
    try:
        # JWT / Token check
        auth_header = request.headers.get("Authorization")

        if not auth_header or auth_header != f"Bearer {VALID_TOKEN}":
            return jsonify({
                "status": "error",
                "message": "Unauthorized access"
            }), 401

        # Get JSON data
        data = request.get_json()
        prompt = data.get("prompt", "") if data else ""

        # Sanitize input
        clean_prompt, error = sanitize_input(prompt)

        if error:
            return jsonify({
                "status": "error",
                "message": error
            }), 400

        # Call AI
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


# Security headers
@app.after_request
def secure_headers(response):
    # Content Security Policy
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "frame-ancestors 'none'; "
        "form-action 'self'; "
        "base-uri 'self';"
    )

    # Anti-clickjacking
    response.headers["X-Frame-Options"] = "DENY"

    # MIME sniffing protection
    response.headers["X-Content-Type-Options"] = "nosniff"

    # XSS protection
    response.headers["X-XSS-Protection"] = "1; mode=block"

    # Remove server info
    response.headers.pop("Server", None)

    return response


# Register modular routes
app.register_blueprint(describe_bp)
app.register_blueprint(recommend_bp)
app.register_blueprint(report_bp)


# Run app
if __name__ == "__main__":
    app.run(port=5000)
```
