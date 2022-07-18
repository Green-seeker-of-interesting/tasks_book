from flask import flash
from flask_login import login_user

from logic.models import User
from logic import db



def user_login_worker(email:str, psw:str, is_remember:bool = False) -> bool:
    user_logining = db.session.query(User).filter(User.email == email).first()
    if user_logining:
        if user_logining.chek_pasword(psw):
                login_user(user_logining)
                return True
        else:
            flash("Неверное имя пользователя или пароль")
    else:
        flash("Неверное имя пользователя или пароль")
        return False


def user_registr_worker(name:str, email:str, psw:str, psw_cheak:str) -> bool:
    if psw == psw_cheak:
        nUser = User(
            name=name,
            email=email,
            online = False
        )
        nUser.set_password(psw)
        db.session.add(nUser)
        db.session.commit()
        return True
    else:
        flash("Пароли должны совпадать")
        return False