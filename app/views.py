from turtle import title
from flask import render_template, request, redirect, url_for

from app import app, db
from app.models import task
from app.forms import tasksForm


MAIN_MENU_LIST = [
    {"name" : "main_page", "url" : "/"},
    #{"name" : "all_data", "url" : "/all_data/"},
    {"name" : "forms", "url" : "/forms/"},
    # {"name" : "main_page", "url" : "index_view"},
]


@app.route("/")
def index():
    data_from_db = db.session.query(task).all()

    return render_template(
        "index.html",
        title = "Main",
        menu = MAIN_MENU_LIST,
        all_task = data_from_db[::-1]
        )



@app.route("/forms/", methods=["GET","POST"])
def form_for_task():

    form = tasksForm()

    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")

        task_new = task(
            title = title,
            content = content
            )        

        db.session.add(task_new)
        db.session.commit()


    return render_template(
        "form.html",
        menu = MAIN_MENU_LIST,
        form = form,
    )


@app.route("/post/<int:task_id>")
def one_task(task_id):
    task_data =  db.session.query(task).get(int(task_id))
    
    return render_template(
        "one_task.html",
        menu = MAIN_MENU_LIST,
        task=task_data
    )