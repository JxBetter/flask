import os
class Config:
    SECRET_KEY=os.environ.get('SECRET_KEY') or 'i am gjx'
    ARTICLE_KEY='qpalzmtgb'
    SQLALCHEMY_COMMIT_ON_TEARDOWN=True
    SQLALCHEMY_TRACK_MODIFICATIONS=True
    MAIL_PREFIX='[EasyThink]'
    MAIL_SENDER='15705834033@163.com'
    MAIL_RECEIVER='429803863@qq.com'
    DEBUG=True
    MAIL_SERVER='smtp.163.com'
    MAIL_USE_TLS=True
    MAIL_USERNAME='15705834033@163.com'
    MAIL_PASSWORD='gujinxin9608'
    ARTICLES_PER_PAGE=25
    SSL_DISABLE=True
    MAIL_SENDER='15705834033@163.com'
    MAIL_RECEIVER='42980386363@qq.com'
    
    @staticmethod
    def init_app(app):
	    pass


class DevelopmentConfig(Config):
    DEBUG=True
    MAIL_SERVER='smtp.163.com'
    MAIL_USE_TLS=True
    MAIL_USERNAME='15705834033@163.com'
    MAIL_PASSWORD='gujinxin9608'
    SQLALCHEMY_DATABASE_URI='mysql://root:rootmysql@0.0.0.0/flask_web_db'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:rootmysql@0.0.0.0/flask_web_db'

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # email errors to the administrators
        import logging
        from logging.handlers import SMTPHandler
        credentials = None
        secure = None
        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_TLS', None):
                secure = ()
        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.FLASKY_MAIL_SENDER,
            toaddrs=[cls.FLASKY_ADMIN],
            subject=cls.FLASKY_MAIL_SUBJECT_PREFIX + ' Application Error',
            credentials=credentials,
            secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)


class HerokuConfig(ProductionConfig):
    SSL_REDIRECT = True if os.environ.get('DYNO') else False
    SSL_DISABLE=True
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # handle reverse proxy server headers
        from werkzeug.contrib.fixers import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app)

        # log to stderr
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        from werkzeug.contrib.fixers import ProxyFix
        app.wsgi_app=ProxyFix(app.wsgi_app)


config={
    'default':DevelopmentConfig,
    'heroku':HerokuConfig,
}
