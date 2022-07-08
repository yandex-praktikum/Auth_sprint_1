# -*- coding: utf-8 -*-
#
# @created: 27.06.2022
# @author: sprint6_team

from http import HTTPStatus
from flask import Blueprint, request, url_for, redirect
from app import app
from db.db import db
from authlib.integrations.flask_client import OAuth
from api.v1.login import login_controller
from db.user import post_user
from config import oauth_settings, logger
from db.db_models import User, generate_random_password, SocialAccount
from utils.passwords import hash_password
from flask_jwt_extended import get_jwt_identity, jwt_required

oauth = OAuth(app)

oauth_blueprint = Blueprint("oauth", __name__, url_prefix="/oauth")
app.register_blueprint(oauth_blueprint)

@oauth_blueprint.route('/google/')
def google():
   
    GOOGLE_CLIENT_ID = oauth_settings.google_client_id
    GOOGLE_CLIENT_SECRET = oauth_settings.google_client_secret
     
    CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
    oauth.register(
        name='google',
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        server_metadata_url=CONF_URL,
        client_kwargs={
            'scope': 'openid email profile'
        }
    )
    # Redirect to google_auth function
    redirect_uri = url_for('google_auth', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)
 

@oauth_blueprint.route('/google/auth/')
def google_auth():
    access_token = oauth.google.authorize_access_token()
    google_user = oauth.google.parse_id_token(access_token)
    logger.info(f"Google User {google_user}")
    google_user["login"] = google_user["email"]
    return process_auth_user(google_user)


def process_auth_user(access_token: str, oauth_user: str):
    email = oauth_user["email"]
    user = User.get_user_by_universal_login(email=email)
    user_agent = request.user_agent.string
    if user:

        social_dict = {
            "user_id": user.id,
            "social_type": "google",
            "social_id": oauth_user["id"],
            "social_name": oauth_user["name"],
            "access_token": access_token,
        }
        social_account = SocialAccount(**user)
        db.session.add(social_account)
        db.session.commit()
        return login_controller(user, user_agent)

    password = generate_random_password()
    user_dict = {
        "login": email,
        "email": email,
        "hash_password": hash_password(password),
    }
    user = post_user(user_dict)

    social_dict = {
        "user_id": user.id,
        "social_type": "google",
        "social_id": oauth_user["id"],
        "social_name": oauth_user["name"],
        "access_token": access_token,
    }
    social_account = SocialAccount(**user)
    db.session.add(social_account)
    db.session.commit()
    
    if not user:
        return {}, HTTPStatus.CONFLICT
    return login_controller(user, user_agent)


@oauth_blueprint.route("/google/logout")
@jwt_required()
def google_logout():
    user_info = get_jwt_identity()
    user = User.get_user_by_universal_login(email=user_info["email"])
    if not user:
        return {}, HTTPStatus.UNAUTHORIZED
    access_token = user.access_token
    resp = google.post(
        "https://accounts.google.com/o/oauth2/revoke",
        params={"token": access_token},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    user.reset_oauth_field("google")
    return redirect("/logout")
