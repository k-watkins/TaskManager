from datetime import datetime
from forms import RegistrationForm, LoginForm, AddTask
from flask import Flask, render_template, url_for, flash, redirect, request
from flask_restful import Api, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# from views import views


app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = '98da64f0467c51ae07c26964ea2993d8'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///taskMgr.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password123@localhost:3307/task_manager'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


# app.register_blueprint(views, url_prefix="/")
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    tasks = db.relationship('TaskModel', backref='task', lazy=True)

    def __repr__(self):
        return f"User('{self.username}, {self.email}')"


#  each class will be a separate table
class TaskModel(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(100), nullable=False)
    task_description = db.Column(db.String(100), nullable=False)
    task_due_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)

    def __repr__(self):
        return f"Task(Task id = {self.task_id}, Task Name = {self.task_name}, " \
               f"Task Description = {self.task_description} " \
               f"Task Due date = {self.task_due_date}"


task_put_args = reqparse.RequestParser()
task_post_args = reqparse.RequestParser()


task_post_args.add_argument("Taskname", type=str, help="Taskname is required", required=True)
task_post_args.add_argument("Description", type=str, help="Description is required", required=True)
task_post_args.add_argument("date", type=str, help="date is required", required=True)

task_put_args.add_argument("Taskname", type=str, help="Taskname is required", required=True)
task_put_args.add_argument("Description", type=str, help="Description is required", required=True)
task_put_args.add_argument("date", type=str, help="date is required", required=True)


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
    form = LoginForm()
    logged_in = False
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            logged_in = True
            return redirect(url_for('task_data'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template("login.html", title="Login", form=form)


def delete():
    pass


"""
class TaskModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Task(username = {username}, views = {subject}, likes = {description})"


task_post_args = reqparse.RequestParser()
task_post_args.add_argument("username", type=str, help="Username is required", required=True)
task_post_args.add_argument("subject", type=str, help="Subject is required", required=True)
task_post_args.add_argument("description", type=str, help="Description is required", required=True)

task_put_args = reqparse.RequestParser()
task_put_args.add_argument("username", type=str, help="Username is required", required=True)
task_put_args.add_argument("subject", type=str, help="Subject is required", required=True)
task_put_args.add_argument("description", type=str, help="Description is required", required=True)
task_delete_args = reqparse.RequestParser()

resource_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'subject': fields.String,
    'description': fields.String
}

with app.app_context():
    db.create_all()
    
class Task(Resource):
    @marshal_with(resource_fields)
    def get(self):
        # result = TaskModel.query.filter_by(id=task_id).first()
        result = TaskModel.query.all()
        render_template("index.html", data=result)
        if not result:
            abort(404, message="Id does not exist, cannot return results")
        return result, 200

    @marshal_with(resource_fields)
    def post(self, task_id):
        args = task_post_args.parse_args()
        result = TaskModel.query.filter_by(id=task_id).first()
        if result:
            abort(409, message="Id already exists, cannot create record")
        task = TaskModel(id=task_id, username=args['username'],
                         subject=args['subject'],
                         description=args['description'])
        db.session.add(task)
        db.session.commit()
        return task, 201

    @marshal_with(resource_fields)
    def put(self, task_id):
        args = task_put_args.parse_args()
        result = TaskModel.query.filter_by(id=task_id).first()
        if not result:
            task = TaskModel(id=task_id, username=args['username'], subject=args['subject'],
                             description=args['description'])
            db.session.add(task)
            db.session.commit()
            return task, 200
        if args['username']:
            result.username = args['username']
        if args['subject']:
            result.subject = args['subject']
        if args['description']:
            result.description = args['description']

        db.session.commit()
        return result, 200

    @marshal_with(resource_fields)
    def delete(self, task_id):
        args = task_delete_args.parse_args()
        result = TaskModel.query.filter_by(id=task_id).first()
        if not result:
            abort(404, message="Id does not exist, cannot delete record")
        db.session.delete(result)
        db.session.commit()
        return result, 200
@app.route('/')
def index():
    return render_template("index.html", data=TaskModel.query.filter_by())


api.add_resource(Task, "/task/<int:task_id>")
"""
if __name__ == "__main__":
    app.run(debug=True)
