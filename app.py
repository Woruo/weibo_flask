from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell
from models import db


from routes.user import main as routes_user
from routes.weibo import main as routes_weibo
from routes.weibo_api import main as routes_api_weibo

app = Flask(__name__)
db_path = 'Wor.db'
secret_key = 'random_string'
FLASKY_MAIL_SUBJECT_PREFIX = '[Weibo_register]'
FLASKY_MAIL_SENDER = '731051689@qq.com'
FLASKY_ADMIN = 'Wor若'
MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = 587
MAIL_USERNAME = '731051689@qq.com'
MAIL_PASSWORD = 'pwyiftwecmccbbfh'

manager = Manager(app)


def register_route(app):
    app.register_blueprint(routes_user)
    app.register_blueprint(routes_weibo, url_prefix='/weibo')
    app.register_blueprint(routes_api_weibo, url_prefix='/api/weibo')


def configure_app():
    app.secret_key = secret_key
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(db_path)
    db.init_app(app)
    from routes import mail
    mail.init_app(app)
    register_route(app)



def configured_app():
    configure_app()
    return app


@manager.command
def server():
    app = configured_app()
    config = dict(
        debug=True,
        host='0.0.0.0',
        port=4000,
    )
    app.run(**config)


def make_shell_context():
    from models.user import User, Follow
    from models.weibo import Weibo, WCollect, WFavorite, Comment
    return dict(app=app, db=db, User=User, Follow=Follow, Comment=Comment)


def configure_manager():
    Migrate(app, db)
    manager.add_command('db', MigrateCommand)
    manager.add_command("shell", Shell(make_context=make_shell_context))
    manager.add_command('db', MigrateCommand)


if __name__ == "__main__":
    configure_manager()
    configure_app()
    manager.run()
