from . import ModelMixin
from . import db
from . import timestamp
from models.user import User


class weiboTag(db.Model, ModelMixin):
    __tablename__ = 'weibotags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    weibos = db.relationship('Weibo', backref='weibotag', lazy='dynamic')

    def __init__(self, form):
        self.name = form.get('name', '')


class Weibo(db.Model, ModelMixin):
    __tablename__ = 'weibos'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String())
    created_time = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments_num = db.Column(db.Integer, default=0)
    fav_num = db.Column(db.Integer, default=0)
    col_num = db.Column(db.Integer, default=0)
    cite_num = db.Column(db.Integer, default=0)
    has_cite = db.Column(db.Boolean, default=False)
    cite_id = db.Column(db.Integer, default=0)
    is_hidden = db.Column(db.Integer, default=0)
    comments = db.relationship(
        'Comment',
        backref='weibo',
        lazy='dynamic',
        order_by=lambda: Comment.created_time.desc()
    )
    tag_id = db.Column(db.String(), db.ForeignKey('weibotags.id'))

    def __init__(self, form):
        self.content = form.get('content', '')
        self.created_time = timestamp()
        self.tag_id = form.get('tag_id', None)

    def save_weibo(self, user):
        w = self.content.strip()
        l = len(w)
        if l < 3:
            return False, None, '微博长度至少为3个字符'
        elif l > 140:
            return False, None, '微博长度不能超过140个字符'
        else:
            self.user = user
            self.user_id = user.id
            self.save()
            return True, self.response(), '微博内容合法'

    def delete_weibo(self, user):
        if self.user_id == user.id:
            self.delete()
            return True, {'id': self.id}, '删除微博成功'
        else:
            return False, None, '非本人微博'

    def response(self):
        return dict(
            id=self.id,
            content=self.content,
            username=self.user.username,
            avatar=self.user.avatar,
            comments_num=self.comments_num,
            created_time=self.created_time,
            user_id=self.user_id,
            fav_num=self.fav_num,
        )


class WCollect(db.Model, ModelMixin):
    __tablename__ = 'wcollects'
    id = db.Column(db.Integer, primary_key=True)
    created_time = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    weibo_id = db.Column(db.Integer)

    def __init__(self, form):
        self.created_time = timestamp()
        self.weibo_id = form.get('weibo_id', None)

    def save_collect(self, user):
        if self.weibo_id is None:
            return False, None, '收藏失败，该微博不存在'
        wc_l = len(WCollect.query.filter_by(weibo_id=self.weibo_id, user_id=user.id).all())
        print('wc_l', wc_l, self.weibo_id, user.id)
        if wc_l == 0:
            self.user_id = user.id
            self.save()
            w = Weibo.query.get(self.weibo_id)
            w.col_num += 1
            w.save()
            return True, self.response(), '收藏成功'
        else:
            wc = WCollect.query.filter_by(weibo_id=self.weibo_id, user_id=user.id).first()
            wc.delete()
            w = Weibo.query.get(self.weibo_id)
            w.col_num -= 1
            w.save()
            return True, wc.response(), '取消收藏成功'

    def response(self):
        return dict(
            id=self.id,
            user_id=self.user_id,
            weibo_id=self.weibo_id,
        )


class WFavorite(db.Model, ModelMixin):
    __tablename__ = 'wfavorites'
    id = db.Column(db.Integer, primary_key=True)
    created_time = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    weibo_id = db.Column(db.Integer)

    def __init__(self, form):
        self.created_time = timestamp()
        self.weibo_id = form.get('weibo_id', None)

    def save_Favorite(self, user):
        if self.weibo_id is None:
            return False, None, '喜欢失败，该微博不存在'
        wf_l = len(WFavorite.query.filter_by(weibo_id=self.weibo_id, user_id=user.id).all())
        if wf_l == 0:
            self.user_id = user.id
            self.save()
            w = Weibo.query.get(self.weibo_id)
            w.fav_num += 1
            w.save()
            return True, self.response(), '喜欢成功'
        else:
            wf = WFavorite.query.filter_by(weibo_id=self.weibo_id, user_id=user.id).first()
            wf.delete()
            w = Weibo.query.get(wf.weibo_id)
            w.fav_num -= 1
            w.save()
            return True, wf.response(), '取消喜欢成功'

    def response(self):
        return dict(
            id=self.id,
            user_id=self.user_id,
            weibo_id=self.weibo_id,
        )


class Comment(db.Model, ModelMixin):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String())
    created_time = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    weibo_id = db.Column(db.Integer, db.ForeignKey('weibos.id'))
    fav_num = db.Column(db.Integer, default=0)
    chat_num = db.Column(db.Integer, default=0)
    is_hidden = db.Column(db.Integer, default=0)

    def __init__(self, form):
        self.content = form.get('content', '')
        self.created_time = timestamp()
        self.weibo_id = form.get('weibo_id', None)

    @classmethod
    def show_comments(cls, weibo_id, user):
        if weibo_id is None:
            return False, None, '查询评论失败，该微博不存在'
        comments = Comment.query.filter_by(weibo_id=weibo_id).all()
        cs = []
        for c in comments:
            c.user = User.query.get(c.user_id)
            r = c.response()
            if CFavorite.query.filter_by(comment_id=c.id, user_id=user.id).first() is not None:
                r['is_fav'] = True
            else:
                r['is_fav'] = False
            cs.append(r)
        print(cs)
        return True, cs, '查询评论成功'

    def save_comment(self, user):
        length = len(self.content.strip())
        if length < 1:
            return False, None, '评论需大于1个字符'
        elif length > 100:
            return False, None, '评论不能超过100个字符'
        self.user_id = user.id
        self.user = user
        self.weibo = Weibo.query.get(self.weibo_id)
        self.weibo.comments_num += 1
        self.save()
        return True, self.response(), '评论成功'

    def response(self):
        return dict(
            id=self.id,
            content=self.content,
            username=self.user.username,
            avatar=self.user.avatar,
            created_time=self.created_time,
            user_id=self.user_id,
            fav_num=self.fav_num,
        )


class Commentchat(db.Model, ModelMixin):
    __tablename__ = 'commentchats'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String())
    created_time = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer)
    weibo_id = db.Column(db.Integer)
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
    fav_num = db.Column(db.Integer, default=0)

    def __int__(self, form):
        self.content = form.get('content', '')
        self.created_time = timestamp()
        self.comment_id = form.get('comment_id', None)
        self.weibo_id = form.get('weibo_id', None)

    def save_chat(self, user):
        length = len(self.content.strip())
        if length < 1:
            return False, None, '评论需大于1个字符'
        elif length > 100:
            return False, None, '评论不能超过100个字符'
        self.user_id = user.id
        self.user = user
        self.comment = Comment.query.get(self.comment_id)
        self.comment.chat_num += 1
        self.save()
        return True, self.response(), '评论成功'


class CFavorite(db.Model, ModelMixin):
    __tablename__ = 'cfavorites'
    id = db.Column(db.Integer, primary_key=True)
    created_time = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    weibo_id = db.Column(db.Integer)
    comment_id = db.Column(db.Integer)

    def __init__(self, form):
        self.created_time = timestamp()
        self.weibo_id = form.get('weibo_id', None)
        self.comment_id = form.get('comment_id', None)

    def save_Favorite(self, user):
        if self.weibo_id is None:
            return False, None, '喜欢失败，该评论不存在'
        cf = CFavorite.query.filter_by(comment_id=self.comment_id, user_id=user.id).first()
        if cf is None:
            self.user_id = user.id
            self.save()
            c = Comment.query.get(self.comment_id)
            c.fav_num += 1
            c.save()
            return True, self.response(), '喜欢成功'
        else:
            cf.delete()
            c = Comment.query.get(cf.comment_id)
            c.fav_num -= 1
            c.save()
            return True, cf.response(), '取消喜欢成功'

    def response(self):
        return dict(
            id=self.id,
            user_id=self.user_id,
            weibo_id=self.weibo_id,
            comment_id=self.comment_id,
        )
