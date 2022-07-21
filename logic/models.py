from datetime import datetime
from turtle import color

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from logic import db


class User(db.Model, UserMixin):
    __tablename__ = 'User'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    psw = db.Column(db.String(255), nullable=False)
   
    ### Схема 2.0 
    num_task = db.Column(db.Integer(), default=0)
    date_registration = db.Column(db.DateTime(), default=datetime.utcnow)
    last_online = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    about_self = db.Column(db.Text())
    super_user = db.Column(db.Boolean, default=False)

    
    prodject = db.relationship('UserToPridject', backref='theAuthor') 
    tasks = db.relationship('Task', backref='theAuthor')
    create_prodject = db.relationship('Prodject', backref='theAuthor')

    def set_password(self, pas:str):
        self.psw = generate_password_hash(pas)

    def chek_pasword(self, pas:str):
        return check_password_hash(self.psw, pas)

    def chek_is_author(self, prodject_id:int):
        #Можно переписать на насколько ретёрнов, будет в теории быстрее
        out = False
        for item in self.prodject:
            if item.prodject == prodject_id:
                out = True
              
        
        for item in self.create_prodject:
            if item.id == prodject_id:
                out = True
        return out

    def __repr__(self):
	    return "id - {id} \n name {name} \n email {email}".format(
            id = self.id,
            name = self.name,
            email = self.email,
        )


class UserToPridject(db.Model):
    __tablename__ = "UserToPridject"
    id = db.Column(db.Integer(), primary_key=True)
    author = db.Column(db.Integer(),db.ForeignKey('User.id'))
    prodject = db.Column(db.Integer(),db.ForeignKey('Prodject.id'))



class Prodject(db.Model):
    __tablename__ = 'Prodject'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    is_open = db.Column(db.Boolean, default=False)
    category = db.Column(db.Integer(),db.ForeignKey('Category.id'))
    creator = db.Column(db.Integer(),db.ForeignKey('User.id'))

    author = db.relationship('UserToPridject', backref='theProdject') 
    tasks = db.relationship('Task', backref='theProdject')


class Category(db.Model):
    __tablename__ = 'Category'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), nullable=False)


class Priority(db.Model):
    __tablename__ = 'Priority'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    color = db.Column(db.String(10), nullable=False, default="#000000")

    tasks = db.relationship('Task', backref='ThePriority') 



class Task(db.Model):
    __tablename__ = 'Task'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text(), nullable=False)

    author = db.Column(db.Integer(),db.ForeignKey('User.id'))
    prodject = db.Column(db.Integer(),db.ForeignKey('Prodject.id'))

    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    is_finished = db.Column(db.Boolean, default=False)
    deadline = db.Column(db.DateTime())

    priority = db.Column(db.Integer(),db.ForeignKey('Priority.id'))

    def get_value_task(self):
        out = {
            "title" : self.title,
            "content" : self.content,
            "authot" : db.session.query(User).filter(User.id == self.author).first().name,
            "created_on" : self.created_on, 
            "updated_on" : self.updated_on,
            "is_finished" : self.is_finished,
            "deadline" : self.deadline,
            "priority" : self.priority,
        }
        return out

    def __repr__(self):
	    return str(self.get_value_task())
