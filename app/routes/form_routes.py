import json
from app.util.temp import trail_recommendation
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
    difficulty = request.form['difficulty']
    min_length = request.form['minLength']
    max_length = request.form['maxLength']
    max_elevation_gain = request.form['maxElevationGain']

    prompt = f"""
        Considering the following criteria:
        - Date: {date}
        - Maximum Drive Time from Start Location: {max_drive_time} hours
        - Start Location: {start_location}
        - Difficulty: {difficulty}
        - Length of Hike: {min_length} to {max_length} miles
        - Maximum Elevation Gain: {max_elevation_gain} feet
        - Additional Preferences: {prompt_field}

        Please provide a list of the best possible hikes that meet these criteria, formatted as JSON. Each hike should include its name and relevant metadata. The response should be structured as follows:

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
        print(trail_recommendation(date, max_drive_time, start_location, prompt_field, difficulty, min_length, max_length, max_elevation_gain))
        response = chat_gpt_service.prompt_chat_gpt(prompt)
        hikes_response = json.loads(
            response["choices"][0]["message"]["content"])
        return render_template("response.html", hikes_response=hikes_response)

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Failed to process the request"}), 500
