from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

import config


app = Flask(__name__)
app.config.from_object(config.DevelopementConfig)
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

migrate = Migrate(app, db, render_as_batch=True)

from . import views
from . import models
from . import forms


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(models.User).get(user_id)