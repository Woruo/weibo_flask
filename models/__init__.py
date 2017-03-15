from flask_sqlalchemy import SQLAlchemy
import time

# from models.user import User
# from models.weibo import Weibo, WCollect, WFavorite

db = SQLAlchemy()


def current_time():
    format = '%Y/%m/%d %H:%M'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    return dt


def change_time(t):
    format = '%Y/%m/%d %H:%M'
    value = time.localtime(t)
    dt = time.strftime(format, value)
    return dt


def datetime_timestamp(dt):
    # dt为字符串
    # 中间过程，一般都需要将字符串转化为时间数组
    time.strptime(dt, '%Y/%m/%d %H:%M:%S')
    ## time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=-1)
    # 将"2012-03-28 06:53:40"转化为时间戳
    s = time.mktime(time.strptime(dt, '%Y/%m/%d %H:%M:%S'))
    return int(s)


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
