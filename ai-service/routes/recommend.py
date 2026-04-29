from flask import Blueprint, request, jsonify
from services.groq_client import call_groq

recommend_bp = Blueprint("recommend", __name__)

@recommend_bp.route("/recommend", methods=["POST"])
def recommend():
    data = request.json.get("input")

    if not data:
        return jsonify({"error": "Invalid input"}), 400

    # Structured prompt
    prompt = f"""
Given the cybersecurity threat below, return ONLY valid JSON.

Threat:
{data}

Instructions:
- Return exactly 3 recommendations
- Output must be a JSON array
- Do NOT include any text outside JSON
- Do NOT include markdown

Format:
[
  {{
    "action_type": "",
    "description": "",
    "priority": "Low | Medium | High"
  }}
]
"""

    response = call_groq(prompt)

    return jsonify({
        "result": response,
        "generated_at": "timestamp"
    })