from flask import Blueprint, render_template, redirect, url_for, session, request

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

from password_validator import PasswordValidator
from functools import wraps

from games.domainmodel.model import Review, User
import games.authentication.services as services
from games.utilities import utilities
import games.adapters.repository as repo

authentication = Blueprint('authentication', __name__, url_prefix='/auth', static_folder='static',
                           template_folder='templates')


@authentication.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    user_name_not_unique = None

    if form.validate_on_submit():
        try:
            services.addUser(form.username.data, form.password.data, repo.repo_instance)
            return redirect(url_for('authentication.login'))
        except services.NameNotUniqueException:
            user_name_not_unique = 'Your username is already taken. Please try again.'

    return render_template('authentication/auth.html',
                           title='Register',
                           form=form,
                           usernameErrorMsg=user_name_not_unique,
                           handler_url=url_for('authentication.register')
                           )


@authentication.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    user_name_not_recognised = None
    password_does_not_match_user_name = None

    if form.validate_on_submit():
        try:
            user = services.getUser(form.username.data, repo.repo_instance)
            services.authUser(user['user_name'], form.password.data, repo.repo_instance)
            session.clear()
            session['username'] = user['user_name']
            return redirect(url_for('home.home_home'))

        except services.UnknownUserException:
            user_name_not_recognised = 'Invalid Username! Please try again.'

        except services.AuthenticationException:
            password_does_not_match_user_name = 'Invalid Password! Please try again.'

    return render_template('authentication/auth.html',
                           title='Login',
                           form=form,
                           usernameErrorMsg=user_name_not_recognised,
                           passwordErrorMsg=password_does_not_match_user_name,
                           )


@authentication.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home.home_home'))


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if 'username' not in session:
            return redirect(url_for('authentication.login'))
        return view(**kwargs)

    return wrapped_view


class PasswordValid:
    def __init__(self, message=None):
        if not message:
            message = "Password must be at least 8 characters long, contain an uppercase, lowercase, digit and special character"
        self.message = message

    def __call__(self, form, field):
        schema = PasswordValidator()
        schema \
            .min(8) \
            .has().uppercase() \
            .has().lowercase() \
            .has().digits()
        if not schema.validate(field.data):
            raise ValidationError(self.message)


class RegistrationForm(FlaskForm):
    username = StringField('Username', [
        DataRequired(message='Your username is required!'),
        Length(min=3, message='Your username is too short!')])
    password = PasswordField('Password', [
        DataRequired(message='Your password is required!'),
        PasswordValid()])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField('Username', [
        DataRequired()])
    password = PasswordField('Password', [
        DataRequired()])
    submit = SubmitField('Login')
