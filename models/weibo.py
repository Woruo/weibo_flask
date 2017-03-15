from . import ModelMixin
from . import db
from . import timestamp, current_time, change_time
from models.user import User
from random import randint


class weiboTag(db.Model, ModelMixin):
    __tablename__ = 'weibotags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    weibos = db.relationship('Weibo', backref='weibotag', lazy='dynamic')

    def __init__(self, form):
        self.name = form.get('name', '')


class Weibo(db.Model, ModelMixin):
    __tablename__ = 'weibos'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500))
    created_time = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments_num = db.Column(db.Integer, default=0)
    fav_num = db.Column(db.Integer, default=0)
    col_num = db.Column(db.Integer, default=0)
    cite_num = db.Column(db.Integer, default=0)
    has_cite = db.Column(db.Boolean, default=False)
    cite_id = db.Column(db.Integer, default=0)
    origin_w_id = db.Column(db.Integer, default=0)
    is_hidden = db.Column(db.Integer, default=False)
    only_self = db.Column(db.Boolean, default=False)
    only_friends = db.Column(db.Boolean, default=False)
    comments = db.relationship(
        'Comment',
        backref='weibo',
        lazy='dynamic',
        order_by=lambda: Comment.created_time.desc()
    )
    tag_id = db.Column(db.Integer, db.ForeignKey('weibotags.id'))

    def __init__(self, form):
        self.content = form.get('content', '')
        self.created_time = current_time()
        self.tag_id = form.get('tag_id', None)
        self.cite_id = form.get('cite_id', None)
        self.origin_w_id = form.get('origin_w_id', None)

    def save_weibo(self, user):
        w = self.content.strip()
        l = len(w)
        if self.cite_id is not None:
            self.tag_id = Weibo.query.get(self.cite_id).tag_id
            self.has_cite = True
            cite_weibo = Weibo.query.get(self.cite_id)
            cite_weibo.cite_num += 1
            cite_weibo.save()
            if l == 0:
                self.content = "转发微博"
        l = len(w)
        if l < 1:
            return False, None, '微博长度至少为1个字符'
        elif self.tag_id != '5' and l > 140:
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

    @classmethod
    def show_cites_weibo(cls, weibo_id, user):
        if weibo_id is None:
            return False, None, '查询转发内容失败，该微博不存在'
        cites = Weibo.query.filter_by(cite_id=weibo_id).all()
        cs = []
        for c in cites:
            c.user = User.query.get(c.user_id)
            r = c.response()
            if WFavorite.query.filter_by(weibo_id=c.id, user_id=user.id).first() is not None:
                r['is_fav'] = True
            else:
                r['is_fav'] = False
            cs.append(r)
        print(cs)
        return True, cs, '查询转发评论成功'

    @classmethod
    def add_fake_weibo(cls):
        weibo = ['后端啊啊啊啊啊啊～', '前端啊啊啊啊啊啊～', '生活啊啊啊啊啊啊～', '互联网啊啊啊啊啊啊～',
                 '长微博啊啊啊啊啊啊～啊啊啊啊啊啊～啊啊啊啊啊啊～啊啊啊啊啊啊～啊啊啊啊啊啊～啊啊啊啊啊啊～\
                 啊啊啊啊啊啊～啊啊啊啊啊啊～啊啊啊啊啊啊～啊啊啊啊啊啊～啊啊啊啊啊啊～啊啊啊啊啊啊～啊啊啊啊啊啊～\
                 啊啊啊啊啊啊～啊啊啊啊啊啊～啊啊啊啊啊啊～啊啊啊啊啊啊～啊啊啊啊啊啊～啊啊啊啊啊啊～啊啊啊啊啊啊～\
                 啊啊啊啊啊啊～啊啊啊啊啊啊～啊啊啊啊啊啊～啊啊啊啊啊啊～啊啊啊啊啊啊～啊啊啊啊啊啊～啊啊啊啊啊啊～\
                 啊啊啊啊啊啊～啊啊啊啊啊啊～啊啊啊啊啊啊～啊啊啊啊啊啊～啊啊啊啊啊啊～啊啊啊啊啊啊～啊啊啊啊啊啊～\
                 啊啊啊啊啊啊～啊啊啊啊啊啊～啊啊啊啊啊啊～啊啊啊啊啊啊～啊啊啊啊啊啊～啊啊啊啊啊啊～啊啊啊啊啊啊～啊啊啊啊啊啊～啊啊啊啊啊啊～\
                 啊啊啊啊啊啊～啊啊啊啊啊啊～啊啊啊啊啊啊～']
        us = User.query.all()
        t_begin = 1483200000
        t_end = 1489475993
        for u in us:
            for i in range(0, 10):
                id = i % 5
                form = {
                    'content': weibo[id],
                    'tag_id': id + 1,
                }
                w = Weibo(form)
                w.user_id = u.id
                w.created_time = change_time(randint(t_begin, t_end))
                w.save()



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
            col_num=self.col_num,
            cite_num=self.cite_num,
        )


class WCollect(db.Model, ModelMixin):
    __tablename__ = 'wcollects'
    id = db.Column(db.Integer, primary_key=True)
    created_time = db.Column(db.String(100), default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    weibo_id = db.Column(db.Integer)

    def __init__(self, form):
        self.created_time = current_time()
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

    @classmethod
    def show_collect_weibo(cls, user):
        wcollects = user.wcollects.all()
        ws = []
        for wc in wcollects:
            w = Weibo.query.get(wc.weibo_id)
            ws.append(w.response())
        return True, ws, '查询用户收藏微博成功'

    @classmethod
    def add_fake_wcollect(cls):
        ws = Weibo.query.all()
        us = User.query.all()
        t_begin = 1483200000
        t_end = 1489475993
        for i in range(200):
            j = randint(0, len(ws) - 1)
            k = randint(0, len(us) - 1)
            w = ws[j]
            form = {
                'weibo_id': w.id,
            }
            wc = WCollect(form)
            wc.user_id = us[k].id
            wc.created_time = change_time(randint(t_begin, t_end))
            wc.save()
            w.col_num += 1
            w.save()

    def response(self):
        return dict(
            id=self.id,
            user_id=self.user_id,
            weibo_id=self.weibo_id,
        )


class WFavorite(db.Model, ModelMixin):
    __tablename__ = 'wfavorites'
    id = db.Column(db.Integer, primary_key=True)
    created_time = db.Column(db.String(100), default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    weibo_id = db.Column(db.Integer)

    def __init__(self, form):
        self.created_time = current_time()
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

    @classmethod
    def add_fake_wfavorite(cls):
        ws = Weibo.query.all()
        us = User.query.all()
        t_begin = 1483200000
        t_end = 1489475993
        for i in range(300):
            j = randint(0, len(ws) - 1)
            k = randint(0, len(us) - 1)
            w = ws[j]
            form = {
                'weibo_id': w.id,
            }
            wf = WFavorite(form)
            wf.user_id = us[k].id
            wf.created_time = change_time(randint(t_begin, t_end))
            wf.save()
            w.fav_num += 1
            w.save()

    def response(self):
        return dict(
            id=self.id,
            user_id=self.user_id,
            weibo_id=self.weibo_id,
        )


class Comment(db.Model, ModelMixin):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200))
    created_time = db.Column(db.String(100), default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    weibo_id = db.Column(db.Integer, db.ForeignKey('weibos.id'))
    fav_num = db.Column(db.Integer, default=0)
    chat_num = db.Column(db.Integer, default=0)
    is_hidden = db.Column(db.Integer, default=0)

    def __init__(self, form):
        self.content = form.get('content', '')
        self.created_time = current_time()
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
            r['is_fav'] = False
            if user is not None and CFavorite.query.filter_by(comment_id=c.id, user_id=user.id).first() is not None:
                r['is_fav'] = True
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

    @classmethod
    def add_fake_comment(cls):
        comment = ['我是沙发～', '沙发好，我是地板啊啊啊啊～，别踩我，疼！', '楼上真搞笑～', '这个微博的主题是什么啊啊啊～',
                   '长评论啊啊啊啊啊啊～啊啊啊啊啊啊～啊啊啊啊啊啊～啊啊啊啊啊啊～啊啊啊啊啊啊～啊啊啊啊啊啊～\
                   啊啊啊啊啊啊～啊啊啊啊啊啊～啊啊啊啊啊啊～啊啊啊啊啊啊～啊啊啊啊啊啊～啊啊啊啊啊啊～啊啊啊啊啊啊～\
                   啊啊啊啊啊啊～啊啊啊啊啊啊～啊啊啊啊啊啊～啊啊啊啊啊啊～\
                   啊啊啊啊啊啊～啊啊啊啊啊啊～听说可以100字', '诶呀，我就是想评论一下而已']
        l = len(comment)
        ws = Weibo.query.all()
        us = User.query.all()
        t_begin = 1483200000
        t_end = 1489475993
        for i in range(200):
            w = ws[randint(0, len(ws) - 1)]
            for id in range(l):
                user = us[randint(0, len(us) - 1)]
                form = {
                    'content': comment[id],
                    'weibo_id': w.id,
                }
                c = Comment(form)
                c.user_id = user.id
                c.created_time = change_time(randint(t_begin, t_end))
                c.save()
                w.comments_num += 1
                w.save()

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


class CFavorite(db.Model, ModelMixin):
    __tablename__ = 'cfavorites'
    id = db.Column(db.Integer, primary_key=True)
    created_time = db.Column(db.String(100), default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    weibo_id = db.Column(db.Integer)
    comment_id = db.Column(db.Integer)

    def __init__(self, form):
        self.created_time = current_time()
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

    @classmethod
    def add_fake_cfavorite(cls):
        cs = Comment.query.all()
        us = User.query.all()
        t_begin = 1483200000
        t_end = 1489475993
        for i in range(200):
            j = randint(0, len(cs) - 1)
            k = randint(0, len(us) - 1)
            c = cs[j]
            w = Weibo.query.get(c.weibo_id)
            form = {
                'comment_id': c.id,
                'weibo_id': w.id
            }
            cf = CFavorite(form)
            cf.user_id = us[k].id
            cf.created_time = change_time(randint(t_begin, t_end))
            cf.save()
            c.fav_num += 1
            c.save()

    def response(self):
        return dict(
            id=self.id,
            user_id=self.user_id,
            weibo_id=self.weibo_id,
            comment_id=self.comment_id,
        )

