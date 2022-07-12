from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import config


app = Flask(__name__)
app.config.from_object(config.DevelopementConfig)
db = SQLAlchemy(app)




from . import views
from . import models