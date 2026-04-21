from flask import Blueprint, request, jsonify
from services.groq_client import call_groq

report_bp = Blueprint("report", __name__)

def load_prompt(input_text):
    with open("prompts/report.txt", "r") as f:
        template = f.read()
    return template.replace("{input}", input_text)

@report_bp.route("/generate-report", methods=["POST"])
def report():
    data = request.json.get("input")

    if not data:
        return jsonify({"error": "Invalid input"}), 400

    prompt = load_prompt(data)

    response = call_groq(prompt)

    return jsonify({"report": response})