from flask import Blueprint, session, render_template, redirect, url_for, current_app, request, abort, flash, jsonify
from blog.app.db_models import Role, User, Article, Comment
from blog.app.form import EditProfileForm, EditProfileAdminForm, ShowWhoForm, ArticleForm, CommentForm
from blog.app.factory import db
from blog.app.email_fun import send_email
from blog.app.decorators import admin_required
from blog.app.db_models import Permissions
from flask_login import login_required, current_user
from itsdangerous import TimedJSONWebSignatureSerializer
from datetime import datetime

rootbp = Blueprint('root_bp', __name__, template_folder='root_bp_templates', static_folder='root_bp_static')

res = {}


@rootbp.route('/', methods=['GET', 'POST'])
def index():
    form = ArticleForm()
    if current_user.can(Permissions.WRITE_ARTICLES) and \
            form.validate_on_submit():
        article = Article(title=form.title.data,
                          body=form.body.data,
                          author=current_user._get_current_object())
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('root_bp.index'))
    page = request.args.get('page', 1, type=int)
    pagination = Article.query.order_by(Article.editstamp.desc()).paginate(page,
                                                                           per_page=current_app.config[
                                                                               'ARTICLES_PER_PAGE'],
                                                                           error_out=False)
    articles = pagination.items
    return render_template('index.html', form=form, articles=articles, pagination=pagination)

@rootbp.route('/gs', methods=['GET', 'POST'])
def grand_service():
    keys = ['deviceKey', 'personGuid', 'showTime', 'photoUrl', 'type', 'data']
    if request.method == 'POST':
        print('get_json: ', request.get_json())
        for key in keys:
            res[key] = request.args.get(key)
            #if res[key] == None:
                #res[key] = request.form.get(key)
            print(request.args.get(key))
    return jsonify(res)


@rootbp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    articles = user.articles.order_by(Article.timestamp.desc()).all()
    return render_template('user.html', user=user, articles=articles)


@rootbp.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        flash('Your profile has been updated.')
        return redirect(url_for('root_bp.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit-profile.html', form=form)


@rootbp.route('/edit-profile-admin/<who>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(who):
    form = EditProfileAdminForm()
    user = User.query.filter_by(username=who).first()
    if form.validate_on_submit():
        if user:
            form.set_user(user)
            if form.username.data != user.username and \
                    not User.query.filter_by(username=form.username.data).first():
                user.username = form.username.data
            if form.email.data != user.email and \
                    not User.query.filter_by(email=form.email.data).first():
                user.email = form.email.data
            user.email = form.email.data
            user.role = Role.query.get(form.role.data)
            user.name = form.name.data
            user.location = form.location.data
            user.about_me = form.about_me.data
            user.confirmed = form.confirmed.data
            db.session.add(user)
            db.session.commit()
            flash('Profile has been updated by admin.')
            return redirect(url_for('root_bp.user', username=current_user.username))
    form.name.data = user.name
    form.email.data = user.email
    form.username.data = user.username
    form.location.data = user.location
    form.about_me.data = user.about_me
    form.confirmed.data = user.confirmed
    return render_template('edit-profile.html', form=form)


@rootbp.route('/showho', methods=['GET', 'POST'])
@login_required
@admin_required
def showho():
    form = ShowWhoForm()
    if form.validate_on_submit():
        who = form.changewho.data
        if User.query.filter_by(username=who).first():
            return redirect(url_for('root_bp.edit_profile_admin', who=who))
        else:
            flash('not exist {}.'.format(who))
    return render_template('edit-profile.html', form=form)


@rootbp.route('/article/<token>',methods=['GET','POST'])
def per_article(token):
    s=TimedJSONWebSignatureSerializer(current_app.config['ARTICLE_KEY'])
    try:
        data = s.loads(token)
        article = Article.query.filter_by(id=data.get('confirm')).first()
    except:
        abort(500)
    form=CommentForm()
    if form.validate_on_submit():
        comment=Comment(body=form.body.data,
                       article=article,
                       author=current_user._get_current_object())
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('root_bp.per_article',token=article.generate_token(),page=-1))
    page=request.args.get('page',1,type=int)
    if page == -1:
        page=(article.comments.count()-1) / \
             current_app.config['ARTICLES_PER_PAGE']+1
    pagination=article.comments.order_by(Comment.timestamp.asc()).paginate(
                                            page,per_page=current_app.config['ARTICLES_PER_PAGE'],error_out=False)
    comments=pagination.items
    return render_template('per_article.html', article=article,form=form,comments=comments,pagination=pagination)

@rootbp.route('/edit_article/<int:id>',methods=['GET','POST'])
@login_required
def edit_article(id):
    article=Article.query.get_or_404(id)
    if current_user != article.author and not current_user.is_administrator():
        abort(403)
    form=ArticleForm()
    if form.validate_on_submit():
        article.title=form.title.data
        article.body=form.body.data
        article.editstamp=datetime.utcnow()
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('root_bp.index'))
    return render_template('edit_article.html',form=form)

@rootbp.route('/delete_article/<article_id>')
def del_article(article_id):
    article=Article.query.filter_by(id=article_id).first()
    db.session.delete(article)
    db.session.commit()
    return redirect(url_for('root_bp.index'))

@rootbp.app_context_processor
def inject_permissions():
    return dict(Permissions=Permissions)
