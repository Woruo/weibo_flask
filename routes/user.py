from routes import *
from models.user import User
from models.weibo import Weibo
from utils import log
from routes import *


main = Blueprint('user', __name__)


@main.route('/')
def login_view():
    u = current_user()
    if u is None:
        ws = Weibo.query.filter_by(has_cite=False).order_by(Weibo.id.desc()).all()
        print('weibo', len(ws))
        return render_template('weibo.html', weibos=ws)
    if not u.confirmed:
        ws = Weibo.query.filter_by(has_cite=False).order_by(Weibo.id.desc()).all()
        print('weibo', len(ws))
        return render_template('weibo.html', weibos=ws)
    else:
        return redirect(url_for('weibo.timeline_view', user_id=u.id))


@main.route('/register', methods=['POST'])
def register():
    form = request.form
    u = User(form)
    user_id, msg = u.validate_register()
    if user_id is None:
        return api_response(message=msg)
    ws = Weibo.query.filter_by(has_cite=False).order_by(Weibo.id.desc()).all()
    return render_template('weibo.html', weibos=ws)


@main.route('/login', methods=['POST'])
def login():
    form = request.form
    u = User(form)
    user_id, msg = u.validate_login()
    if user_id is None:
        return api_response(message=msg)
    session['user_id'] = user_id
    return api_response(True, {'id': user_id}, message=msg)


@main.route('/logout')
@login_required
def logout():
    session.pop('user_id', None)
    return redirect(url_for('.login_view'))







