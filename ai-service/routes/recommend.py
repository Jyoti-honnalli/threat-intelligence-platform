from flask import Blueprint, request, jsonify
from services.groq_client import call_groq

recommend_bp = Blueprint("recommend", __name__)

def load_prompt(input_text):
    with open("prompts/recommend.txt", "r") as f:
        template = f.read()
    return template.replace("{input}", input_text)

@recommend_bp.route("/recommend", methods=["POST"])
def recommend():
    data = request.json.get("input")

    if not data:
        return jsonify({"error": "Invalid input"}), 400

    prompt = load_prompt(data)

    response = call_groq(prompt)

    return jsonify({"result": response})