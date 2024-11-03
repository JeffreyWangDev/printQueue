import time
from flask import make_response, url_for, redirect
from users import User
from utils import hash

login_coookies = {}

def cheek_permission(request, permission:int):
    if request.cookies.get('id') is not None and request.cookies.get('auth') is not None:
        user_id = request.cookies.get('id')
        auth = request.cookies.get('auth')
        if login_coookies.get(int(user_id)) == auth:
            user = User.user_from_database(int(user_id))
            if user.permission >= permission:
                return True, user
    return False, None

def log_in(user):
    resp = make_response(redirect(url_for('home')))
    resp.set_cookie('id', str(user.id))
    auth = hash(str(time.time())+user.username+str(user.id))
    resp.set_cookie('auth', auth)
    login_coookies[user.id] = auth
    return resp

def log_out(request):
    permission_cheek = cheek_permission(request, 0)
    if permission_cheek[0]:
        login_coookies.pop(int(permission_cheek[1].id))
        resp = make_response(redirect(url_for('login')))
        resp.set_cookie('id', '', expires=0)
        resp.set_cookie('auth', '', expires=0)
        return resp
    return redirect(url_for('login'))