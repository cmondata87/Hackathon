# /financial-coach-backend/main.py
import functions_framework
from flask import jsonify
from vertexai.generative_models import GenerativeModel
import json

model = GenerativeModel("gemini-1.5-flash-001")

@functions_framework.http
def financial_coach_agent(request):
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        return ('', 204, headers)

    headers = {'Access-Control-Allow-Origin': '*'}
    request_json = request.get_json(silent=True)
    if not request_json or 'prompt' not in request_json:
        return (jsonify({"error": "Invalid request: 'prompt' is required."}), 400, headers)

    prompt = request_json['prompt']

    try:
        response = model.generate_content(prompt)
        response_text = response.candidates[0].content.parts[0].text
        return (jsonify({"response": response_text}), 200, headers)
    except Exception as e:
        print(f"Error calling Vertex AI: {e}")
        return (jsonify({"error": "An error occurred."}), 500, headers)