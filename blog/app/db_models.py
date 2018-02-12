from werkzeug.security import generate_password_hash, check_password_hash
from blog.app.factory import db,loginmanager
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer
from flask import current_app

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role {}>'.format(self.name)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    confirmed=db.Column(db.Boolean,default=False)


    def __repr__(self):
        return '<User {}>'.format(self.username)

    @property
    def password(self):
        raise AttributeError('you cant get password!')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_token(self,time=1800):
        s=TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'],time)
        return s.dumps({'confirm':self.id})

    def confirm(self,token):
        s=TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'])
        try:
            data=s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed=True
        db.session.add(self)
        db.session.commit()
        return True

@loginmanager.user_loader
def load_user(userid):
    return User.query.get(int(userid))