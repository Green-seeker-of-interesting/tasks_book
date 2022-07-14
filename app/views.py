from flask import render_template, flash, request, redirect, url_for
from flask_login import login_required, login_user, logout_user

from app import app, db
from app.models import Task, User, Prodject
from app.forms import tasksForm


MAIN_MENU_LIST = [
    {"name" : "main_page", "url" : "/"},
    #{"name" : "all_data", "url" : "/all_data/"},
    {"name" : "forms", "url" : "/forms/"},
    {"name" : "login", "url" : "/login/"},
]


@app.route("/")
def index():
    data_from_db = db.session.query(Task).all()

    return render_template(
        "index.html",
        title = "Main",
        menu = MAIN_MENU_LIST,
        all_task = data_from_db
        )


@app.route("/forms/", methods=["GET","POST"])
@login_required
def form_for_task():

    form = tasksForm()

    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")

        task_new = Task(
            title = title,
            content = content
            )        

        db.session.add(task_new)
        db.session.commit()
        flash("Всё ОК")
        return redirect(url_for("form_for_task"))
        
    
    return render_template(
        "form.html",
        menu = MAIN_MENU_LIST,
        form = form,
    )


@app.route("/post/<int:task_id>")
def one_task(task_id):
    task_data =  db.session.query(Task).get(int(task_id))
    
    return render_template(
        "one_task.html",
        menu = MAIN_MENU_LIST,
        task=task_data
    )


@app.route("/login/", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        user_logining = db.session.query(User).filter(User.email == request.form['email']).first()
        if user_logining:
            if user_logining.chek_pasword(request.form["psw"]):
                login_user(user_logining)
        else:
            flash("Нет такого мыла")



    return render_template(
        "login.html",
        menu = MAIN_MENU_LIST
    )


@app.route("/register/",  methods=["GET", "POST"])
def register():
    if request.method == "POST":
        n_user = User(
            name = request.form['name'],
            email = request.form['email'],
            online = False
        )
        n_user.set_password(request.form["psw"])

        db.session.add(n_user)
        db.session.commit()
        flash("Всё ок")

    return render_template(
        "register.html",
        menu = MAIN_MENU_LIST
    )


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for('login'))

# @app.errorhandler(401)
# def pageNotFount(error):
#     return redirect(url_for('login'))
    