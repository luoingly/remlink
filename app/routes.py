from flask import Blueprint, request, session, render_template, redirect

from .services import USERNAME_REGEX, PASSWORD_REGEX, PAGE_SIZE
from .services import UserService, PostService


blueprint = Blueprint('main', __name__)


@blueprint.route('/')
def index():
    viewer_user_id = session.get('user_id', None)
    page = request.args.get('page', 1)
    logined = viewer_user_id is not None

    try:
        posts = PostService.get_posts(
            viewer_user_id, None, PAGE_SIZE * (page - 1))
        return render_template(
            'index.html', posts=posts, page=page, logined=logined)
    except Exception as e:
        return render_template(
            'index.html', error=str(e), posts=[], page=page, logined=logined)


@blueprint.route('/register', methods=['GET'])
def register_get():
    if session.get('user_id'):
        return redirect('/')
    return render_template(
        'register.html', logined=False,
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
            'register.html', error=str(e), logined=False,
            username_regex=USERNAME_REGEX, password_regex=PASSWORD_REGEX)


@blueprint.route('/login', methods=['GET'])
def login_get():
    if session.get('user_id'):
        return redirect('/')
    return render_template('login.html', logined=False)


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
        return render_template('login.html', error=str(e), logined=False)


@blueprint.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect('/')


@blueprint.route('/security', methods=['GET'])
def security_get():
    if not session.get('user_id'):
        return redirect('/login')
    return render_template('security.html', logined=True,
                           password_regex=PASSWORD_REGEX)


@blueprint.route('/security', methods=['POST'])
def security_post():
    if not session.get('user_id'):
        return redirect('/login')
    user_id = session['user_id']

    old_password = request.form.get('old-password', '')
    new_password = request.form.get('new-password', '')

    try:
        UserService.change_password(user_id, old_password, new_password)
        return redirect('/')
    except Exception as e:
        return render_template('security.html', error=str(e), logined=True,
                               password_regex=PASSWORD_REGEX)


@blueprint.route('/new', methods=['GET'])
def new_get():
    if not session.get('user_id'):
        return redirect('/login')
    return render_template('new.html', logined=True)


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
        return render_template('new.html', error=str(e), logined=True)


@blueprint.route('/profile')
def profile_redirect():
    if not session.get('user_id'):
        return redirect('/login')
    return redirect(f'/profile/{session["user_id"]}')


@blueprint.route('/profile/<int:target_user_id>')
def profile(target_user_id: int):
    viewer_user_id = session.get('user_id', None)
    page = request.args.get('page', 1)
    logined = viewer_user_id is not None

    try:
        profile = UserService.get_profile(target_user_id)
        posts = PostService.get_posts(
            viewer_user_id, target_user_id, PAGE_SIZE * (page - 1))
        return render_template(
            'profile.html', profile=profile, posts=posts,
            logined=logined, is_me=viewer_user_id == target_user_id)
    except Exception as e:
        return render_template('error.html', error=str(e), logined=logined)


@blueprint.route('/settings', methods=['GET'])
def settings_get():
    if not session.get('user_id'):
        return redirect('/login')
    user_id = session['user_id']

    try:
        profile = UserService.get_profile(user_id)
        return render_template('settings.html', profile=profile, logined=True,
                               username_regex=USERNAME_REGEX)
    except Exception as e:
        return render_template('error.html', error=str(e), logined=True)


@blueprint.route('/settings', methods=['POST'])
def settings_post():
    if not session.get('user_id'):
        return redirect('/login')
    user_id = session['user_id']

    profile = UserService.get_profile(user_id)
    username = request.form.get('username', '')
    bio = request.form.get('bio', '')

    try:
        UserService.update_profile(user_id, username, bio)
        return redirect('/profile')
    except Exception as e:
        return render_template('settings.html', error=str(e), logined=True,
                               profile=profile, username_regex=USERNAME_REGEX)


@blueprint.route('/follow/<int:target_user_id>', methods=['POST'])
def follow(target_user_id: int):
    if not session.get('user_id'):
        return '', 401
    user_id = session['user_id']

    try:
        UserService.follow(user_id, target_user_id)
        return '', 204
    except Exception as e:
        return str(e), 400


@blueprint.route('/unfollow/<int:target_user_id>', methods=['POST'])
def unfollow(target_user_id: int):
    if not session.get('user_id'):
        return '', 401
    user_id = session['user_id']

    try:
        UserService.unfollow(user_id, target_user_id)
        return '', 204
    except Exception as e:
        return str(e), 400


@blueprint.route('/like/<int:post_id>', methods=['POST'])
def like(post_id: int):
    if not session.get('user_id'):
        return '', 401
    user_id = session['user_id']

    try:
        PostService.like(user_id, post_id)
        return '', 204
    except Exception as e:
        return str(e), 400


@blueprint.route('/unlike/<int:post_id>', methods=['POST'])
def unlike(post_id: int):
    if not session.get('user_id'):
        return '', 401
    user_id = session['user_id']

    try:
        PostService.unlike(user_id, post_id)
        return '', 204
    except Exception as e:
        return str(e), 400
