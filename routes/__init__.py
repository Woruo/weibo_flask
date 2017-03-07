from flask import Blueprint
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import send_from_directory
from flask import session
from flask import url_for
from flask import abort
import json
from functools import wraps

from models.user import User



def api_response(status=False, data=None, message=None):
    r = dict(
        success=status,
        data=data,
        message=message
    )
    print(json.dumps(r, ensure_ascii=False))
    return json.dumps(r, ensure_ascii=False)


def current_user():
    uid = session.get('user_id')
    if uid is not None:
        user = User.query.get(uid)
        return user
    else:
        return None


def login_required(f):
    @wraps(f)
    def function(*args, **kwargs):
        u = current_user()
        if u is None:
            return redirect(url_for('user.login_view'))
        return f(u, *args, **kwargs)

    return function