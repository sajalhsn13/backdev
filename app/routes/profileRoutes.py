from PIL import Image
import secrets
import os
from flask import render_template, redirect, url_for
from flask_login import login_required, current_user
from app import app, bcrypt, db
from app.models import User
from app.forms import UpdateProfileForm


@app.route("/profile/<string:username>")
def show_profile(username):
    user = User.query.filter_by(username=username).first()
    image_url = (
        url_for("static", filename=f"propics/{user.image_url}")
        if user.image_url
        else "https://placekitten.com/200/200"
    )
    return render_template("users/profile.html", user=user, image_url=image_url)


@app.route("/profile/edit")
@login_required
def edit_profile():
    form = UpdateProfileForm()
    form.username.data = current_user.username
    form.email.data = current_user.email
    return render_template("users/update.html", form=form)


@app.route("/profile/edit", methods=["POST"])
@login_required
def update_profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        if form.new_password.data:
            current_user.password = bcrypt.generate_password_hash(
                form.new_password.data
            ).decode("utf-8")
        if form.upload.data:
            current_user.image_url = save_image(form.upload.data)
        db.session.commit()
        return redirect(url_for("show_profile", username=current_user.username))
    return render_template("users/update.html", form=form)


def save_image(from_image):
    random_hex = secrets.token_hex(32)
    _, extension = os.path.splitext(from_image.filename)
    if current_user.image_url:
        current_image_path = os.path.join(
            app.root_path, "static", "propics", current_user.image_url
        )
        os.remove(current_image_path)
    image_file_name = random_hex + extension
    image_path = os.path.join(app.root_path, "static", "propics", image_file_name)
    image_folder_path = os.path.join(app.root_path, "static", "propics")
    if not os.path.exists(image_folder_path):
        os.makedirs(image_folder_path)
    output_size = (200, 200)
    image = Image.open(from_image)
    image.thumbnail(output_size)
    image.save(image_path)
    return image_file_name

