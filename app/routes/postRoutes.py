from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user
import pendulum
from app import app, db
from app.models import Post, Comment
from app.forms import NewPostForm, NewCommentForm


@app.route("/")
def index_post():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template("home.html", posts=posts, pendulum=pendulum)


@app.route("/posts/<int:post_id>", methods=["GET", "POST"])
def show_post(post_id):
    form = NewCommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data, user_id=current_user.id, post_id=post_id)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for("show_post", post_id=post_id))
    myPost = Post.query.get(int(post_id))
    return render_template("posts/show.html", post=myPost, form=form, pendulum=pendulum)


@app.route("/posts/create", methods=["GET", "POST"])
@login_required
def create_post():
    form = NewPostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash("New post!!!", "success")
        return redirect(url_for("show_post", post_id=post.id))
    return render_template("/posts/create.html", form=form)
