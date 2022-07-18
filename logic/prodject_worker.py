from flask_login import current_user

from logic.models import Prodject
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