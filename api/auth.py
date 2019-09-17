import datetime

import jwt
from functools import wraps
from flask import Blueprint, current_app, jsonify, request, abort

from api.models import User, UserToken, session_scope

def token_is_valid(token):
    try:
        _ = jwt.decode(token, key=current_app.config.get("SECRET_KEY"), algorithm='HS256')
    except jwt.ExpiredSignatureError:
        # TODO: Remove Token from DB
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
    token = request.headers.get('Authentication')
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
        if current_app.config.get('TESTING'):
            user = True
        if not user:
            return {"error": "User not authenticated"}, 401
        else:
            return func(*args, **kwargs)
    return wrapper

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/login', methods=['POST'])
def login():
    """Handle login requests
    """
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
            {'login': uname, 'iat': datetime.datetime.utcnow(),
            'exp': datetime.datetime.utcnow()+datetime.timedelta(30)},
            key=current_app.config.get("SECRET_KEY"),
            algorithm='HS256'
            ).decode()
        token = UserToken(token=jw_token)
        user.tokens.append(token)
        clean_tokens(user, sess)
    return jsonify({"success": True, "token": jw_token})


# @auth_blueprint.route('/logout', methods=['POST'])
# @check_auth
# def logout():
#     json = request.json
#     uname = json.get('login')
