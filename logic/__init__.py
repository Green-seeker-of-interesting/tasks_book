from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

from app import app

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Пожалуйста войдите в систему"

migrate = Migrate(app, db, render_as_batch=True)


from . import models
from . import user_worker
from . import prodject_worker
from . import decorators

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(models.User).get(user_id)