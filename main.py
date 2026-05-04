from flask import Flask, jsonify, redirect, render_template, send_from_directory, request
from flask_restful import Api, abort
from werkzeug.exceptions import HTTPException
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from sqlalchemy import func
from sqlalchemy.orm import joinedload

from dotenv import load_dotenv
import os
from random import choice
import time
from werkzeug.utils import secure_filename
from re import fullmatch, IGNORECASE

from data import db_session
from data.users import User
from data.tracks import Track
from data.dump import Dump
from data.genres import Genre
from data.playlists import Playlist
from resources import (
    TrackResource, TrackListResource, TrackLikeResource,
    UserResource, UserListResource,
    GenreResource, GenreListResource,
    StatsResource,
    ApiKeyResource, ApiKeyDetailResource,
    PlaylistTracksResource, PlaylistTrackResource,
    PlaylistListResource, PlaylistResource
)
from utils.forms import LoginForm, RegisterForm, TrackForm, PlaylistForm
from utils.mail_utils import send_conf_email, conf_token
from utils.mail_init import mail
from utils.scheduler import start_scheduler

load_dotenv()

app = Flask(__name__)
api = Api(app)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
APIKEY = os.getenv('ADMIN_API_KEY')

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
api.add_resource(PlaylistListResource, '/api/playlists')
api.add_resource(PlaylistResource, '/api/playlists/<int:playlist_id>')
api.add_resource(PlaylistTracksResource, '/api/playlists/<int:playlist_id>/tracks')
api.add_resource(PlaylistTrackResource, '/api/playlists/<int:playlist_id>/tracks/<int:track_id>')

# почта
app.config['MAIL_SERVER'] = 'smtp.yandex.ru'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = 'rezistorka@ya.ru'
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = 'rezistorka@ya.ru'

mail.init_app(app)

# вход
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@app.errorhandler(HTTPException)
def handle_http_exception(e):
    """Перехватывает все HTTP-ошибки и возвращает JSON с описанием ошибки и кодом статуса"""
    return jsonify({
        'error': e.description if hasattr(e, 'description') else str(e),
        'status_code': e.code
    }), e.code


@login_manager.user_loader
def load_user(user_id):
    """Подгрузка профиля"""
    with db_session.create_session() as db_sess:
        return db_sess.get(User, user_id)


# обработчики
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Вход"""
    form = LoginForm()
    if form.validate_on_submit():
        with db_session.create_session() as db_sess:
            user = db_sess.query(User).filter(User.email == form.email.data).first()  # ищем пользователя
            if user and user.check_password(form.password.data):  # проверяем пароль
                login_user(user, remember=form.remember_me.data)
                return redirect('/')
        return render_template(
            'login.html',
            message='Неверный логин или пароль',
            form=form, title='Авторизация'
        )

    return render_template(
        'login.html',
        form=form,
        title='Авторизация'
    )


@app.route('/logout')
@login_required
def logout():
    """Выход из аккаунта"""
    logout_user()
    return redirect('/')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Регистрация"""
    form = RegisterForm()
    if form.validate_on_submit():
        # валидация пароля
        if form.password.data != form.repeat_password.data:
            return render_template(
                'register.html',
                message='Пароли не совпадают',
                form=form,
                title='Регистрация'
            )

        if len(form.password.data) < 8:
            return render_template(
                'register.html',
                message='Пароль должен быть минимум 8 символов',
                form=form,
                title='Регистрация'
            )

        with db_session.create_session() as db_sess:
            # проверка уникальности email
            if db_sess.query(User).filter(User.email == form.email.data).first():
                return render_template(
                    'register.html',
                    message='Этот email занят',
                    form=form,
                    title='Регистрация'
                )

            # создание пользователя
            user = User()
            user.username = form.username.data
            user.email = form.email.data
            user.set_password(form.password.data)

            db_sess.add(user)
            db_sess.commit()

            # сохраняем id и данные до закрытия сессии
            user_id = user.id
            user_email = user.email
            user_username = user.username

        # отправка письма с подтверждением (используем сохранённые данные)
        send_conf_email(user_email, user_username)

        # загружаем пользователя заново через user_loader
        login_user(load_user(user_id))  # авторизация
        return redirect('/confirm_wait')
    return render_template('register.html', form=form, title='Регистрация')


@app.route('/confirm/<token>')
def confirm_token(token):
    """Подтверждение email по ссылке из письма"""
    email = conf_token(token)  # расшифровка токена
    if not email:
        return render_template('message.html', message='Ссылка недействительна или истекла')

    with db_session.create_session() as db_sess:
        user = db_sess.query(User).filter(User.email == email).first()
        if user.confirmed:
            return render_template('message.html', message='Email уже подтверждён')
        user.confirmed = True  # активация аккаунта
        db_sess.commit()

    return render_template('message.html', message='Email подтверждён! Спасибо.')


@app.route('/confirm_wait')
def confirm_wait():
    """Ожидание подтверждения"""
    return render_template('confirm_wait.html', title='Подтверждение email')


@app.route('/')
def index():
    """Главная страница"""
    with db_session.create_session() as db_sess:
        # топ 5 треков по лайкам
        top_tracks = db_sess.query(Track).options(joinedload(Track.user)).order_by(Track.likes_count.desc()).limit(
            5).all()

        # топ 5 исполнителей по сумме лайков их треков
        top_artists = db_sess.query(User, func.sum(Track.likes_count).label('total_likes')
                                    ).join(Track, User.id == Track.users_id).group_by(User.id).order_by(
            func.sum(Track.likes_count).desc()).limit(5).all()

    return render_template(
        'index.html',
        top_tracks=top_tracks,
        top_artists=top_artists,
        title='REZISTORKA',
        api_key=APIKEY
    )


@app.route('/dump')
@login_required
def dump():
    """Свалка"""
    with db_session.create_session() as db_sess:  # заглушка (берем первый трек)
        dump_track = db_sess.query(Track).join(Dump, Track.id == Dump.track_id).first()
    return render_template('dump.html', track=dump_track, title='Свалка', api_key=APIKEY)


@app.route('/api/dump/random')
def api_dump_random():
    """Возвращает случайный трек их свалки"""
    with db_session.create_session() as db_sess:
        dump_tracks = db_sess.query(Track).join(Dump, Track.id == Dump.track_id).all()  # получаем все треки
        print(f"Найдено треков в свалке: {len(dump_tracks)}")
        if not dump_tracks:
            return jsonify({'track': None})
        random_track = choice(dump_tracks)  # случайный трек
        return jsonify({
            'track': {
                'id': random_track.id,
                'likes_count': random_track.likes_count
            }
        })


@app.route('/editor')
@login_required
def editor():
    """Страница c аудиоредактором AudioMass"""
    return render_template('editor.html', title='Создать трек', api_key=APIKEY)


@app.route('/upload-track', methods=['GET', 'POST'])
@login_required
def update_track():
    """Загрузка нового трека"""
    form = TrackForm()

    with db_session.create_session() as db_sess:  # получаем жанры для выпадающего списка
        genres = db_sess.query(Genre).all()
        form.genre_id.choices = [(g.id, g.title) for g in genres]

    if form.validate_on_submit():
        audio = form.audio_file.data

        extens = r'mp3|ogg|wav'  # проверка расширений
        if not fullmatch(fr'.+\.({extens})', audio.filename, IGNORECASE):
            abort(400, message='Неподдерживаемый формат файла')

        filename = secure_filename(f'{current_user.id}_{int(time.time())}.mp3')  # даем файлу уникальное имя и сохраняем
        filepath = f'uploads/snds/{filename}'
        audio.save(filepath)

        with db_session.create_session() as db_sess:
            # создание трека
            track = Track(
                title=form.title.data,
                file_path=filepath,
                users_id=current_user.id,
                genre_id=form.genre_id.data,
                subgenres=form.subgenres.data
            )
            db_sess.add(track)
            db_sess.commit()

            # отправляем трек в свалку
            dump = Dump(track_id=track.id)
            db_sess.add(dump)
            db_sess.commit()

        return redirect('/dump')

    return render_template('upload.html', form=form, title='Загрузить трек', api_key=APIKEY)


@app.route('/about')
def about():
    """Страница <<О нас>>"""
    return render_template('about.html', title='О нас', api_key=APIKEY)


@app.route('/api/tracks/<int:track_id>/stream')
def stream_tracks(track_id):
    """Отдает файл для воспроизведения"""
    with db_session.create_session() as db_sess:
        track = db_sess.get(Track, track_id)
        if not track:
            return '', 404

        track.views_count = (track.views_count or 0) + 1  # добавляем прослушивание
        db_sess.commit()

        file_path = track.file_path

    return send_from_directory(os.path.dirname(file_path), os.path.basename(file_path))  # отправляем файл


@app.route('/search')
def search():
    """Поиск по категориям: треки, пользователи, жанры, поджанры"""
    query = request.args.get('q', '').strip()  # получаем запрос
    if not query:
        return redirect('/')

    with db_session.create_session() as db_sess:
        # поиск по названию трека
        tracks = db_sess.query(Track).options(joinedload(Track.user)).filter(
            Track.title.ilike(f'%{query}%')
        ).order_by(Track.likes_count.desc()).all()

        # поиск по пользователям
        artists = db_sess.query(
            User, func.coalesce(func.sum(Track.likes_count), 0).label('total_likes')
        ).outerjoin(Track, User.id == Track.users_id).filter(
            User.username.ilike(f'%{query}%')
        ).group_by(User.id).order_by(func.sum(Track.likes_count).desc()).all()

        # поиск по жанрам
        genres = db_sess.query(Genre).filter(Genre.title.ilike(f'%{query}%')).all()

        # поиск по поджанрам
        subgenres = set()
        all_tracks = db_sess.query(Track).all()
        for track in all_tracks:
            if track.subgenres:
                for sg in track.subgenres.split(','):
                    if query.lower() in sg.lower():
                        subgenres.add(sg.strip())
        subgenres = sorted(subgenres)

    return render_template(
        'search.html',
        query=query,
        tracks=tracks,
        artists=artists,
        genres=genres,
        subgenres=subgenres,
        title=f'Поиск: {query}',
        api_key=APIKEY
    )


@app.route('/genre/<int:genre_id>')
def genre_page(genre_id):
    """Страница с треками данного жанра"""
    with db_session.create_session() as db_sess:
        genre = db_sess.query(Genre).get(genre_id)
        if not genre:
            abort(404)

        # берем треки данного жанра и сортируем по лайкам
        tracks = db_sess.query(Track).options(joinedload(Track.user)).filter(
            Track.genre_id == genre_id
        ).order_by(Track.likes_count.desc()).all()

    return render_template(
        'genre_result.html',
        genre=genre,
        tracks=tracks,
        title=f'Жанр: {genre.title}',
        api_key=APIKEY
    )


@app.route('/subgenre/<string:subgenre_name>')
def subgenre_page(subgenre_name):
    """Страница с треками данного поджанра"""
    with db_session.create_session() as db_sess:
        # берем треки данного поджанра и сортируем по лайкам
        tracks = db_sess.query(Track).options(joinedload(Track.user)).filter(
            Track.subgenres.ilike(f'%{subgenre_name}%')
        ).order_by(Track.likes_count.desc()).all()

    return render_template(
        'subgenre_result.html',
        subgenre_name=subgenre_name,
        tracks=tracks,
        title=f'Поджанр: {subgenre_name}',
        api_key=APIKEY
    )


@app.route('/profile')
@login_required
def profile():
    user_id = current_user.id

    with db_session.create_session() as db_sess:
        artist_name = db_sess.query(User).get(user_id).username
        tracks = db_sess.query(Track).filter(Track.users_id == user_id).all()
        playlists = db_sess.query(Playlist).filter(Playlist.user_id == user_id).all()

        tracks_count = len(tracks)

        steps = min(6, tracks_count)

        intop_total = 0
        likes_count = 0
        views_count = 0
        if tracks:
            intop_total = db_sess.query(func.sum(Track.intop_count)).filter(Track.users_id == user_id).scalar()
            likes_count = db_sess.query(func.sum(Track.likes_count)).filter(Track.users_id == user_id).scalar()
            views_count = db_sess.query(func.sum(Track.views_count)).filter(Track.users_id == user_id).scalar()

        return render_template(
            'profile.html',
            artist_name=artist_name,
            title=artist_name,
            tracks=tracks,
            steps=steps,
            tracks_count=tracks_count,
            likes_count=likes_count,
            views_count=views_count,
            playlists=playlists,
            intop_total=intop_total,
            api_key=os.getenv('ADMIN_API_KEY')
        )


@app.route('/profile/<int:user_id>')
@login_required
def profile_view(user_id):
    with db_session.create_session() as db_sess:
        artist_name = db_sess.query(User).get(user_id).username
        tracks = db_sess.query(Track).filter(Track.users_id == user_id).all()
        playlists = db_sess.query(Playlist).filter(Playlist.user_id == user_id).all()

        tracks_count = len(tracks)

        steps = min(6, tracks_count)

        intop_total = 0
        likes_count = 0
        views_count = 0
        if tracks:
            intop_total = db_sess.query(func.sum(Track.intop_count)).filter(Track.users_id == user_id).scalar()
            likes_count = db_sess.query(func.sum(Track.likes_count)).filter(Track.users_id == user_id).scalar()
            views_count = db_sess.query(func.sum(Track.views_count)).filter(Track.users_id == user_id).scalar()

        return render_template(
            'profile_view.html',
            artist_name=artist_name,
            title=artist_name,
            tracks=tracks,
            steps=steps,
            tracks_count=tracks_count,
            likes_count=likes_count,
            views_count=views_count,
            playlists=playlists,
            intop_total=intop_total,
            api_key=os.getenv('ADMIN_API_KEY')
        )


@app.route('/tracks/<int:user_id>')
@login_required
def tracks_page(user_id):
    with db_session.create_session() as db_sess:
        tracks = db_sess.query(Track).filter(Track.users_id == user_id).all()

        return render_template(
            "tracks.html",
            tracks=tracks,
            api_key=os.getenv('ADMIN_API_KEY')
        )


@app.route('/settings')
@login_required
def settings():
    with db_session.create_session() as db_sess:
        return render_template(
            "settings.html",
            api_key=os.getenv('ADMIN_API_KEY')
        )


@app.route('/playlists')
@login_required
def playlists():
    """Страница с плейлистами"""
    return render_template('playlists.html', title='Мои плейлисты', api_key=APIKEY)


@app.route('/playlists/create', methods=['GET', 'POST'])
@login_required
def create_playlist():
    form = PlaylistForm()

    if form.validate_on_submit():
        with db_session.create_session() as db_sess:
            # создание плейлиста
            playlist = Playlist(
                user_id=current_user.id,
                title=form.title.data
            )
            db_sess.add(playlist)
            db_sess.commit()
        return redirect('/playlists')

    return render_template(
        'create_playlist.html',
        title='Новый плейлист',
        form=form,
        api_key=APIKEY
    )


@app.route('/playlist/<int:playlist_id>')
@login_required
def playlist_page(playlist_id):
    """Страница плейлиста"""
    with db_session.create_session() as db_sess:  # ищем плейлист
        playlist = db_sess.query(Playlist).filter(
            Playlist.id == playlist_id,
            Playlist.user_id == current_user.id  # проверка владельца
        ).first()
        if not playlist:
            abort(404)
        playlist_title = playlist.title

    return render_template(
        'playlist_detail.html',
        playlist_id=playlist_id,
        playlist_title=playlist_title,
        title=playlist_title,
        api_key=APIKEY
    )


if __name__ == '__main__':
    if "db" not in os.listdir():
        os.mkdir("db")

    db_session.global_init('db/rs.db')  # инициализируем бд
    start_scheduler()  # запуск планировщика для обновления Track.intop-count

    # создание API ключа если его нет (потом добавить в .env вручную)
    from utils.get_apikey import create_apikey
    from data.api_key import ApiKey

    with db_session.create_session() as session:
        if not session.query(ApiKey).first():  # проверка, что ключ один
            create_apikey('ADMIN')

    if "uploads" not in os.listdir():
        os.mkdir("uploads")
        os.mkdir("uploads/snds")
        os.mkdir("uploads/imgs")

    app.run(host='127.0.0.1', port=5000)  # запуск сервера
