from routes import *
from models.user import User
from utils import log
from routes import *

main = Blueprint('user', __name__)


@main.route('/')
def login_view():
    u = current_user()
    if u is None:
        return render_template('weibo.html')
    else:
        return redirect(url_for('weibo.timeline_view', user_id=u.id))


@main.route('/register', methods=['POST'])
def register():
    form = request.form
    u = User(form)
    user_id, msg = u.validate_register()
    if user_id is None:
        return api_response(message=msg)
    return api_response(True, {'id': user_id})


@main.route('/login', methods=['POST'])
def login():
    form = request.form
    u = User(form)
    user_id, msg = u.validate_login()
    if user_id is None:
        return api_response(message=msg)
    session['user_id'] = user_id
    return api_response(True, {'id': user_id}, message=msg)


@main.route('/profile')
def user_profile():
    user = current_user()
    pass
