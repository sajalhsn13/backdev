from flask import render_template
from flask_login import login_required
from app import app
from app.models import User
from app.forms import UpdateProfileForm


@app.route("/profile/<string:username>")
def show_profile(username):
    user = User.query.filter_by(username=username).first()
    return render_template("users/profile.html.j2", user=user)


@app.route("/profile/edit")
@login_required
def edit_profile():
    form = UpdateProfileForm()
    return render_template("users/update.html.j2", form=form)

