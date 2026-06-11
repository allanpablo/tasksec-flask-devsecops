from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy import or_

from app import db
from app.forms import LoginForm, RegistrationForm, TaskForm
from app.models import Task, User
from app.utils import log_security_event

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")
main_bp = Blueprint("main", __name__)
task_bp = Blueprint("task", __name__, url_prefix="/task")


@main_bp.route("/")
def index():
    return render_template("index.html")


@main_bp.route("/health")
def health():
    return {"status": "healthy"}, 200


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        log_security_event(
            "User registered successfully", user=user.username, level="info"
        )
        flash("Conta criada com sucesso!", "success")
        return redirect(url_for("auth.login"))
    return render_template("register.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            log_security_event(
                "User logged in successfully", user=user.username, level="info"
            )
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for("main.dashboard"))
        log_security_event(
            "Failed login attempt", user=form.username.data, level="warning"
        )
        flash("Usuário ou senha inválidos.", "danger")
    return render_template("login.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    log_security_event("User logged out", user=current_user.username, level="info")
    logout_user()
    flash("Você saiu da sua conta.", "info")
    return redirect(url_for("main.index"))


@main_bp.route("/dashboard")
@login_required
def dashboard():
    search = request.args.get("q", "")
    page = request.args.get("page", 1, type=int)
    query = Task.query.filter_by(user_id=current_user.id)
    if search:
        query = query.filter(
            or_(Task.title.ilike(f"%{search}%"), Task.description.ilike(f"%{search}%"))
        )
    tasks = query.order_by(Task.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    return render_template("dashboard.html", tasks=tasks, search=search)


@task_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(
            title=form.title.data,
            description=form.description.data,
            user_id=current_user.id,
        )
        db.session.add(task)
        db.session.commit()
        log_security_event(
            "Task created", user=current_user.username, level="info"
        )
        flash("Tarefa criada com sucesso!", "success")
        return redirect(url_for("main.dashboard"))
    return render_template("create_task.html", form=form)


@task_bp.route("/<int:task_id>", methods=["GET"])
@login_required
def detail(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    return render_template("task_detail.html", task=task)


@task_bp.route("/<int:task_id>/edit", methods=["GET", "POST"])
@login_required
def edit(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    form = TaskForm(obj=task)
    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.completed = form.completed.data
        db.session.commit()
        log_security_event(
            "Task edited", user=current_user.username, level="info"
        )
        flash("Tarefa atualizada!", "success")
        return redirect(url_for("main.dashboard"))
    return render_template("edit_task.html", form=form, task=task)


@task_bp.route("/<int:task_id>/delete", methods=["POST"])
@login_required
def delete(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    db.session.delete(task)
    db.session.commit()
    log_security_event(
        "Task deleted", user=current_user.username, level="info"
    )
    flash("Tarefa excluída.", "success")
    return redirect(url_for("main.dashboard"))
