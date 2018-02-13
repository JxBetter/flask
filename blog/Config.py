import os
class Config:
    SECRET_KEY=os.environ.get('SECRET_KEY') or 'i am gjx'
    SQLALCHEMY_COMMIT_ON_TEARDOWN=True
    SQLALCHEMY_TRACK_MODIFICATIONS=True
    MAIL_PREFIX='[EasyThink]'
    MAIL_SENDER='15705834033@163.com'
    MAIL_RECEIVER='429803863@qq.com'
    
    @staticmethod
    def init_app(app):
	    pass


class DevelopmentConfig(Config):
    DEBUG=True
    MAIL_SERVER='smtp.163.com'
    MAIL_USE_TLS=True
    MAIL_USERNAME='15705834033@163.com'
    MAIL_PASSWORD='gujinxin9608'
    SQLALCHEMY_DATABASE_URI='mysql://root:rootmysql@localhost/flask_web_db'


config={
    'default':DevelopmentConfig,
}
