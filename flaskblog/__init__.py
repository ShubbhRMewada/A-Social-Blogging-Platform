

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = '4cdfaf1e15928bcd06cb8c1efb3e12a9'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'dummy.mail.for.iitmproject@gmail.com'
app.config['MAIL_PASSWORD'] = 'gawzkalottnvdbmk'
mail = Mail(app)


db.create_all()

from flaskblog import routes
