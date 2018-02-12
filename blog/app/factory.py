from flask import Flask,render_template
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from blog.Config import config

import pymysql
pymysql.install_as_MySQLdb()

loginmanager=LoginManager()
bootstrap=Bootstrap()
moment=Moment()
db=SQLAlchemy()
mail=Mail()

loginmanager.session_protection='basic'
loginmanager.login_view='auth_bp.login'

def create_app(config_name):
    app=Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    loginmanager.init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    from blog.app.rootblueprint.rbp import rootbp
    from blog.app.errorblueprint.ebp import errorbp
    from blog.app.authblueprint.abp import authbp
    app.register_blueprint(authbp)
    app.register_blueprint(rootbp)
    app.register_blueprint(errorbp)
    return app
