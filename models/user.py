from . import ModelMixin
from . import db
from . import timestamp



class Follow(db.Model, ModelMixin):
    __tablename__ = 'follows'
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    timestamp = db.Column(db.Integer)


class userTag(db.Model, ModelMixin):
    __tablename__ = 'usertags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    users = db.relationship('User', backref='usertag', lazy='dynamic')

    def __init__(self, form):
        self.name = form.get('name', '')


class User(db.Model, ModelMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String())
    password = db.Column(db.String())
    created_time = db.Column(db.Integer, default=0)
    avatar = db.Column(db.String())
    email = db.Column(db.String(), default='')
    signature = db.Column(db.String())
    weibos = db.relationship('Weibo', backref='user', lazy='dynamic', order_by="desc(Weibo.id)")
    comments = db.relationship('Comment', backref='user', lazy='dynamic', order_by="desc(Comment.id)")
    followed = db.relationship('Follow',
                               foreign_keys='Follow.follower_id',
                               backref=db.backref('follower', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')
    followers = db.relationship('Follow',
                                foreign_keys='Follow.followed_id',
                                backref=db.backref('followed', lazy='joined'),
                                lazy='dynamic',
                                cascade='all, delete-orphan')
    wcollects = db.relationship('WCollect', backref='user', lazy='dynamic', order_by='desc(WCollect.id)')
    wfavorites = db.relationship('WFavorite', backref='user', lazy='dynamic', order_by='desc(WFavorite.id)')
    cfavorites = db.relationship('CFavorite', backref='user', lazy='dynamic', order_by='desc(CFavorite.id)')
    tag_id = db.Column(db.String(), db.ForeignKey('usertags.id'))

    def __init__(self, form):
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.created_time = timestamp()

    def get_avatar(self):
        avatar_n = str(self.id % 10)
        self.avatar = '/static/img/avatar_img/{}.jpg'.format(avatar_n)

    def validate_register(self):
        err_msgs = ''
        suc_msg = '注册成功'
        if len(self.username) == 0:
            err_msgs += '用户名不能为空<br>'
        if len(self.password) <= 2:
            err_msgs += '密码长度必须大于2<br>'
        if err_msgs == '':
            self.save()
            self.get_avatar()
            self.save()
            return self.id, suc_msg
        err_msgs += '注册失败'
        return None, err_msgs

    def validate_login(self):
        err_msg = '登录失败'
        suc_msg = '登录成功'
        user = User.query.filter_by(username=self.username,
                                    password=self.password).first()
        if user is not None:
            return user.id, suc_msg
        return None, err_msg

    def change_password(self, password):
        if len(password) > 2:
            self.password = password
            self.save()
            return True
        else:
            return False

    def follow(self, user):
        fe = self.followed.filter_by(followed_id=user.id).first()
        if fe is None:
            f = Follow(follower=self, followed=user)
            f.save()

    def unfollow(self, user):
        fe = self.followed.filter_by(followed_id=user.id).first()
        if fe is not None:
            fe.delete()

    def is_following(self, user):
        return self.followed.filter_by(followed_id=user.id).first() is not None

    def is_followed_by(self, user):
        return self.followers.filter_by(follower_id=user.id).first() is not None

    def is_admin(self):
        return self.id == 1
