from flask import Blueprint, redirect, request, render_template, Response, \
    url_for, jsonify

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
    On {date}, I'm looking for a hiking adventure. I can drive up to {max_drive_time} hours from {start_location}. Considering my constraints and the following specifics: {prompt_field}, can you recommend the best possible hike that meets my criteria? Please provide details about the hike, including the trail name, location, expected conditions, and why it's a great match for my request.
    """

    try:
        response = chat_gpt_service.prompt_chat_gpt(prompt)
        return render_template("response.html", response=response["choices"][0]["message"]["content"])

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Failed to process the request"}), 500
