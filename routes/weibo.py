from routes import *
from utils import log
from models.weibo import Weibo, WCollect, WFavorite

main = Blueprint('weibo', __name__)


@main.route('/')
def weibo_view():
    return render_template('weibo.html')


@main.route('/<int:user_id>/timeline')
def timeline_view(user_id):
    u = current_user()
    ws = Weibo.query.order_by(Weibo.id.desc()).all()
    for w in ws:
        w.user = User.query.filter_by(id=w.user_id).first()
        w.is_collected = WCollect.query.filter_by(user_id=u.id, weibo_id=w.id).first() is not None
        w.is_favored = WFavorite.query.filter_by(user_id=u.id, weibo_id=w.id).first() is not None
    return render_template('weibo_home.html', weibos=ws, user=u)


@main.route('/<int:user_id>/homepage')
def homepage(user_id):
    return render_template('person_home.html')
