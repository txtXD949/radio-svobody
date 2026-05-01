import os
import random
import datetime

from data import db_session
from data.users import User
from data.tracks import Track
from data.genres import Genre
from data.dump import Dump
from data.likes import Like
from data.playlists import Playlist
from data.playlist_tracks import PlaylistTrack

# Данные для генерации
GENRES = ['рок', 'классика', 'спейс', 'народные песни', 'джаз']

TRACKS_BY_GENRE = {
    'рок': [
        ('Hey Jude - The Beatles', 'классический рок'),
        ('Солдатами не рождаются - ГрОб', 'русский рок,пост-панк'),
        ('Still Waiting - sum41', 'поп-панк,панк'),
        ('The Future Never Dies - Scorpions', 'хардкор,хеви-метал'),
        ('Forgotten - Linking Park', 'альтернативный рок,ню-метал'),
        ('Daydreaming - Radiohead', 'арт-рок,экспериментал'),
        ('Vermillion - Slipknot', 'ню-метал,альтернативный метал')
    ],
    'классика': [
        ('Вальс Шостаковича', 'симфоническая музыка,джаз'),
        ('Лунная соната', 'романтизм,симфоническая музыка'),
        ('Токката и фуга ре минор', 'органная музыка,барокко'),
        ('Вивальди - Времена года', 'барокко,концерт'),
        ('Шестая симфония Бетховена', 'классицизм'),
        ('Танец рыцарей', 'неоклассицизм,балет'),
        ('Рахманинов - Симфония до диез минор', 'романтизм,поздний романтизм')
    ],
    'народные песни': [
        ('Во поли береза стояла', 'лирическая,русская народная'),
        ('Черный ворон', 'казачья,историческая'),
        ('Калинка', 'русская народная,плясовая'),
        ('Любо браты любо', 'казачья,походная'),
        ('Ойся ты ойся', 'казачья,плясовая'),
        ('Конь', 'русская народная,романс'),
        ('Дубинушка', 'рабочая народная,эпическая')
    ],
    'джаз': [
        ('Americano - Lo Fi Hip Hop The Jazz Cafe', 'лонж,чил-хоп'),
        ('Black to Black', 'кул-джаз,блюз'),
        ('Бесконечный рассвет', 'джаз-рок,фьюжн'),
        ('Sheakeasy Swagger', 'свинг,биг-бэнд'),
        ('Lulu Swing', 'свинг,танцевальный джаз'),
        ('Mr Pinstripe Suit', 'бибоп,хард-боп')
    ],
    'спейс': [
        ('White Stork', 'эмбиент,атмосферный'),
        ('Mortal Coil', 'эмбиент,индастриал'),
        ('Still Alright', 'спейс,lo-fi'),
        ('Onyx', 'рок,психоделический рок'),
        ('Ultra Deep Field', 'эмбиент,дроун'),
        ('Home in the morning', 'чил-спейс,электроника'),
        ('The Outer Shell', 'дарк-эмбиент,саунд-дизайн')
    ]
}

USERS = [
    {'username': 'cecsv', 'email': 'ce3742@test.com', 'password': '12345678'},
    {'username': 'txtxt', 'email': 'tx214@test.com', 'password': '87654321'},
    {'username': 'mp3ii', 'email': 'mp471@test.com', 'password': '33445566'},
    {'username': 'milt', 'email': 'mi252@test.com', 'password': '4489130124'},
    {'username': 'jennaghata', 'email': 'je3518@test.com', 'password': 'fjw30-fnke'},
    {'username': 'qwar', 'email': 'qw349@test.com', 'password': 'mkm239f-23uh3dd'},
]

# Путь к папке с аудиофайлами-заглушками
AUDIO_PLACEHOLDER = 'uploads/snds/placeholder.mp3'


def create_audio_placeholder():
    """Создаёт папку и пустой аудиофайл-заглушку"""
    os.makedirs('uploads/snds', exist_ok=True)
    if not os.path.exists(AUDIO_PLACEHOLDER):
        with open(AUDIO_PLACEHOLDER, 'wb') as f:
            f.close()
        print(f'Создан файл-заглушка: {AUDIO_PLACEHOLDER}')


def generate_test_data():
    print('Начало генерации тестовых данных...')

    # Инициализация БД
    db_session.global_init('db/rs.db')
    db_sess = db_session.create_session()

    # Очистка существующих данных
    print('Очистка существующих данных...')
    db_sess.query(PlaylistTrack).delete()
    db_sess.query(Playlist).delete()
    db_sess.query(Like).delete()
    db_sess.query(Dump).delete()
    db_sess.query(Track).delete()
    db_sess.query(User).delete()
    db_sess.query(Genre).delete()
    db_sess.commit()

    # Жанры
    print('Создание жанров...')
    genre_objects = {}
    for genre_name in GENRES:
        genre = Genre(title=genre_name)
        db_sess.add(genre)
        genre_objects[genre_name] = genre
    db_sess.commit()

    # Пользователи
    print('Создание пользователей...')
    user_objects = []
    for u in USERS:
        user = User()
        user.username = u['username']
        user.email = u['email']
        user.set_password(u['password'])
        user.confirmed = True
        db_sess.add(user)
        user_objects.append(user)
    db_sess.commit()

    # Треки и добавляем в свалку
    print('Создание треков...')
    track_objects = []
    track_id_counter = 1

    for genre_name, tracks in TRACKS_BY_GENRE.items():
        genre = genre_objects[genre_name]
        for track_title, subgenres in tracks:
            user = random.choice(user_objects)

            track = Track(
                title=track_title,
                genre_id=genre.id,
                subgenres=subgenres,
                users_id=user.id,
                file_path=f'uploads/snds/track_{track_id_counter}.mp3',
                likes_count=random.randint(0, 50),
                views_count=random.randint(0, 200),
                intop_count=random.randint(0, 10),
                created_at=datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 30))
            )
            db_sess.add(track)
            db_sess.flush()  # Получаем id трека

            # Добавляем в свалку
            dump = Dump(track_id=track.id)
            db_sess.add(dump)

            track_objects.append(track)
            track_id_counter += 1

    db_sess.commit()
    print(f'Создано {len(track_objects)} треков и добавлено в свалку')

    # Лайки
    print('Создание лайков...')
    like_count = 0
    for track in track_objects:
        num_likers = random.randint(0, 5)
        if num_likers > 0 and len(user_objects) > 0:
            likers = random.sample(user_objects, min(num_likers, len(user_objects)))
            for liker in likers:
                existing = db_sess.query(Like).filter(
                    Like.track_id == track.id,
                    Like.user_id == liker.id
                ).first()
                if not existing:
                    like = Like(track_id=track.id, user_id=liker.id)
                    db_sess.add(like)
                    like_count += 1
    db_sess.commit()
    print(f'Создано {like_count} лайков')

    # Плейлисты для пользователей
    print('Создание плейлистов...')
    playlist_objects = []
    playlist_names = ['Любимое', 'В дорогу', 'Настроение', 'Избранное', 'Работаю']

    for user in user_objects:
        num_playlists = random.randint(1, 3)
        for i in range(num_playlists):
            playlist_name = random.choice(playlist_names) + f' {i + 1}'
            playlist = Playlist(
                user_id=user.id,
                title=playlist_name
            )
            db_sess.add(playlist)
            playlist_objects.append(playlist)
    db_sess.commit()
    print(f'Создано {len(playlist_objects)} плейлистов')

    # Добавление треков в плейлисты
    print('Добавление треков в плейлисты...')
    playlist_track_count = 0
    for playlist in playlist_objects:
        num_tracks = random.randint(3, 7)
        if num_tracks > 0 and len(track_objects) > 0:
            selected_tracks = random.sample(track_objects, min(num_tracks, len(track_objects)))
            for order, track in enumerate(selected_tracks):
                pt = PlaylistTrack(
                    playlist_id=playlist.id,
                    track_id=track.id,
                    order=order
                )
                db_sess.add(pt)
                playlist_track_count += 1
    db_sess.commit()
    print(f'Добавлено {playlist_track_count} треков в плейлисты')

    print('\n=== Генерация завершена ===')
    print(f'Жанров: {len(genre_objects)}')
    print(f'Пользователей: {len(user_objects)}')
    print(f'Треков: {len(track_objects)}')
    print(f'Треков в свалке: {db_sess.query(Dump).count()}')
    print(f'Лайков: {like_count}')
    print(f'Плейлистов: {len(playlist_objects)}')
    print(f'Треков в плейлистах: {playlist_track_count}')


if __name__ == '__main__':
    create_audio_placeholder()
    generate_test_data()
