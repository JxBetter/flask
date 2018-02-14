from flask_wtf import FlaskForm
from wtforms import ValidationError
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo
from blog.app.db_models import User, Role
from flask_pagedown.fields import PageDownField
from flask_login import current_user


class Login_Form(FlaskForm):
    username_email = StringField('Username or Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    keep = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class Registration_Form(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 64), Regexp(
        '^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Username must be letters, numbers, dots,underscores')])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(1, 64)])
    password1 = PasswordField('Password',
                              validators=[DataRequired(), EqualTo('password2', message='Password must match')])
    password2 = PasswordField('Confirm your Password', validators=[DataRequired()])
    submit = SubmitField('Register!')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already been registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already been registered.')


class Reset_Form(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Reset')

    def validate_username(self, field):
        if not User.query.filter_by(username=field.data).first():
            raise ValidationError('Username or Email not exist!')


class Reset_Password_Form(FlaskForm):
    password1 = PasswordField('Password',
                              validators=[DataRequired(), EqualTo('password2', message='Password must match')])
    password2 = PasswordField('Confirm your Password', validators=[DataRequired()])
    submit = SubmitField('Go.')


class Email_Form(FlaskForm):
    email = StringField('Old email', validators=[DataRequired(), Email(), Length(1, 64)])
    submit = SubmitField('Check')


class Change_Email_Form(FlaskForm):
    email = StringField('New email', validators=[DataRequired(), Email()])
    submit = SubmitField('Go.')


class EditProfileForm(FlaskForm):
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')


class EditProfileAdminForm(FlaskForm):
    email = StringField('Email', validators=[Email(), Length(0, 64)])
    username = StringField('Username', validators=[DataRequired(), Length(1, 64), Regexp(
        '^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Username must be letters, numbers, dots,underscores')])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
        self.user = None

    def set_user(self, user):
        self.user = user


class ShowWhoForm(FlaskForm):
    changewho = StringField('ChangeWho?', validators=[DataRequired(), Length(1, 64)])
    submit = SubmitField('Submit')


class ArticleForm(FlaskForm):
    title=StringField('Title',validators=[DataRequired()])
    body=PageDownField('Say something',validators=[DataRequired()])
    submit=SubmitField('Submit')
