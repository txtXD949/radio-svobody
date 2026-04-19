from flask import Flask, jsonify, redirect, render_template
from flask_restful import Api
from werkzeug.exceptions import HTTPException
from flask_login import LoginManager, login_user, logout_user, login_required

from sqlalchemy import func

from dotenv import load_dotenv
import os

from data import db_session
from data.users import User
from data.tracks import Track
from data.api_key import ApiKey
from resources import (
    TrackResource, TrackListResource, TrackLikeResource,
    UserResource, UserListResource,
    GenreResource, GenreListResource,
    StatsResource,
    ApiKeyResource, ApiKeyDetailResource
)
from utils.forms import LoginForm, RegisterForm
from utils.mail_utils import send_conf_email, conf_token
from utils.mail_init import mail

load_dotenv()

app = Flask(__name__)
api = Api(app)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# ресурсы
api.add_resource(TrackListResource, '/api/tracks')
api.add_resource(TrackResource, '/api/tracks/<int:track_id>')
api.add_resource(TrackLikeResource, '/api/tracks/<int:track_id>/like')
api.add_resource(UserListResource, '/api/users')
api.add_resource(UserResource, '/api/users/<int:user_id>')
api.add_resource(GenreListResource, '/api/genres')
api.add_resource(GenreResource, '/api/genres/<int:genre_id>')
api.add_resource(StatsResource, '/api/stats')
api.add_resource(ApiKeyResource, '/api/keys')
api.add_resource(ApiKeyDetailResource, '/api/keys/<int:key_id>')

# почта
app.config['MAIL_SERVER'] = 'smtp.yandex.ru'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = 'radio.svobodi532@yandex.ru'
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = 'radio.svobodi532@yandex.ru'

mail.init_app(app)

# вход
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@app.errorhandler(HTTPException)
def handle_http_exception(e):
    return jsonify({
        'error': e.description if hasattr(e, 'description') else str(e),
        'status_code': e.code
    }), e.code


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User, user_id)


# обработчики
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/')
        return render_template('login.html', message='Неверный логин или пароль', form=form, title='Авторизация')
    return render_template('login.html', form=form, title='Авторизация')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.repeat_password.data:
            return render_template('register.html', message='Пароли не совпадают', form=form, title='Регистрация')
        if form.password.data.__len__() < 8:
            return render_template('register.html', message='Пароль должен быть минимум 8 символов', form=form,
                                   title='Регистрация')

        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', message='Этот email занят', form=form, title='Регистрация')

        user = User()
        user.username = form.username.data
        user.email = form.email.data
        user.set_password(form.password.data)

        db_sess.add(user)
        db_sess.commit()

        send_conf_email(user.email, user.username)

        login_user(user)
        return redirect('/confirm_wait')
    return render_template('register.html', form=form, title='Регистрация')


@app.route('/confirm/<token>')
def confirm_token(token):
    email = conf_token(token)
    if not email:
        return render_template('message.html', message='Ссылка недействительна или истекла')

    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.email == email).first()

    if user.confirmed:
        return render_template('message.html', message='Email уже подтверждён')

    user.confirmed = True
    db_sess.commit()

    return render_template('message.html', message='Email подтверждён! Спасибо.')


@app.route('/confirm_wait')
def confirm_wait():
    return render_template('confirm_wait.html', title='Подтверждение email')


@app.route('/')
def index():
    db_sess = db_session.create_session()

    # топ треков
    top_tracks = db_sess.query(Track).order_by(Track.likes_count.desc()).limit(5).all()

    # топ исполнителей
    top_artists = top_artists = db_sess.query(User, func.sum(Track.likes_count).label('total_likes')
                                              ).join(Track, User.id == Track.users_id).group_by(User.id).order_by(
        func.sum(Track.likes_count).desc()).limit(5).all()

    return render_template('index.html', top_tracks=top_tracks, top_artists=top_artists, title='Radio Svobodi')


if __name__ == '__main__':
    db_session.global_init('db/rs.db')

    session = db_session.create_session()
    # if not session.query(ApiKey).first():
    #     admin_key = ApiKey(
    #         key=ApiKey.generate_key(),
    #         name='Admin Key'
    #     )
    #     session.add(admin_key)
    #     session.commit()
    session.close()

    app.run(host='127.0.0.1', port=5000)
