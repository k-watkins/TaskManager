from datetime import datetime
from taskmanager import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# app.register_blueprint(views, url_prefix="/")
class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    tasks = db.relationship('TaskModel', backref='task', lazy=True)

    def get_id(self):
           return (self.user_id)

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
