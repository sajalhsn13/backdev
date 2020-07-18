from app import app, db, bcrypt
from flask import render_template, redirect, flash, url_for
from app.forms import RegisterForm
from app.models import User
from flask_login import current_user, login_user


@app.route("/register")
def show_register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegisterForm()
    return render_template("register.html", form=form, register=True)


@app.route("/register", methods=["POST"])
def store_register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=bcrypt.generate_password_hash(form.password.data).decode("utf-8"),
        )
        db.session.add(user)
        db.session.commit()
        user = User.query.filter_by(username=user.username).first()
        login_user(user)
        flash("You account has been created!", "success")
        return redirect(url_for("index_post"))
    return render_template("register.html", form=form)
