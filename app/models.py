from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from app import db


class task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    dead_line = db.Column(db.Date(), nullable=False)
    is_сompleted = db.Column(db.Boolean(), default=False)

    def __repr__(self):
	    return "<{}:{}>".format(self.id,  self.title[:10])