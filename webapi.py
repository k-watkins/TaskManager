import datetime

from flask import Flask, render_template
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
import flask_mysqldb

# from views import views


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///taskMgr.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password123@localhost:3307/task_manager'
db = SQLAlchemy(app)


# app.register_blueprint(views, url_prefix="/")


class TaskModel(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(100), nullable=False)
    task_description = db.Column(db.String(100), nullable=False)
    task_due_date = db.Column(db.Date(), nullable=False)

    def __repr__(self):
        return f"Task(Task Name = {self.task_name}, Task Description = {self.task_description} " \
               f"Task Due date = {self.task_due_date}"

    def __init__(self, id, name, desc, due):
        self.task_id = id
        self.task_name = name
        self.task_description = desc
        self.task_due_date = due


task_put_args = reqparse.RequestParser()
task_post_args = reqparse.RequestParser()

with app.app_context():
    db.create_all()

task_post_args.add_argument("Taskname", type=str, help="Taskname is required", required=True)
task_post_args.add_argument("Description", type=str, help="Description is required", required=True)
task_post_args.add_argument("date", type=str, help="date is required", required=True)

task_put_args.add_argument("Taskname", type=str, help="Taskname is required", required=True)
task_put_args.add_argument("Description", type=str, help="Description is required", required=True)
task_put_args.add_argument("date", type=str, help="date is required", required=True)


@app.route('/')
def users():
    user = db.session.execute(db.select(TaskModel).order_by(TaskModel.task_id)).scalars()
    for i in user:
        return render_template("index.html", data=i)




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
