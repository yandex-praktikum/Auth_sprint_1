from flask import Blueprint, render_template
from flask import request
from flask import flash
from flask import jsonify

from flask_jwt_extended import jwt_required

from http import HTTPStatus

from db.user import get_user, post_user
from db.auth import post_auth_record, get_auth_records
from db.refresh import pull_refresh_token, update_refresh_token
from db.refresh import push_refresh_token, delete_refresh_token

from utils.password import hash_password, verify_password
from utils.jwt_token import get_access_token, get_refresh_token
from utils.jwt_token import get_jwt, get_jwt_identity
from utils.jwt_token import get_jti

from db.redis import push_blocklist


auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    login = request.form.get('login')
    password = request.form.get('password')

    # Проверяем парроль
    user = get_user(login)
    if not user:
        flash('Login does not exist')
        return jsonify('Login does not exist'), HTTPStatus.BAD_REQUEST

    if not verify_password(password, user.hash_password):
        flash('Wrong password')
        return jsonify('Wrong password'), HTTPStatus.UNAUTHORIZED

    # Проверяем есть ли regresh токен с этого устройства
    user_agent = request.user_agent.string
    token_info = pull_refresh_token(user.id, user_agent)

    # Создаем новый токены
    access_token = get_access_token(user)
    refresh_token = get_refresh_token(user)

    # Есть regresh токен - меняем, нет - создаем
    jti = get_jti(refresh_token)

    if token_info:
        update_refresh_token(token_info, jti)
    else:
        push_refresh_token(user.id, user_agent, jti)

    # Создаем запись о входе в акаунт
    auth_dict = {
        'user_id': user.id,
        'user_agent': request.user_agent.string
    }
    post_auth_record(auth_dict)

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

    # Проверка, что юзера не сущетвует
    user = get_user(user_dict['login'])
    if user:
        flash('Login already exists')
        return jsonify('Login already exists'), HTTPStatus.CONFLICT

    # Запись с проверкой уникальности e-mail
    post = post_user(user_dict)
    if not post:
        flash('E-mail already exists')
        return jsonify('E-mail already exists'), HTTPStatus.CONFLICT

    flash('Successful registration')
    return jsonify('Successful registration'), HTTPStatus.CREATED


@auth.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh_post():
    # Вытаскиваем содержимое refresh токена
    get_token = get_jwt()
    user_info = get_jwt_identity()
    user_agent = request.user_agent.string

    # Вытаскиваем из БД токен
    token_info = pull_refresh_token(user_info['id'], user_agent)

    # Если машина не та или токена удален из БД
    if not token_info:
        return jsonify('Wrong token'), HTTPStatus.UNAUTHORIZED

    # Если токен не совпал
    if token_info.refresh_token != get_token:
        return jsonify('Wrong token'), HTTPStatus.UNAUTHORIZED

    # Создаем токены
    access_token = get_access_token(user_info)
    refresh_token = get_refresh_token(user_info)

    # Обновляем данные о refresh токене
    update_refresh_token(token_info, refresh_token)

    return jsonify(access_token=access_token, refresh_token=refresh_token), \
        HTTPStatus.OK


@auth.route('/info', methods=['GET'])
@jwt_required()
def info_get():
    user_info = get_jwt_identity()
    auth_records = get_auth_records(user_info['id'])
    auth_records = [{
        'user_agent': item.user_agent,
        'data_time': item.data_time
    } for item in auth_records]
    return jsonify(auth_records), HTTPStatus.OK


@auth.route('/logout', methods=["DELETE"])
@jwt_required()
def logout():
    # Вытаскиваем данные о пользователе и устройсве
    user_info = get_jwt_identity()
    user_agent = request.user_agent.string

    # Добавляем accsess токен в blocklist
    jti = get_jwt()
    push_blocklist(jti)

    # Удаляем refrech токен
    delete_refresh_token(user_info['id'], user_agent)

    return jsonify("Access and refresh token delete"), HTTPStatus.OK


@auth.route('/newlogin')
def newlogin():
    return render_template('newlogin.html')


@auth.route('/newlogin', methods=['POST'])
def newlogin_post():
    login = request.form.get('login')
    password = request.form.get('password')
    new_login = request.form.get('new_login')

    # Пороверяем, что ползователь есть
    user = get_user(login)
    if not user:
        flash('Login dose not exist')
        return jsonify('Login dose not exist'), HTTPStatus.NOT_FOUND

    # Проверяем пароль
    if not verify_password(password, user.hash_password):
        flash('Wrong password')
        return jsonify('Wrong password'), HTTPStatus.UNAUTHORIZED

    # Если все хорошо, подменяем и постим
    user.login = new_login
    if post_user(user):
        return jsonify('New login set'), HTTPStatus.OK
    else:
        return jsonify('Login already exists'), HTTPStatus.CONFLICT


@auth.route('/newpassword')
def newpasswordn():
    return render_template('newpassword.html')


@auth.route('/newpassword', methods=['POST'])
def newpassword_post():
    login = request.form.get('login')
    password = request.form.get('password')
    new_password = request.form.get('new_password')

    # Пороверяем, что ползователь есть
    user = get_user(login)
    if not user:
        flash('Login dose not exist')
        return jsonify('Login dose not exist'), HTTPStatus.NOT_FOUND

    # Проверяем пароль
    if not verify_password(password, user.hash_password):
        flash('Wrong password')
        return jsonify('Wrong password'), HTTPStatus.UNAUTHORIZED

    # Если все хорошо, подменяем и постим
    user.hash_password = hash_password(new_password)
    if post_user(user):
        return jsonify('New login set'), HTTPStatus.OK
    else:
        return jsonify('Login already exists'), HTTPStatus.CONFLICT
