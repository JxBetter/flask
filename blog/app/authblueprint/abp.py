from flask import Blueprint, render_template, redirect, url_for, flash, request,current_app
from flask_login import login_required, login_user, logout_user, current_user
from blog.app.form import Login_Form, Registration_Form, Reset_Form, Reset_Password_Form, Email_Form, Change_Email_Form
from blog.app.db_models import User,Role,Permissions
from blog.app.factory import db
from blog.app.email_fun import send_email
import hashlib

authbp = Blueprint('auth_bp', __name__,
                   template_folder='auth_bp_templates',
                   static_folder='auth_bp_static')


@authbp.route('/login', methods=['GET', 'POST'])
def login():
    form = Login_Form()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.username_email.data).first() \
               or User.query.filter_by(username=form.username_email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.keep.data)
            return redirect(url_for('root_bp.index'))
        flash('Invalid Username/Email or Password.')
    return render_template('login.html', form=form)


@authbp.route('/logout', methods=['GET'])
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('root_bp.index'))


@authbp.route('/register', methods=['GET', 'POST'])
def register():
    form = Registration_Form()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=form.password1.data, )
        db.session.add(user)
        db.session.commit()
        token = user.generate_token()
        send_email(user.email,
                   'Confirm Your Account',
                   'confirm',
                   enable=True,
                   user=user,
                   token=token)
        flash('Regrister Successful,Now you can login.')
        return redirect(url_for('.login'))
    return render_template('register.html', form=form)


@authbp.route('/confirm/<token>/<name>')
def confirm(token, name):
    user = User.query.filter_by(username=name).first()
    if user.confirmed:
        return redirect(url_for('root_bp.index'))
    if user.confirm(token):
        flash('You have confirmed your account.')
    else:
        flash('The confirmation link is invalid.')
    return redirect(url_for('root_bp.index'))


@authbp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.endpoint[:8] != 'auth_bp.' \
            and request.endpoint != 'static':
        return redirect(url_for('auth_bp.unconfirmed'))


@authbp.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect('root_bp.index')
    return render_template('unconfirmed.html')


@authbp.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_token()
    send_email(current_user.email,
               'Confirm Your Account',
               'confirm',
               enable=True,
               user=current_user,
               token=token)
    flash('A new confirmation email has been sent to you.')
    return redirect(url_for('root_bp.index'))


@authbp.route('/reset/password', methods=['GET', 'POST'])
def reset_password():
    form = Reset_Form()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        token = user.generate_token()
        send_email(user.email,
                   'Reset Your Password',
                   'reset_password',
                   enable=True,
                   user=user,
                   token=token)
        flash('We send a email to you for reseting your password.')
    return render_template('reset.html', form=form)


@authbp.route('/reset/password/<token>/<name>', methods=['GET', 'POST'])
def real_reset(token, name):
    user = User.query.filter_by(username=name).first()
    form = Reset_Password_Form()
    if form.validate_on_submit():
        if user.confirm(token):
            user.password = form.password1.data
            db.session.add(user)
            db.session.commit()
            flash('reset password successful.')
        else:
            flash('reset failed!')
        return redirect(url_for('auth_bp.login'))
    return render_template('reset.html', form=form)


@authbp.route('/change/password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = Reset_Password_Form()
    if form.validate_on_submit():
        current_user.password = form.password1.data
        logout_user()
        flash('Your password has been changed.')
        return redirect(url_for('auth_bp.login'))
    return render_template('reset.html', form=form)


@authbp.route('/check/oldemail', methods=['GET', 'POST'])
@login_required
def check_old_email():
    form = Email_Form()
    if form.validate_on_submit():
        token = current_user.generate_token()
        if form.email.data == current_user.email:
            send_email(form.email.data,
                       'Check Your Old Email',
                       'check_old_email',
                       enable=True,
                       token=token,
                       user=current_user)
            flash('We have sent a email to you for checking your old email.')
            return redirect(url_for('root_bp.index'))
        else:
            flash('Invalid Email')
    return render_template('reset.html', form=form)


@authbp.route('/check/newemail/<token>', methods=['GET', 'POST'])
@login_required
def check_new_email(token):
    form = Change_Email_Form()
    if form.validate_on_submit():
        if current_user.confirm(token):
            new_token = current_user.generate_token()
            send_email(form.email.data,
                       'Change New Email',
                       'change_new_email',
                       enable=True,
                       token=new_token,
                       user=current_user)
            current_user.email = form.email.data
            current_user.avatar_hash=hashlib.md5(current_user.email.encode('utf-8')).hexdigest()
            if form.email.data == current_app.config.get('MAIL_USERNAME'):
                current_user.role=Role.query.filter_by(permissions=0xff).first()
            flash('Your email has changed to {}'.format(form.email.data))
        return redirect(url_for('root_bp.index'))
    return render_template('reset.html', form=form)


@authbp.route('/test')
@login_required
def test():
    return render_template('test.html',name='gujinxin')
