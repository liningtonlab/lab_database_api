import os
import datetime

import jwt
from functools import wraps
from flask import Blueprint, current_app, jsonify, request, abort

from api.models import User, UserToken, session_scope

# This seems to be compatible with gunicorn + running test
# May need revision
try:
    PRIVATE_KEY = open('jwt.key').read()
    PUBLIC_KEY = open('jwt.key.pub').read()
    ALGORITHM = "RS256"
# Assume testing or not interested in RS keys
except FileNotFoundError as e:
    PRIVATE_KEY = os.getenv("SECRET_KEY", "TOPSECRET")
    PUBLIC_KEY = PRIVATE_KEY
    ALGORITHM = "HS256"

def token_is_valid(token):
    try:
        _ = jwt.decode(token, key=PUBLIC_KEY, algorithm=ALGORITHM)
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidSignatureError:
        return False
    return True


def clean_tokens(user, sess):
    # Remove expired tokens
    for token in user.tokens:
        if not token_is_valid(token.token):
            sess.delete(token)


def get_identify(request):
    # Query Arg based auth
    token = request.args.get('token')
    if token and token_is_valid(token):
        with session_scope() as sess:
            user = sess.query(User).join(UserToken).filter_by(token=token).first()
            if user:
                return user
    # Header based auth
    token = request.headers.get('Authorization')
    if token:
        token = token.replace('JWT', '', 1).strip()
        if token_is_valid(token):
            with session_scope() as sess:
                user = sess.query(User).join(UserToken).filter_by(token=token).first()
                if user:
                    return user
    return None


def check_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = get_identify(request)
        # Override authentication for testing
        if current_app.config.get('ENV') in ['development', 'testing']:
            user = True
        if not user:
            return {"error": "User not authenticated"}, 401
        else:
            return func(*args, **kwargs)
    return wrapper


auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/api/v1/login', methods=['GET', 'POST'])
def login():
    """Handle login requests
    """
    if request.method == 'POST':
        json = request.json
        uname = json.get('login')
        pwd = json.get('password')
        if not json or not uname or not pwd:
            abort(401)
        with session_scope() as sess:
            user = sess.query(User).filter_by(login=uname).first()
            if not user or not user.verify_password(pwd):
                abort(401, 'User not found')
            jw_token = jwt.encode(
                {'login': uname, 'level': user.level, 
                'iat': datetime.datetime.utcnow(),
                'exp': datetime.datetime.utcnow()+datetime.timedelta(30)},
                key=PRIVATE_KEY,
                algorithm=ALGORITHM
                ).decode()
            token = UserToken(token=jw_token)
            user.tokens.append(token)
            clean_tokens(user, sess)
            data = {"token": jw_token, "level": user.level, "username": user.login}
        return jsonify({"success": True, "user": data})
    
    # Token validation with GET
    token = request.args.get('token')
    if not token:
        token = request.headers.get('Authorization')
        token = token.replace('JWT', '', 1).strip()
    if not token:
        abort(401, "No token provided")
    if token_is_valid(token):
        return jsonify(True)
    abort(401)


@auth_blueprint.route('/api/v1/logout', methods=['GET'])
@check_auth
def logout():
    # To get past `check_auth` token is necessarily valid *EXCEPT* in testing env
    token = request.args.get('token')
    if not token:
        token = request.headers.get('Authorization')
        token = token.replace('JWT', '', 1).strip()
    with session_scope() as sess:
        tok = sess.query(UserToken).filter_by(token=token).first()
        sess.delete(tok)
    return jsonify({"success": True})
