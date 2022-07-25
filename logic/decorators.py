from flask_login import current_user
from flask_restful import abort

from logic import prodject_worker as pjw


def access_check(func):

    def wrapper(*args, **kwargs):
        prj = pjw.get_prodjecr_by_id(prodject_id=kwargs["prodject_id"])

        if prj.is_author(current_user.id):
            return func(*args, **kwargs)
        else:
            return abort(403)
    wrapper.__name__ = func.__name__ 

    return wrapper
