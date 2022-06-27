
from flask_jwt_extended import JWTManager, create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import decode_token
from flask_jwt_extended import get_jwt as flask_get_jwt
from flask_jwt_extended import get_jwt_identity as flask_get_identity
from db.redis import blocklist_check

jwt = JWTManager()

@jwt.user_identity_loader
def user_identity_lookup(user):
    """То, что записывается в JWT"""
    if type(user) == dict:
        return {
            'id': user['id'],
            'login': user['login'],
            'name': user['name'],
            'role': user['role']
        }
    return {
        'id': user.id,
        'login': user.login,
        'name': user.name,
        'role': user.role
    }


def get_access_token(user):
    access_token = create_access_token(identity=user)
    return access_token

def get_refresh_token(user):
    refresh_token = create_refresh_token(identity=user)
    return refresh_token


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_in_redis = blocklist_check(jti)
    return token_in_redis is not None

def get_jwt():
    return flask_get_jwt()['jti']

def get_jwt_identity():
    return flask_get_identity()

def get_jti(token):
    decod_token = decode_token(token)
    return decod_token['jti']
