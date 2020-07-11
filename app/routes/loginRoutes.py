from app import app, bcrypt
from flask import render_template, redirect, flash, url_for, request
from app.forms import LoginForm
from app.models import User
from flask_login import login_user, logout_user, current_user


@app.route("/login")
def show_login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    return render_template("login.html.j2", form=form, login=True)


@app.route("/login", methods=["POST"])
def store_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            nextPage = request.args.get("next", url_for("index_post"))
            flash("Welcome back!", "success")
            return redirect(nextPage)
        else:
            flash("Login unsuccessful! Check your credentials.", "danger")
    return render_template("login.html.j2", form=form, login=True)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index_post"))

