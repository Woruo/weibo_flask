from . import ModelMixin
from . import db
from . import timestamp
from models.user import User

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
