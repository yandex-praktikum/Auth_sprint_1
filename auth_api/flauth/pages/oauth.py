# -*- coding: utf-8 -*-
#
# @created: 27.06.2022
# @author: sprint6_team

from http import HTTPStatus
from flask import Blueprint, request, url_for, redirect
from app import app
from authlib.integrations.flask_client import OAuth
from auth_api.flauth.api.v1.login import login_controller
from db.user import post_user
from config import oauth_settings, logger
from db.db_models import User, generate_random_password
from utils.passwords import hash_password
from flask_jwt_extended import jwt_required

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
    return process_auth_user(google_user)


def process_auth_user(access_token: str, oauth_user: str):
    email = oauth_user["email"]
    user = User.get_user_by_universal_login(email=email)
    logger.info(f"Google User {user}")
    user_agent = request.user_agent.string
    if user:
        user.google_id = email
        user.google_token = access_token
        user.save()
        return login_controller(user, user_agent)
    password = generate_random_password()
    user_dict = {
        "login": email,
        "email": email,
        "google_token": access_token,
        "hash_password": hash_password(password),
    }
    user = post_user(user_dict)
    if not user:
        return {}, HTTPStatus.CONFLICT
    return login_controller(user, user_agent)


@oauth_blueprint.route("/google/logout")
@jwt_required()
def google_logout():
    token = blueprint.token["access_token"]
    resp = google.post(
        "https://accounts.google.com/o/oauth2/revoke",
        params={"token": token},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert resp.ok, resp.text
    logout_user()        # Delete Flask-Login's session cookie
    del blueprint.token  # Delete OAuth token from storage
    return redirect(somewhere)


@oauth_blueprint.route('/twitter/')
def twitter():
   
    # Twitter Oauth Config
    TWITTER_CLIENT_ID = os.environ.get('TWITTER_CLIENT_ID')
    TWITTER_CLIENT_SECRET = os.environ.get('TWITTER_CLIENT_SECRET')
    oauth.register(
        name='twitter',
        client_id=TWITTER_CLIENT_ID,
        client_secret=TWITTER_CLIENT_SECRET,
        request_token_url='https://api.twitter.com/oauth/request_token',
        request_token_params=None,
        access_token_url='https://api.twitter.com/oauth/access_token',
        access_token_params=None,
        authorize_url='https://api.twitter.com/oauth/authenticate',
        authorize_params=None,
        api_base_url='https://api.twitter.com/1.1/',
        client_kwargs=None,
    )
    redirect_uri = url_for('twitter_auth', _external=True)
    return oauth.twitter.authorize_redirect(redirect_uri)
 
@oauth_blueprint.route('/twitter/auth/')
def twitter_auth():
    token = oauth.twitter.authorize_access_token()
    resp = oauth.twitter.get('account/verify_credentials.json')
    profile = resp.json()
    print(" Twitter User", profile)
    return redirect('/')

@oauth_blueprint.route('/facebook/')
def facebook():
   
    # Facebook Oauth Config
    FACEBOOK_CLIENT_ID = os.environ.get('FACEBOOK_CLIENT_ID')
    FACEBOOK_CLIENT_SECRET = os.environ.get('FACEBOOK_CLIENT_SECRET')
    oauth.register(
        name='facebook',
        client_id=FACEBOOK_CLIENT_ID,
        client_secret=FACEBOOK_CLIENT_SECRET,
        access_token_url='https://graph.facebook.com/oauth/access_token',
        access_token_params=None,
        authorize_url='https://www.facebook.com/dialog/oauth',
        authorize_params=None,
        api_base_url='https://graph.facebook.com/',
        client_kwargs={'scope': 'email'},
    )
    redirect_uri = url_for('facebook_auth', _external=True)
    return oauth.facebook.authorize_redirect(redirect_uri)
 
@oauth_blueprint.route('/facebook/auth/')
def facebook_auth():
    token = oauth.facebook.authorize_access_token()
    resp = oauth.facebook.get(
        'https://graph.facebook.com/me?fields=id,name,email,picture{url}')
    profile = resp.json()
    print("Facebook User ", profile)
    return redirect('/')