from flask_wtf import FlaskForm
from wtforms import ValidationError
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo
from blog.app.db_models import User

class Login_Form(FlaskForm):
    username_email = StringField('Username or Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    keep = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class Registration_Form(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 64), Regexp(
        '^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Username must be letters, numbers, dots,underscores')])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(1, 64)])
    password1=PasswordField('Password',validators=[DataRequired(),EqualTo('password2',message='Password must match')])
    password2=PasswordField('Confirm your Password',validators=[DataRequired()])
    submit=SubmitField('Register!')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already been registered.')

    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already been registered.')

class Reset_Form(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    submit=SubmitField('Reset')

    def validate_username(self,field):
        if not User.query.filter_by(username=field.data).first():
            raise ValidationError('Username or Email not exist!')


class Reset_Password_Form(FlaskForm):
    password1=PasswordField('Password',validators=[DataRequired(),EqualTo('password2',message='Password must match')])
    password2=PasswordField('Confirm your Password',validators=[DataRequired()])
    submit=SubmitField('Go.')

class Email_Form(FlaskForm):
    email = StringField('Old email', validators=[DataRequired(), Email(), Length(1, 64)])
    submit=SubmitField('Check')

class Change_Email_Form(FlaskForm):
    email=StringField('New email',validators=[DataRequired(),Email()])
    submit=SubmitField('Go.')