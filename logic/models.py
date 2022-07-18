from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from logic import db


class User(db.Model, UserMixin):
    __tablename__ = 'User'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    psw = db.Column(db.String(255), nullable=False)
    online = db.Column(db.Boolean(), nullable=False, default=False)# Это поле бесполезно
    
    prodject = db.relationship('Prodject', backref='theAuthor')
    tasks = db.relationship('Task', backref='theAuthor')

    def set_password(self, pas:str):
        self.psw = generate_password_hash(pas)

    def chek_pasword(self, pas:str):
        return check_password_hash(self.psw, pas)

    def __repr__(self):
	    return "id - {id} \n name {name} \n email {email} \n prodject {prj}".format(
            id = self.id,
            name = self.name,
            email = self.email,
            prj = self.prodject
        )


class Prodject(db.Model):
    __tablename__ = 'Prodject'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    author = db.Column(db.Integer(),db.ForeignKey('User.id'))
    tasks = db.relationship('Task', backref='theProdject')


class Task(db.Model):
    __tablename__ = 'Task'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text(), nullable=False)

    author = db.Column(db.Integer(),db.ForeignKey('User.id'))
    prodject = db.Column(db.Integer(),db.ForeignKey('Prodject.id'))


    def get_value_task(self):
        out = {
            "title" : self.title,
            "content" : self.content,
            "authot" : self.author,
        }
        return out

    def __repr__(self):
	    return str(self.get_value_task())
