from flask import render_template, flash, redirect, url_for, abort
from flask_login import login_required, current_user
import pendulum
from app import app, db
from app.models import Post, Comment
from app.forms import NewPostForm, NewCommentForm, UpdatePostForm, UpdateCommentForm


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


@app.route("/posts/<int:post_id>/edit", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    post = Post.query.get(post_id)
    if current_user.id != post.author.id:
        abort(401)

    form = UpdatePostForm()

    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post_id))

    form.title.data = post.title
    form.body.data = post.body
    return render_template("posts/update.html", form=form)


@app.route("/posts/<int:post_id>/delete")
@login_required
def delete_post(post_id):
    post = Post.query.get(post_id)
    if current_user.id != post.author.id:
        abort(401)
    if post:
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for("index_post"))
    else:
        abort(404)


@app.route("/comments/<int:comment_id>", methods=["GET", "POST"])
@login_required
def update_comment(comment_id):
    comment = Comment.query.get(comment_id)
    if comment.author.id != current_user.id:
        abort(401)
    form = UpdateCommentForm()
    if form.validate_on_submit():
        comment.body = form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=comment.post.id))

    form.body.data = comment.body
    return render_template("comments/update.html", form=form)


@app.route("/comments/<int:comment_id>/delete")
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get(comment_id)
    if comment.author.id != current_user.id:
        abort(401)
    post_id = comment.post.id
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for("show_post", post_id=post_id))

