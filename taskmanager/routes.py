from taskmanager.models import User, TaskModel
from taskmanager.forms import RegistrationForm, LoginForm, AddTask
from flask import render_template, url_for, flash, redirect, request
from taskmanager import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
def task_data():
    task_get_data = TaskModel.query.all()
    return render_template("index.html", data=task_get_data)


@app.route('/addtask', methods=['GET', 'POST'])
def add_task():
    add = AddTask()
    if request.method == "POST":
        task = TaskModel(
            task_name=request.form['name'],
            task_description=request.form['description'],
            user_id=1
        )
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('task_data'))
    return render_template("addtask.html", form=add)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('task_data'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.pass_conf.data).decode('utf-8')
        if request.method == 'POST':
            user = User(
                username=request.form['username'],
                email=request.form['email'],
                password=hash_password
            )
            db.session.add(user)
            db.session.commit()
            flash(f'Account created for {form.username.data}', 'success')
        return redirect(url_for('login'))
    return render_template("signup.html", title="Sign-up", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('task_data'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Login Successful', 'success')
            return redirect(url_for('task_data'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template("login.html", title="Login", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('task_data'))


def delete():
    pass
