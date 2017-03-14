from routes import *
from models.weibo import Weibo, WCollect, WFavorite, Comment
from models.user import User, Follow

main = Blueprint('weibo', __name__)


def weibo_detail(ws, u):
    folowed_n = len(u.followed.all())
    followers_n = len(u.followers.all())
    w_u = Weibo.query.filter_by(user_id=u.id).all()
    ws_l = len(w_u)
    for w in ws:
        w.user = User.query.filter_by(id=w.user_id).first()
        w.is_collected = WCollect.query.filter_by(user_id=u.id, weibo_id=w.id).first() is not None
        w.is_favored = WFavorite.query.filter_by(user_id=u.id, weibo_id=w.id).first() is not None
        w.is_comment = Comment.query.filter_by(user_id=u.id, weibo_id=w.id).first() is not None
        w.origin_w = Weibo.query.filter_by(id=w.origin_w_id).first()
        if w.origin_w is not None:
            w.origin_w.user = User.query.filter_by(id=w.origin_w.user_id).first()
    form = {
        'folowed_n': folowed_n,
        'followers_n': followers_n,
        'ws_l': ws_l,
        'weibos': ws,
        'user': u
    }
    return form


@main.route('/<int:user_id>/timeline')
@login_required
def timeline_view(u, user_id):
    ws = Weibo.query.join(Follow, Follow.followed_id == Weibo.user_id). \
        filter(Follow.follower_id == u.id).order_by(Weibo.created_time.desc()).all()
    print('length of weibo', len(ws))
    form = weibo_detail(ws, u)
    return render_template('weibo_home.html', **form)


@main.route('/<int:user_id>/col_weibo')
@login_required
def col_weibo_view(u, user_id):
    ws = Weibo.query.join(WCollect, WCollect.weibo_id == Weibo.id). \
        filter(WCollect.user_id == u.id).order_by(Weibo.created_time.desc()).all()
    print('length of collect weibo', len(ws))
    form = weibo_detail(ws, u)
    return render_template('weibo_collect.html', **form)


@main.route('/<int:user_id>/fav_weibo')
@login_required
def fav_weibo_view(u, user_id):
    ws = Weibo.query.join(WFavorite, WFavorite.weibo_id == Weibo.id). \
        filter(WFavorite.user_id == u.id).order_by(Weibo.created_time.desc()).all()
    print('length of collect weibo', len(ws))
    form = weibo_detail(ws, u)
    return render_template('weibo_favor.html', **form)


@main.route('/<int:user_id>/tag/<int:tag_id>')
@login_required
def tag_weibo_view(u, user_id, tag_id):
    ws = Weibo.query.join(Follow, Follow.followed_id == Weibo.user_id). \
        filter(Follow.follower_id == u.id).filter(Weibo.tag_id == tag_id).order_by(Weibo.created_time.desc()).all()
    print('tag weibo', tag_id, len(ws))
    form = weibo_detail(ws, u)
    return render_template('weibo_home.html', **form)


@main.route('/<int:user_id>/homepage')
def homepage(user_id):
    u = User.query.get(user_id)
    c_u = current_user()
    ws = Weibo.query.filter_by(user_id=user_id).order_by(Weibo.created_time.desc()).all()
    form = weibo_detail(ws, u)
    return render_template('person_home.html', c_u=c_u, **form)


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



@main.route('/<int:user_id>/focus_detail')
def focus_detail(user_id):
    c_u = current_user()
    u = User.query.get(user_id)
    folowed_n = len(u.followed.all())
    followers_n = len(u.followers.all())
    fs = u.followed.all()
    form = {
        'folowed_n': folowed_n,
        'followers_n': followers_n,
        'fs': fs,
        'user': u,
        'c_u': c_u
    }
    return render_template('followed_detail.html', **form)


@main.route('/<int:user_id>/follower_detail')
def follower_detail(user_id):
    c_u = current_user()
    u = User.query.get(user_id)
    folowed_n = len(u.followed.all())
    followers_n = len(u.followers.all())
    fs = u.followed.all()
    form = {
        'folowed_n': folowed_n,
        'followers_n': followers_n,
        'fs': fs,
        'user': u,
        'c_u': c_u
    }
    return render_template('follower_detail.html', w=w, c_u=c_u)
