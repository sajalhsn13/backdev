from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
    HiddenField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app import bcrypt
from app.models import User, Post


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember me")
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    password_confirm = PasswordField(
        "Confirm password",
        validators=[
            DataRequired(),
            EqualTo("password", message="This field should match the password"),
        ],
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("This username is taken!")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("This email is taken!")


class UpdateProfileForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    new_password = PasswordField("New Password")
    new_password_confirm = PasswordField(
        "Confirm New Password", validators=[EqualTo("new_password")]
    )
    current_password = PasswordField("Current password", validators=[DataRequired()])
    upload = FileField(
        "Profile image",
        validators=[FileAllowed(["jpg", "png"], ".jpg and .png image only!")],
    )
    submit = SubmitField("Update")

    def validate_username(self, username):
        if username.data == current_user.username:
            return
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("This username is taken!")

    def validate_email(self, email):
        if email.data == current_user.email:
            return
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("This email is taken!")

    def validate_current_password(self, current_password):
        if not bcrypt.check_password_hash(current_user.password, current_password.data):
            raise ValidationError("Password is not correct!!!")


class NewPostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    body = TextAreaField("Body", validators=[DataRequired()])
    post = SubmitField("Post")

    def validate_title(self, title):
        post = Post.query.filter_by(title=title.data).first()
        if post:
            raise ValidationError("Title has been taken")


class UpdatePostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    body = TextAreaField("Body", validators=[DataRequired()])
    update = SubmitField("Update")

    def validate_title(self, title):
        if self.title == title:
            return
        post = Post.query.filter_by(title=title.data).first()
        if post:
            raise ValidationError("Title has been taken")


class NewCommentForm(FlaskForm):
    body = TextAreaField("Post a comment", validators=[DataRequired()])
    submit = SubmitField("Post")


class UpdateCommentForm(FlaskForm):
    body = TextAreaField("Update comment", validators=[DataRequired()])
    submit = SubmitField("Update")
