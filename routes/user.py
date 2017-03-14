from routes import *
from models.user import User
from models.weibo import Weibo
from utils import log
from routes import *
from threading import Thread
from flask_mail import Mail
from flask import current_app

main = Blueprint('user', __name__)


@main.route('/')
def login_view():
    u = current_user()
    if u is None:
        ws = Weibo.query.filter_by(has_cite=False).order_by(Weibo.id.desc()).all()
        print('weibo', len(ws))
        return render_template('weibo.html', weibos=ws)
    if not u.confirmed:
        ws = Weibo.query.filter_by(has_cite=False).order_by(Weibo.id.desc()).all()
        print('weibo', len(ws))
        return render_template('weibo.html', weibos=ws)
    else:
        return redirect(url_for('weibo.timeline_view', user_id=u.id))


@main.route('/register', methods=['POST'])
def register():
    form = request.form
    u = User(form)
    user_id, msg = u.validate_register()
    if user_id is None:
        return api_response(message=msg)
    ws = Weibo.query.filter_by(has_cite=False).order_by(Weibo.id.desc()).all()
    return render_template('weibo.html', weibos=ws)


@main.route('/login', methods=['POST'])
def login():
    form = request.form
    u = User(form)
    user_id, msg = u.validate_login()
    if user_id is None:
        return api_response(message=msg)
    session['user_id'] = user_id
    return api_response(True, {'id': user_id}, message=msg)


@main.route('/logout')
@login_required
def logout():
    session.pop('user_id', None)
    return redirect(url_for('.login_view'))
















@main.route('/confirm/<token>')
@login_required
def confirm(user, token):
    if user.confirmed:
        return redirect(url_for('main.index'))
    if user.confirm(token):
        msg = '你已经确认你的账号，谢谢！'
    else:
        msg = '确认链接非法或者已经失效'
    return redirect(url_for('main.index'))


@main.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@main.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
               'auth/email/confirm', user=current_user, token=token)
    flash(u'新的确认邮件已经发到你的邮箱')
    return redirect(url_for('main.index'))


@main.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash(u'你的密码已经更新')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid password.')
    return render_template('auth/change_password.html', form=form)


@main.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, 'Reset Your Password',
                       'auth/email/reset_password',
                       user=user, token=token,
                       next=request.args.get('next'))
        flash(u'重置密码的链接已经发送到你的邮箱')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


@main.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            return redirect(url_for('main.index'))
        if user.reset_password(token, form.password.data):
            flash(u'你的密码已经更新')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)


@main.route('/change-email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data
            token = current_user.generate_email_change_token(new_email)
            send_email(new_email, 'Confirm your email address',
                       'auth/email/change_email',
                       user=current_user, token=token)
            flash(u'重置密码的链接已经发送到你的邮箱')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid email or password.')
    return render_template('auth/change_email.html', form=form)


@main.route('/change-email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        flash(u'你的邮箱地址已经更新')
    else:
        flash(u'非法请求')
    return redirect(url_for('main.index'))


@main.route('/profile')
def user_profile():
    user = current_user()
    pass
