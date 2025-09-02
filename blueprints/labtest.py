from flask import Blueprint, render_template

labtest_bp = Blueprint("labtest", __name__, url_prefix="/labtest")

@labtest_bp.route("/")
def labtest():
    return render_template("labtest.html")
