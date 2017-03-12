from routes import *
from utils import log
from models.weibo import Weibo, WCollect, WFavorite

main = Blueprint('weibo', __name__)


@main.route('/')
def weibo_view():
    return render_template('weibo.html')


@main.route('/<int:user_id>/timeline')
@login_required
def timeline_view(u, user_id):
    ws = Weibo.query.order_by(Weibo.id.desc()).all()
    folowed_n = len(u.followed.all())
    followers_n = len(u.followers.all())
    w_u = Weibo.query.filter_by(user_id=u.id).all()
    ws_l = len(w_u)
    for w in ws:
        w.user = User.query.filter_by(id=w.user_id).first()
        w.is_collected = WCollect.query.filter_by(user_id=u.id, weibo_id=w.id).first() is not None
        w.is_favored = WFavorite.query.filter_by(user_id=u.id, weibo_id=w.id).first() is not None
        w.cite_w = Weibo.query.filter_by(id=w.cite_id).first()
        if w.cite_w is not None:
            w.cite_w.user = User.query.filter_by(id=w.cite_w.user_id).first()
    return render_template('weibo_home.html', weibos=ws, user=u, ws_l=ws_l, folowed_n=folowed_n, followers_n=followers_n)


@main.route('/<int:user_id>/homepage')
def homepage(user_id):
    u = User.query.get(user_id)
    c_u = current_user()
    ws = Weibo.query.filter_by(user_id=user_id).order_by(Weibo.id.desc()).all()
    ws_l = len(ws)
    folowed_n = len(u.followed.all())
    followers_n = len(u.followers.all())
    for w in ws:
        w.user = User.query.filter_by(id=w.user_id).first()
        w.is_collected = WCollect.query.filter_by(user_id=u.id, weibo_id=w.id).first() is not None
        w.is_favored = WFavorite.query.filter_by(user_id=u.id, weibo_id=w.id).first() is not None
        w.cite_w = Weibo.query.filter_by(id=w.cite_id).first()
        if w.cite_w is not None:
            w.cite_w.user = User.query.filter_by(id=w.cite_w.user_id).first()
    return render_template('person_home.html', weibos=ws, u=u, ws_l=ws_l,
                            current_u=c_u, folowed_n=folowed_n, followers_n=followers_n)


@main.route('/<int:id>/detail')
def detail(id):
    c_u = current_user()
    w = Weibo.query.get(id)
    if w.has_cite:
        w.cite_w = Weibo.query.filter_by(id=w.cite_id).first()
        w.cite_w.user = User.query.filter_by(id=w.cite_w.user_id).first()
    for c in w.comments:
        c.avatar = User.query.get(c.user_id).avatar
    return render_template('weibo_detail.html', w=w, c_u=c_u)
