from . import ModelMixin
from . import db
from . import timestamp
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import hashlib
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
            for i in range(l // 2):
                j = randint(0, l-1)
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
    created_time = db.Column(db.Integer, default=0)
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

    def confirm(self, token):
        from app import secret_key
        s = Serializer(secret_key)
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        self.save()
        return True

    def generate_reset_token(self, expiration=3600):
        from app import secret_key
        s = Serializer(secret_key, expiration)
        return s.dumps({'reset': self.id})

    def reset_password(self, token, new_password):
        from app import secret_key
        s = Serializer(secret_key)
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        self.save()
        return True

    def generate_email_change_token(self, new_email, expiration=3600):
        from app import secret_key
        s = Serializer(secret_key, expiration)
        return s.dumps({'change_email': self.id, 'new_email': new_email})

    def generate_auth_token(self, expiration):
        from app import secret_key
        s = Serializer(secret_key,
                       expires_in=expiration)
        return s.dumps({'id': self.id})

    def change_email(self, token):
        from app import secret_key
        s = Serializer(secret_key)
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        self.avatar_hash = hashlib.md5(self.email.encode('utf-8')).hexdigest()
        self.save()
        return True

    @classmethod
    def add_fake_user(cls):
        username = ['Wor若', '瓜', '包', 'lin', 'SumNer', '菜', '森', 'HTML5',
                    'Python', 'Github精选', '我在扯淡', '微博小员工', '和菜头', 'vzch', 'winter', '徐白', 'Hush', '吹']
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
            u.get_avatar()
            u.save()


if __name__ == "__main__":
    u1 = User.query.get(1)
    form = dict(
        username='bao',
        password=123,
    )
    u2 = User(form)
    us = User.query.all()
    print('u1', u1)
    print('u2', u2)
    u1.follow(u2)
    print(u1.is_following(u2))
    u2.follow(u1)
    print(u1.is_followed_by(u2))
    print('u1.followed', u1.followed)
    print('u1.followers', u1.followers)
