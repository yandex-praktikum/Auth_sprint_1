# -*- coding: utf-8 -*-
#
# @created: 27.06.2022
# @author: sprint6_team

from http import HTTPStatus

from requests import request
from db import redis_db
from random import seed
from random import randint
from time import time
from pages.auth import auth_blueprint
from utils.passwords import hash_password

seed(1100)

def generate_random_math():
    a = randint(1,100)
    b = randint(1,100)
    c = randint(1,100)
    d = randint(1,100)
    return a, b, c, d


@auth_blueprint.route("/captcha", methods=["GET"])
def captcha_get():
    captcha = generate_random_math()
    answer = sum(captcha)
    hash = hash_password(str(answer))
    redis_db.set(hash, (answer, time()), ex=60)
    return {"data": captcha, "id": hash}, HTTPStatus.OK


@auth_blueprint.route("/captcha/<hash>", methods=["POST"])
def captcha_check(hash):
    answer = request.form.get("answer")
    if not answer.isnumeric():
        return {}, HTTPStatus.BAD_REQUEST
    result = redis_db.get(hash)
    if not hash:
        return {}, HTTPStatus.BAD_REQUEST
    expected_answer, send_time = result 
    if time.time() - send_time < 30:
        return {}, HTTPStatus.BAD_REQUEST
    if answer != expected_answer:
        return
    return {}, HTTPStatus.OK