
from flask_jwt_extended import JWTManager, create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import decode_token
from flask_jwt_extended import get_jwt as flask_get_jwt
from flask_jwt_extended import get_jwt_identity as flask_get_identity
from db import redis_db

jwt = JWTManager()


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_in_redis = blocklist_check(jti)
    return token_in_redis is not None

def get_jwt():
    return flask_get_jwt()['jti']

def get_jti(token):
    decod_token = decode_token(token)
    return decod_token['jti']
