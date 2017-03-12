from routes import *
from utils import log
from models.weibo import Weibo, WCollect, WFavorite

main = Blueprint('weibo', __name__)


@main.route('/')
def weibo_view():
    return render_template('weibo.html')


@main.route('/<int:user_id>/timeline')
@login_required
def timeline_view(user, user_id):
    u = current_user()
    ws = Weibo.query.order_by(Weibo.id.desc()).all()
    for w in ws:
        w.user = User.query.filter_by(id=w.user_id).first()
        w.is_collected = WCollect.query.filter_by(user_id=u.id, weibo_id=w.id).first() is not None
        w.is_favored = WFavorite.query.filter_by(user_id=u.id, weibo_id=w.id).first() is not None
        w.cite_w = Weibo.query.filter_by(id=w.cite_id).first()
        if w.cite_w is not None:
            w.cite_w.user = User.query.filter_by(id=w.cite_w.user_id).first()
    return render_template('weibo_home.html', weibos=ws, user=u)


@main.route('/<int:user_id>/homepage')
def homepage(user_id):
    u = User.query.get(user_id)
    c_u = current_user()
    ws = Weibo.query.filter_by(user_id=user_id).order_by(Weibo.id.desc()).all()
    ws_l = len(ws)
    folowed_n = len(u.followed.all())
    followers_n = len(u.followers.all())
    print('homepage', u.username, len(ws),folowed_n, followers_n)
    return render_template('person_home.html', weibos=ws, u=u, ws_l=ws_l,
                            current_u=c_u, folowed_n=folowed_n, followers_n=followers_n)


@main.route('/weibo/<int:id>/detail')
def detail(id):
    w = Weibo.query.get(id)
    return render_template('weibo_detail.html', w=w)
