from flask import render_template, flash, request, redirect, url_for
from flask_login import login_required, logout_user, current_user

from app import app
from app.forms import LoginForm, RegistrForm, CreateProjectFrom
from logic import db 
from logic.user_worker import user_login_worker, user_registr_worker
from logic.prodject_worker import create_prodject, get_prodject_array, get_task_array


@app.route("/")
@login_required
def index():
    return render_template(
        "index.html",
        title = "Main",
        prodjects = get_prodject_array(),
        )


@app.route("/login/", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = LoginForm()
    if request.method == "POST" and form.is_submitted():
        if user_login_worker(email=form.email.data, psw=form.psw.data):
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
            out_flag =  user_registr_worker(
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
        if create_prodject(form.name.data):
            return redirect(url_for("index"))

    return render_template(
        "new_prodject.html",
        form=form,
        prodjects = get_prodject_array(),
    )



@app.route('/prodject/<int:prodject_id>/', methods=["GET"])
@login_required
def prodject(prodject_id):
    return render_template(
        "prodject.html",
        prodjects = get_prodject_array(),
        tasks = get_task_array(prodject_id=prodject_id),
    )