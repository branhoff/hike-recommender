import json
from flask import Blueprint, request, render_template, Response, jsonify

from app.services import chat_gpt_service

form_bp = Blueprint("form_bp", __name__)


@form_bp.route("/")
def home() -> Response:
    return render_template("form.html")


@form_bp.route('/submit-form', methods=['POST'])
def handle_data():
    date = request.form['date']
    max_drive_time = request.form['maxDriveTime']
    start_location = request.form['startLocation']
    prompt_field = request.form['promptField']

    prompt = f"""
    Considering the following criteria:
    - Date: {date}
    - Maximum Drive Time from Start Location: {max_drive_time} hours
    - Start Location: {start_location}
    - Additional Preferences: {prompt_field}

    Please provide a list of the best possible hikes that meet these criteria, formatted as JSON. Each hike should include its name and relevant metadata such as difficulty level, estimated duration, and key features. The response should look something like this example:

    {{
        "hikes": [
            {{
                "name": "Example Hike Name",
                "metadata": {{
                    "difficulty": "Moderate",
                    "duration": "4 hours",
                    "features": ["waterfall", "forest views"]
                }}
            }}
        ]
    }}

    Generate a list based on the criteria provided.
    """

    try:
        response = chat_gpt_service.prompt_chat_gpt(prompt)
        hikes_response = json.loads(
            response["choices"][0]["message"]["content"])
        return render_template("response.html", hikes_response=hikes_response)

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Failed to process the request"}), 500
