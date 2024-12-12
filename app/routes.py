from flask import Blueprint, request, session, render_template, redirect

from .services import UserService, USERNAME_REGEX, PASSWORD_REGEX


blueprint = Blueprint('main', __name__)


@blueprint.route('/')
def index():

    # temporary response
    if session.get('user_id'):
        return 'Hello, ' + session['username'] + '!'
    else:
        return 'Hello, anonymous!'


@blueprint.route('/register', methods=['GET'])
def register_get():
    if session.get('user_id'):
        return redirect('/')
    return render_template(
        'register.html',
        username_regex=USERNAME_REGEX, password_regex=PASSWORD_REGEX)


@blueprint.route('/register', methods=['POST'])
def register_post():
    if session.get('user_id'):
        return redirect('/')

    username = request.form['username']
    password = request.form['password']

    try:
        user = UserService.register(username, password)
        session.update({'user_id': user.user_id, 'username': user.username})
        return redirect('/')
    except Exception as e:
        return render_template(
            'register.html', error=str(e),
            username_regex=USERNAME_REGEX, password_regex=PASSWORD_REGEX)


@blueprint.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect('/')
