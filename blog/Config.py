import os
class Config:
    SECRET_KEY=os.environ.get('SECRET_KEY') or 'i am gjx'
    SQLALCHEMY_COMMIT_ON_TEARDOWN=True
    SQLALCHEMY_TRACK_MODIFICATIONS=True
    MAIL_PREFIX='[EasyThink]'
    MAIL_SENDER='xxxx834033@163.com'
    MAIL_RECEIVER='4xx63@qq.com'
    
    @staticmethod
    def init_app(app):
	    pass


class DevelopmentConfig(Config):
    DEBUG=True
    MAIL_SERVER='smtp.163.com'
    MAIL_USE_TLS=True
    MAIL_USERNAME='xxx4033@163.com'
    MAIL_PASSWORD='xxxxxxx'
    SQLALCHEMY_DATABASE_URI='mysql://root:rootmysql@localhost/flask_web_db'


config={
    'default':DevelopmentConfig,
}
