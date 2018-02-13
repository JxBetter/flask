from flask import Blueprint, session, render_template, redirect, url_for, current_app, request, abort,flash
from blog.app.db_models import Role, User
from blog.app.form import EditProfileForm,EditProfileAdminForm,ShowWhoForm
from blog.app.factory import db
from blog.app.email_fun import send_email
from blog.app.decorators import admin_required
from blog.app.db_models import Permissions
from flask_login import login_required,current_user
from datetime import datetime

rootbp = Blueprint('root_bp', __name__, template_folder='root_bp_templates', static_folder='root_bp_static')


@rootbp.route('/')
def index():
    return render_template('index.html', current_time=datetime.utcnow())


@rootbp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('user.html', user=user)

@rootbp.route('/edit-profile',methods=['GET','POST'])
@login_required
def edit_profile():
    form=EditProfileForm()
    if form.validate_on_submit():
        current_user.name=form.name.data
        current_user.location=form.location.data
        current_user.about_me=form.about_me.data
        flash('Your profile has been updated.')
        return redirect(url_for('root_bp.user',username=current_user.username))
    form.name.data=current_user.name
    form.location.data=current_user.location
    form.about_me.data=current_user.about_me
    return render_template('edit-profile.html',form=form)


@rootbp.route('/edit-profile-admin/<who>',methods=['GET','POST'])
@login_required
@admin_required
def edit_profile_admin(who):
    form=EditProfileAdminForm()
    user = User.query.filter_by(username=who).first()
    if form.validate_on_submit():
        if user:
            form.set_user(user)
            if form.username.data != user.username and \
                not User.query.filter_by(username=form.username.data).first():
                user.username=form.username.data
            if form.email.data != user.email and \
                not User.query.filter_by(email=form.email.data).first():
                user.email=form.email.data
            user.email=form.email.data
            user.role = Role.query.get(form.role.data)
            user.name=form.name.data
            user.location=form.location.data
            user.about_me=form.about_me.data
            user.confirmed = form.confirmed.data
            db.session.add(user)
            db.session.commit()
            flash('Profile has been updated by admin.')
            return redirect(url_for('root_bp.user',username=current_user.username))
    form.name.data=user.name
    form.email.data=user.email
    form.username.data=user.username
    form.location.data=user.location
    form.about_me.data=user.about_me
    form.confirmed.data=user.confirmed
    return render_template('edit-profile.html',form=form)

@rootbp.route('/showho',methods=['GET','POST'])
@login_required
@admin_required
def showho():
    form=ShowWhoForm()
    if form.validate_on_submit():
        who=form.changewho.data
        if User.query.filter_by(username=who).first():
            return redirect(url_for('root_bp.edit_profile_admin',who=who))
        else:
            flash('not exist {}.'. format(who))
    return render_template('edit-profile.html',form=form)

@rootbp.app_context_processor
def inject_permissions():
    return dict(Permissions=Permissions)
