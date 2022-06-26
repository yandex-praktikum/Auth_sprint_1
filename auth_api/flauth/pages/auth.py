from flask import Blueprint, render_template
from flask import request
from flask import flash
from flask import jsonify

from http import HTTPStatus

from db.user import get_user, post_user
from db.auth import post_auth_record

from utils.password import hash_password, verify_password
from utils.jwt_tocken import get_access_token, get_refresh_token


auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    login = request.form.get('login')
    password = request.form.get('password')

    user = get_user(login)
    if not user:
        flash('Login does not exist')
        return jsonify('Login does not exist'), HTTPStatus.BAD_REQUEST

    if not verify_password(password, user.hash_password):
        flash('Wrong password')
        return jsonify('Wrong password'), HTTPStatus.UNAUTHORIZED

    auth_dict = {
        'user_id': user.id,
        'user_agent': request.user_agent.string
    }

    post = post_auth_record(auth_dict)
    if not post:
        flash('Recording auth problem')
        return jsonify('Recording auth problem'), HTTPStatus.BAD_REQUEST

    access_token = get_access_token(user)
    refresh_token = get_refresh_token(user)
    return jsonify(access_token=access_token, refresh_token=refresh_token), \
        HTTPStatus.OK


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    user_dict = {}
    user_dict['login'] = request.form.get('login')
    user_dict['email'] = request.form.get('email')
    user_dict['name'] = request.form.get('name')
    password = request.form.get('password')
    user_dict['hash_password'] = hash_password(password)

    user = get_user(user_dict['login'])
    if user:
        flash('Login already exists')
        return jsonify('Login already exists'), HTTPStatus.CONFLICT

    post = post_user(user_dict)
    if not post:
        flash('E-mail already exists')
        return jsonify('E-mail already exists'), HTTPStatus.CONFLICT

    flash('Successful registration')
    return jsonify('Successful registration'), HTTPStatus.CREATED


@auth.route('/logout')
def logout():
    return 'logout'


"""
@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if user actually exists
    # take the user supplied password, hash it,
    # and compare it to the hashed password in database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        # if user doesn't exist or password is wrong, reload the page
        return redirect(url_for('auth.login'))

    # if the above check passes, then we know the user
    # has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))


@auth.route('/signup', methods=['POST'])
def signup_post():

    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    # if this returns a user, then the email already exists in database
    user = User.query.filter_by(email=email).first()

    # if a user is found, we want to redirect
    # back to signup page so user can try again
    if user:
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # create new user with the form data. Hash the password
    # so plaintext version isn't saved.
    new_user = User(
        email=email,
        name=name,
        password=generate_password_hash(password, method='sha256')
    )

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))



@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
"""