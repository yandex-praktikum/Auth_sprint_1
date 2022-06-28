# -*- coding: utf-8 -*-
#
# @created: 27.06.2022
# @author: sprint6_team

from flask import Blueprint, render_template

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/')
def index():
    return render_template('index.html')

@main_blueprint.route('/login')
def login():
    return render_template('login.html')

@main_blueprint.route('/signup')
def signup():
    return render_template('signup.html')

@main_blueprint.route('/newlogin')
def newlogin():
    return render_template('newlogin.html')

@main_blueprint.route('/newpassword')
def newpasswordn():
    return render_template('newpassword.html')



