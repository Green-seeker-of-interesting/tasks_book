from flask_login import current_user

from logic.models import Prodject, Task, Category, Priority, UserToPridject
from logic import db


def create_prodject(name:str, is_open:bool, category_id:int)->bool:

    nProdject = Prodject(
        name = name,
        is_open = is_open,
        category = category_id,
        creator = current_user.id,
    )
    db.session.add(nProdject)
    db.session.commit()

    link = UserToPridject(
        author = current_user.id,
        prodject = nProdject.id
    )

    db.session.add(link)
    db.session.commit()

    return True


def get_prodject_array()-> dict:
    out_open = dict()
    out_close = dict()
    for item in current_user.prodject:
        prj = db.session.query(Prodject).filter(Prodject.id == item.prodject).first()
        
        if prj.is_open:
            out_close.update({
                str(prj.id) : prj.name
            })  
        else:
            out_open.update({
                str(prj.id) : prj.name
            })  

    return out_open, out_close


def get_task_array(prodject_id)-> dict:
    pjc = db.session.query(Prodject).filter(Prodject.id == prodject_id).first()
    out = dict()
    if pjc:
        for item in pjc.tasks:
            out.update({
                str(item.id) : item.get_value_task()
            })
    return out

def get_prodject_status(prodject_id)-> dict:
    pjc = db.session.query(Prodject).filter(Prodject.id == prodject_id).first()
    return pjc.is_open


def get_task_by_id(task_id):
    return db.session.query(Task).filter(Task.id == task_id).first()


def create_task_to_prodject(prodject_id, title, content)->bool:
    
    content = content.replace("\n", "<br>")
    
    nTask = Task(
        title = title,
        content = content,
        author = current_user.id,
        prodject = prodject_id
    )
    
    db.session.add(nTask)
    db.session.commit()

    return True


def change_task(task, title, content, priority, deadline)->bool:
    
    content = content.replace("\n", "<br>")
    task.content = content
    task.title = title

    task.priority = priority
    task.deadline = deadline

    db.session.add(task)
    db.session.commit()

    return True


def del_project_worker(prodject_id):
    pjc = db.session.query(Prodject).filter(Prodject.id == prodject_id).first()
    for task in pjc.tasks:
        db.session.delete(task)

    user_to_prodject_array = db.session.query(UserToPridject).filter(UserToPridject.prodject == prodject_id).all()
    for task in user_to_prodject_array:
        db.session.delete(task)   


    db.session.delete(pjc)
    db.session.commit()


def del_task_worker(task_id):
    task = db.session.query(Task).filter(Task.id == task_id).first()
    db.session.delete(task)
    db.session.commit()


def get_сategori_list_worker_tuple() ->list:
    all_categorii = db.session.query(Category).all()
    return [(item.id , item.name) for item in all_categorii] 


def get_priority_list_worker_tuple() ->list:
    all_priority = db.session.query(Priority).all()
    return [(item.id , item.name) for item in all_priority] 


def add_author_to_prodject(prodject_id, user_id):
    nUtP = UserToPridject(
        author = user_id,
        prodject = prodject_id,
    )

    db.session.add(nUtP)
    db.session.commit()

def del_author_to_prodject(prodject_id, user_id):
    value = db.session.query(UserToPridject).filter(UserToPridject.prodject == prodject_id).all()
    value = value.filter(UserToPridject.author == user_id).first()

    db.session.delete(value)
    db.session.commit()