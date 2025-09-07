from flask import Blueprint, render_template

pharmacy_bp = Blueprint("pharmacy", __name__, url_prefix="/pharmacy")

@pharmacy_bp.route("/")
def pharmacy():
    return render_template("pharmacy.html")
