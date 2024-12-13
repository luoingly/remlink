from flask import Blueprint, request, session, render_template, redirect

from .services import USERNAME_REGEX, PASSWORD_REGEX, PAGE_SIZE
from .services import UserService, PostService


blueprint = Blueprint('main', __name__)


@blueprint.route('/')
def index():
    viewer_user_id = session.get('user_id', None)
    page = request.args.get('page', 1)

    try:
        posts = PostService.get_posts(
            viewer_user_id, None, PAGE_SIZE * (page - 1))
        return render_template('index.html', posts=posts, page=page)
    except Exception as e:
        return render_template('index.html', error=str(e), posts=[], page=page)


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


@blueprint.route('/login', methods=['GET'])
def login_get():
    if session.get('user_id'):
        return redirect('/')
    return render_template('login.html')


@blueprint.route('/login', methods=['POST'])
def login_post():
    if session.get('user_id'):
        return redirect('/')

    username = request.form.get('username', '')
    password = request.form.get('password', '')

    try:
        user = UserService.login(username, password)
        session.update({'user_id': user.user_id, 'username': user.username})
        return redirect('/')
    except Exception as e:
        return render_template('login.html', error=str(e))


@blueprint.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect('/')


@blueprint.route('/new', methods=['GET'])
def new_get():
    if not session.get('user_id'):
        return redirect('/login')
    return render_template('new.html')


@blueprint.route('/new', methods=['POST'])
def new_post():
    if not session.get('user_id'):
        return redirect('/login')
    user_id = session['user_id']

    content = request.form.get('content', '')
    privacy = request.form.get('privacy', 'public')

    try:
        PostService.create_post(user_id, content, privacy)
        return redirect('/')
    except Exception as e:
        return render_template('new.html', error=str(e))


@blueprint.route('/profile/<int:target_user_id>')
def profile(target_user_id: int):
    viewer_user_id = session.get('user_id', None)
    page = request.args.get('page', 1)

    try:
        profile = UserService.get_profile(viewer_user_id)
        posts = PostService.get_posts(
            viewer_user_id, target_user_id, PAGE_SIZE * (page - 1))
        return render_template(
            'profile.html', profile=profile, posts=posts)
    except Exception as e:
        return render_template('error.html', error=str(e))
