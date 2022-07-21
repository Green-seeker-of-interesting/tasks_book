from flask import render_template, flash, request, redirect, url_for
from flask_login import login_required, logout_user, current_user

from app import app
from app.forms import LoginForm, RegistrForm, CreateProjectFrom, CreateTaskForm
from logic import user_worker as usw
from logic import prodject_worker as pjw



@app.route("/")
@login_required
def index():
    open_prj, close_prj = pjw.get_prodject_array()
    return render_template(
        "index.html",
        title = "Main",
        prodjects = open_prj,
        close_prj = close_prj,
        )


@app.route("/login/", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = LoginForm()
    if request.method == "POST" and form.is_submitted():
        if usw.user_login_worker(email=form.email.data, psw=form.psw.data):
            return redirect(url_for("index"))


    return render_template(
            "login.html",
            form = form,
            )


@app.route("/register/",  methods=["GET", "POST"])
def register():
    form = RegistrForm()

    if request.method == "POST":
        if form.is_submitted():
            out_flag =  usw.user_registr_worker(
                name=form.name.data,
                email=form.email.data,
                psw=form.psw.data,
                psw_cheak=form.psw_chek.data
            )
            if out_flag:
                flash("Всё окей")
                return redirect(url_for("login"))
        else:
            flash("Ой что то не то")

    return render_template(
        "register.html",
        form = form,
    )


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    flash("Войдите в систему снова")
    return redirect(url_for('login'))



@app.route('/new_prodject/', methods=["GET", "POST"])
@login_required
def new_prodject():
    form = CreateProjectFrom()

    if request.method == "POST":
        out_flag = pjw.create_prodject(
            name = form.name.data,
            is_open = form.is_open.data,
            category_id=form.category.data,
            )

        if out_flag:
            return redirect(url_for("index"))

    open_prj, close_prj = pjw.get_prodject_array()

    return render_template(
        "new_prodject.html",
        form=form,
        prodjects = open_prj,
        close_prj = close_prj,
    )



@app.route('/prodject/<int:prodject_id>/', methods=["GET"])
@login_required
def prodject(prodject_id):
    open_prj, close_prj = pjw.get_prodject_array()
    return render_template(
        "prodject.html",
        prodjects = open_prj,
        close_prj = close_prj,
        tasks = pjw.get_task_array(prodject_id=prodject_id),
        flag_prodject = True,
        flag_open_prodject = pjw.get_prodject_status(prodject_id),
    )


@app.route('/prodject/<int:prodject_id>/new_task', methods=["GET", "POST"])
@login_required
def new_task(prodject_id):
    form = CreateTaskForm()

    if request.method == "POST":
        pjw.create_task_to_prodject(
            prodject_id=prodject_id,
            title=form.title.data,
            content=form.content.data
            )
        return redirect(f"/prodject/{prodject_id}/")


    open_prj, close_prj = pjw.get_prodject_array()
    return render_template(
        "new_task.html",
        prodjects = open_prj,
        close_prj = close_prj,
        flag_prodject = False,
        form=form,
    )


@app.route('/prodject/<int:prodject_id>/del_project', methods=["GET", "POST"])
@login_required
def del_project(prodject_id):

    if request.method == "POST":
        pjw.del_project_worker(prodject_id=prodject_id)
        return redirect("/")

    open_prj, close_prj = pjw.get_prodject_array()
    return render_template(
        "delete_project.html",
        prodjects = open_prj,
        close_prj = close_prj,
        flag_prodject = False,
    )


@app.route('/prodject/<int:prodject_id>/change_del/<int:task_id>', methods=["POST"])
@login_required
def del_task(prodject_id, task_id):
    pjw.del_task_worker(task_id=task_id)
    return redirect("..")



@app.route('/prodject/<int:prodject_id>/change/<int:task_id>', methods=["GET" ,"POST"])
@login_required
def change_task(prodject_id, task_id):
    task = pjw.get_task_by_id(task_id=task_id)
    form = CreateTaskForm(
        title = task.title,
        content = task.content.replace("<br>","\n"),
        priority = task.priority,
        deadline = task.deadline
    )

    if request.method == "POST":
        pjw.change_task(
            task = task,
            title = form.title.data,
            content = form.content.data,
            priority = form.priority.data,
            deadline = form.deadline.data
            )
        return redirect("..")

    open_prj, close_prj = pjw.get_prodject_array()
    return render_template(
        "new_task.html",
        prodjects = open_prj,
        close_prj = close_prj,
        flag_prodject = True,
        form=form,
    )


@app.route('/prodject/<int:prodject_id>/author_meneger', methods=["GET" ,"POST"])
@login_required
def author_meneger(prodject_id):
    users = usw.get_all_user()
    open_prj, close_prj = pjw.get_prodject_array()
    return render_template(
        "author_meneger.html",
        prodjects = open_prj,
        close_prj = close_prj,
        flag_prodject = True,
        users = users,
        prodject_id = prodject_id,
    )


@app.route('/prodject/<int:prodject_id>/add/<int:user_id>', methods=["POST"])
@login_required
def add_author(prodject_id, user_id):
    pjw.add_author_to_prodject(
        prodject_id=prodject_id, 
        user_id=user_id
        )
    return redirect("..")


@app.route('/prodject/<int:prodject_id>/del/<int:user_id>', methods=["POST"])
@login_required
def del_author(prodject_id, user_id):
    pjw.del_author_to_prodject(
        prodject_id=prodject_id, 
        user_id=user_id
        )
    return redirect("..")