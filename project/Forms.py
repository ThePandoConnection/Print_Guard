from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Regexp, ValidationError
from Models import User

class RegistrationForm(FlaskForm):
    username_new = StringField('Username', validators=[DataRequired(), Regexp('^[a-zA-Z0-9]{5,20}$',
    message='Your username must be between 5 to 20 characters. It can have letters and numbers.')])
    password_new = PasswordField('Password', validators=[DataRequired(),
                                                         EqualTo('password_confirm', message='Passwords must match.')])
    password_confirm = PasswordField('Password Confirm', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, username_new):
        user = User.query.filter_by(username=username_new.data).first()
        if user is not None:
            raise ValidationError('Username has been taken. Type a different username.')

class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Login')
