from routes import *
from utils import log
from models.weibo import Weibo, WCollect, WFavorite, Comment, CFavorite
from models.user import User

main = Blueprint('weiboApi', __name__)


@main.route('/add', methods=['POST'])
@login_required
def add(user):
    form = request.form
    w = Weibo(form)
    status, data, msg = w.save_weibo(user)
    print('weibo add', status, data, msg)
    return api_response(status, data, msg)


@main.route('/delete', methods=['POST'])
@login_required
def delete(user):
    weibo_id = request.form.get('weibo_id', None)
    w = Weibo.query.get(weibo_id)
    if w is not None:
        status, data, msg = w.delete_weibo(user)
        print(status, data, msg)
    else:
        status, data, msg = False, None, '该微博不存在'
    return api_response(status, data, msg)


@main.route('/citeShow', methods=['POST'])
def citeShow():
    w_id = request.form.get('weibo_id', None)
    user = current_user()
    status, data, msg = Weibo.show_cites_weibo(w_id, user)
    return api_response(status, data, msg)


@main.route('/cite/add', methods=['POST'])
@login_required
def cite_add(user):
    form = request.form
    c = Weibo(form)
    status, data, msg = c.save_weibo(user)
    return api_response(status, data, msg)


@main.route('/commentShow', methods=['POST'])
def commentShow():
    w_id = request.form.get('weibo_id', None)
    user = current_user()
    status, data, msg = Comment.show_comments(w_id, user)
    return api_response(status, data, msg)


@main.route('/collect', methods=['POST'])
@login_required
def weibo_collect(user):
    form = request.form
    wc = WCollect(form)
    status, data, msg = wc.save_collect(user)
    return api_response(status, data, msg)


@main.route('/favorite', methods=['POST'])
@login_required
def weibo_favorite(user):
    form = request.form
    wf = WFavorite(form)
    status, data, msg = wf.save_Favorite(user)
    return api_response(status, data, msg)


@main.route('/comment/add', methods=['POST'])
@login_required
def comment_add(user):
    form = request.form
    c = Comment(form)
    status, data, msg = c.save_comment(user)
    return api_response(status, data, msg)


@main.route('/comment/favorite', methods=['POST'])
@login_required
def comment_favorite(user):
    form = request.form
    cc = CFavorite(form)
    status, data, msg = cc.save_Favorite(user)
    return api_response(status, data, msg)
