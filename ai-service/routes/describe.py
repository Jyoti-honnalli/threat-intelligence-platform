from flask import Blueprint, request, jsonify
from services.groq_client import call_groq
from datetime import datetime

describe_bp = Blueprint("describe", __name__)

def load_prompt(input_text):
    with open("prompts/describe.txt", "r") as f:
        template = f.read()
    return template.replace("{input}", input_text)

@describe_bp.route("/describe", methods=["POST"])
def describe():
    data = request.json.get("input")

    if not data:
        return jsonify({"error": "Invalid input"}), 400

    prompt = load_prompt(data)

    response = call_groq(prompt)

    return jsonify({
        "result": response,
        "generated_at": datetime.now().isoformat()
    })