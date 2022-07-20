from flask_login import current_user

from logic.models import Prodject, Task
from logic import db


def create_prodject(name:str)->bool:
    nProdject = Prodject(
        name = name,
        author = current_user.id
    )
    db.session.add(nProdject)
    db.session.commit()
    return True


def get_prodject_array()-> dict:
    out = dict()
    for item in current_user.prodject:
        out.update({
            str(item.id) : item.name
        })
    return out


def get_task_array(prodject_id)-> dict:
    pjc = db.session.query(Prodject).filter(Prodject.id == prodject_id).first()
    out = dict()
    if pjc:
        for item in pjc.tasks:
            out.update({
                str(item.id) : [item.title , item.content]
            })
    return out

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


def change_task(task, title, content)->bool:
    
    content = content.replace("\n", "<br>")
    task.content = content
    task.title = title

    db.session.add(task)
    db.session.commit()

    return True


def del_project_worker(prodject_id):
    pjc = db.session.query(Prodject).filter(Prodject.id == prodject_id).first()
    for task in pjc.tasks:
        db.session.delete(task)
    db.session.delete(pjc)
    db.session.commit()


def del_task_worker(task_id):
    task = db.session.query(Task).filter(Task.id == task_id).first()
    db.session.delete(task)
    db.session.commit()