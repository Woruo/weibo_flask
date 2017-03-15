from routes import *
from models.weibo import Weibo, WCollect, WFavorite, Comment, CFavorite
from models.user import User, Follow

main = Blueprint('weibo', __name__)


def weibo_detail(ws, u, c_u):
    folowed_n = len(u.followed.all())
    followers_n = len(u.followers.all())
    cu_wl = len(u.weibos.all())
    ws_l = len(ws)
    is_followed = False
    if c_u:
        is_followed = c_u.is_following(u)
    for w in ws:
        w.user = User.query.filter_by(id=w.user_id).first()
        if c_u is not None:
            w.is_collected = WCollect.query.filter_by(user_id=c_u.id, weibo_id=w.id).first() is not None
            w.is_favored = WFavorite.query.filter_by(user_id=c_u.id, weibo_id=w.id).first() is not None
            w.is_comment = Comment.query.filter_by(user_id=c_u.id, weibo_id=w.id).first() is not None
        else:
            w.is_collected = None
            w.is_favored = None
            w.is_comment = None
        w.cite_w = Weibo.query.filter_by(id=w.origin_w_id).first()  # cite_w指微博原文
        if w.cite_w is not None:
            w.cite_w.user = User.query.filter_by(id=w.cite_w.user_id).first()
    form = {
        'folowed_n': folowed_n,
        'followers_n': followers_n,
        'ws_l': ws_l,
        'cu_wl': cu_wl,
        'weibos': ws,
        'user': u,
        'is_followed': is_followed
    }
    return form


@main.route('/hot')
def hot_weibo():
    ws = Weibo.query.filter_by(has_cite=False).order_by(Weibo.comments_num.desc()).all()
    c_u = current_user()
    if c_u is None:
        return render_template('weibo.html', weibos=ws)
    else:
        return render_template('weibo_find.html', weibos=ws, c_u=c_u, user=c_u)

@main.route('/tag/<int:tag_id>')
def tag_weibo(tag_id):
    ws = Weibo.query.filter(Weibo.tag_id == tag_id).filter_by(has_cite=False).order_by(Weibo.created_time.desc()).all()
    c_u = current_user()
    if c_u is None:
        return render_template('weibo.html', weibos=ws)
    else:
        return render_template('weibo_find.html', weibos=ws, c_u=c_u, user=c_u)


@main.route('/find')
def find_weibo():
    ws = Weibo.query.filter_by(has_cite=False).order_by(Weibo.created_time.desc()).all()
    c_u = current_user()
    return render_template('weibo_find.html', weibos=ws, c_u=c_u, user=c_u)


@main.route('/<int:user_id>/timeline')
@login_required
def timeline_view(u, user_id):
    ws = Weibo.query.join(Follow, Follow.followed_id == Weibo.user_id). \
        filter(Follow.follower_id == u.id).order_by(Weibo.created_time.desc()).all()
    form = weibo_detail(ws, u, u)
    return render_template('weibo_home.html', **form)


@main.route('/<int:user_id>/col_weibo')
@login_required
def col_weibo_view(u, user_id):
    ws = Weibo.query.join(WCollect, WCollect.weibo_id == Weibo.id). \
        filter(WCollect.user_id == u.id).order_by(Weibo.created_time.desc()).all()
    form = weibo_detail(ws, u, u)
    return render_template('weibo_collect.html', **form)


@main.route('/<int:user_id>/fav_weibo')
@login_required
def fav_weibo_view(u, user_id):
    ws = Weibo.query.join(WFavorite, WFavorite.weibo_id == Weibo.id). \
        filter(WFavorite.user_id == u.id).order_by(Weibo.created_time.desc()).all()
    form = weibo_detail(ws, u, u)
    return render_template('weibo_favor.html', **form)


@main.route('/<int:user_id>/tag/<int:tag_id>')
@login_required
def tag_weibo_view(u, user_id, tag_id):
    ws = Weibo.query.join(Follow, Follow.followed_id == Weibo.user_id). \
        filter(Follow.follower_id == u.id).filter(Weibo.tag_id == tag_id).order_by(Weibo.created_time.desc()).all()
    form = weibo_detail(ws, u, u)
    return render_template('weibo_home.html', **form)


@main.route('/<int:user_id>/homepage')
def homepage(user_id):
    u = User.query.get(user_id)
    c_u = current_user()
    ws = Weibo.query.filter_by(user_id=user_id).order_by(Weibo.created_time.desc()).all()
    form = weibo_detail(ws, u, c_u)
    return render_template('person_home.html', c_u=c_u, **form)


@main.route('/<int:id>/detail')
def detail(id):
    c_u = current_user()
    w = Weibo.query.get(id)
    if w.has_cite:
        o_w = Weibo.query.filter_by(id=w.origin_w_id).first()
        w.cite_w = o_w
        w.cite_w.user = User.query.filter_by(id=o_w.user_id).first()
    if w.comments_num != 0:
        for c in w.comments:
            c.user = User.query.get(c.user_id)
            c.is_favored = False
            if c_u is not None:
                c.is_favored = CFavorite.query.filter_by(user_id=c_u.id, comment_id=c.id).first() is not None
    return render_template('weibo_detail.html', w=w, c_u=c_u, user=c_u)


@main.route('/<int:user_id>/followed_detail')
def focus_detail(user_id):
    c_u = current_user()
    form = User.all_followed(user_id, c_u)
    is_followed = False
    if c_u:
        u = User.query.get(user_id)
        is_followed = c_u.is_following(u)
    form.update({'c_u': c_u, 'is_followed': is_followed})
    return render_template('person_followed.html', **form)


@main.route('/<int:user_id>/follower_detail')
def follower_detail(user_id):
    c_u = current_user()
    form = User.all_followers(user_id, c_u)
    is_followed = False
    if c_u:
        u = User.query.get(user_id)
        is_followed = c_u.is_following(u)
    form.update({'c_u': c_u, 'is_followed': is_followed})
    return render_template('person_followers.html', **form)
