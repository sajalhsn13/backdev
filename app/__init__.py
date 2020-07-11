from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object("config")
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = "show_login"
login_manager.login_message = "Login to view the page"
login_manager.login_message_category = "info"


from app.models import User
from app.routes import loginRoutes, postRoutes, registerRoutes, profileRoutes
