from . import ModelMixin
from . import db
from . import timestamp
from werkzeug.security import generate_password_hash, check_password_hash
from random import randint


class Follow(db.Model, ModelMixin):
    __tablename__ = 'follows'
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    timestamp = db.Column(db.Integer)

    @classmethod
    def add_fake_follow(cls):
        us = User.query.all()
        l = len(us)
        for u in us:
            u.follow(u)
            for i in range(l // 2):
                j = randint(0, l - 1)
                u.follow(us[j])
                u.save()


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
    username = db.Column(db.String(), unique=True)
    password_hash = db.Column(db.String())
    created_time = db.Column(db.String(), default=0)
    avatar = db.Column(db.String())
    confirmed = db.Column(db.Boolean, default=False)
    email = db.Column(db.String(), default='', unique=True)
    note = db.Column(db.String(), default='')
    location = db.Column(db.String(), default='')
    intro = db.Column(db.String(), default='')
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
    tag_id = db.Column(db.Integer(), db.ForeignKey('usertags.id'))

    def __init__(self, form):
        self.username = form.get('username', '')
        self.email = form.get('email', '')
        self.password = form.get('password', '')
        self.created_time = timestamp()

    def get_avatar(self):
        avatar_n = str(self.id % 10)
        self.avatar = '/static/img/avatar_img/{}.jpg'.format(avatar_n)

    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def validate_register(self):
        err_msgs = ''
        suc_msg = '注册成功'
        if len(self.username) == 0:
            err_msgs += '用户名不能为空<br>'
        if len(self.password) <= 2:
            err_msgs += '密码长度必须大于2<br>'
        if err_msgs == '':
            self.hash_password()
            self.save()
            self.get_avatar()
            self.follow(self)
            self.save()
            return self.id, suc_msg
        err_msgs += '注册失败'
        return None, err_msgs

    def validate_login(self):
        err_msg = '登录失败'
        suc_msg = '登录成功'
        user = User.query.filter_by(username=self.username).first()
        print(self.password_hash, generate_password_hash('123'), user)
        if check_password_hash(user.password_hash, self.password):
            return user.id, suc_msg
        return None, err_msg

    def change_password(self, password):
        if len(password) > 2:
            self.password = password
            self.save()
            return True
        else:
            return False

    @classmethod
    def all_followed(cls, user_id, c_u):
        u = User.query.get(user_id)
        folowed_n = len(u.followed.all())
        followers_n = len(u.followers.all())
        fs = u.followed.all()
        f_us = []
        for f in fs:
            followed_u = User.query.get(f.followed_id)
            followed_u.followed_n = len(followed_u.followed.all())
            followed_u.followers_n = len(followed_u.followers.all())
            followed_u.weibo_n = len(followed_u.weibos.all())
            followed_u.is_followed_by_cu = c_u.is_following(followed_u)
            f_us.append(followed_u)
        form = {
            'folowed_n': folowed_n,
            'followers_n': followers_n,
            'f_us': f_us,
            'user': u,
        }
        return form

    @classmethod
    def all_followers(cls, user_id, c_u):
        u = User.query.get(user_id)
        folowed_n = len(u.followed.all())
        followers_n = len(u.followers.all())
        fs = u.followers.all()
        f_us = []
        for f in fs:
            follower_u = User.query.get(f.follower_id)
            follower_u.followed_n = len(follower_u.followed.all())
            follower_u.followers_n = len(follower_u.followers.all())
            follower_u.weibo_n = len(follower_u.weibos.all())
            follower_u.is_followed_by_cu = c_u.is_following(follower_u)
            f_us.append(follower_u)
        form = {
            'folowed_n': folowed_n,
            'followers_n': followers_n,
            'f_us': f_us,
            'user': u,
        }
        return form

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

    @classmethod
    def add_fake_user(cls):
        username = ['Wor若', '瓜', '包', 'lin', 'SumNer', '菜', '森', '菜菜',
                    '学姐', 'Github精选', '彭彭', '微博小员工', '菊', 'vzch', 'winter', '徐白', 'Hush', '吹', '夜弄影']
        location = ['北京', '上海', '杭州', '深圳', '广州']
        num = '1234567890'
        password = '123'
        password_hash = generate_password_hash(password)
        for i in range(len(username)):
            email = ''.join([num[randint(0, 9)] for i in range(9)]) + '@qq.com'
            form = {
                'username': username[i],
                'email': email,
            }
            u = User(form)
            u.confirmed = True
            u.location = location[randint(0, 4)]
            u.note = '我是北纬40度最帅的掏粪工'
            u.intro = '可爱的掏粪工'
            u.password_hash = password_hash
            u.save()
            u.follow(u)
            u.get_avatar()
            u.save()
