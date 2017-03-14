from flask import Blueprint
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import send_from_directory
from flask import session
from flask import url_for
from flask import abort
from flask_mail import Mail, Message
import json
from functools import wraps

from models.user import User

mail = Mail()


def api_response(status=False, data=None, message=None):
    r = dict(
        success=status,
        data=data,
        message=message
    )
    # print(json.dumps(r, ensure_ascii=False))
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
        if not u.confirmed:
            return redirect(url_for('user.login_view'))
        return f(u, *args, **kwargs)

    return function


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
                  sender = app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target = send_async_email, args = [app, msg])
    thr.start()
    return thr