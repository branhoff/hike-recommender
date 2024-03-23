from flask import Blueprint, request, jsonify, render_template, Response
from typing import Optional, Tuple

form_bp = Blueprint("form_bp", __name__)


@form_bp.route("/")
def home() -> Response:
    return render_template("form.html")