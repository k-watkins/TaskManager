from flask import Blueprint, render_template

import webapi

views = Blueprint(__name__, "views")


# Dashboard/Index
@views.route('/')
def index():
    return render_template("index.html", webapi.Task.get(0))


# TODO
@views.route('/login')
def login():
    return render_template("login.html")

