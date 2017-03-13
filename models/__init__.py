from flask_sqlalchemy import SQLAlchemy
import time
# from models.user import User
# from models.weibo import Weibo, WCollect, WFavorite

db = SQLAlchemy()

def current_time():
    format = '%Y/%m/%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    return dt


def timestamp():
    return int(time.time())


class ModelMixin(object):
    def __repr__(self):
        classname = self.__class__.__name__
        properties = ''.join(['{} : ({})\n'.format(k, v) for k, v in self.__dict__.items()])
        return '{}\n{}'.format(classname, properties)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
