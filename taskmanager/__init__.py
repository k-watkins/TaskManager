from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = '98da64f0467c51ae07c26964ea2993d8'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///taskMgr.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password123@localhost:3307/task_manager'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from taskmanager import routes
