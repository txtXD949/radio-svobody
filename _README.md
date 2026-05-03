<h1 style="color: #484AD5; text-align: center;">REZISTORKA</h1>

---

## Содержание

1. [О проекте](#1-о-проекте)
2. [Функциональные возможности](#2-функциональные-возможности)
3. [Технологии](#3-технологии)
4. [Архитектура и структура проекта](#4-архитектура-и-структура-проекта)
5. [Установка и запуск](#5-установка-и-запуск)
6. [API документация](#6-api-документация)
7. [База данных](#7-база-данных)
8. [Интерфейс](#8-интерфейс)
9. [Планы и дальнейшее развитие](#9-планы-и-дальнейшее-развитие)

---

## 1. О проекте

«REZISTORKA» — это платформа для музыкантов, где можно создавать треки онлайн. Готовую музыку можно отправить в
«свалку», где каждый трек живёт за счёт лайков сообщества, а лучшие попадают в топ недели.

Проект даёт свободу творчества без цензуры и ограничений. Здесь нет лейблов и редакторов —
только музыка и те, кто её оценивает. Подходит для независимых музыкантов, подкастеров
и всех, кто хочет поделиться своим звуком.

---

## 2. Функциональные возможности

- Регистрация и авторизация с подтверждением email
- Создание треков во встроенном аудиоредакторе AudioMass
- Загрузка готовых аудиофайлов (MP3, WAV, OGG)
- «Свалка» — случайный трек, лайки, рейтинг
- Топ треков и топ исполнителей на главной
- Фильтр треков по жанрам
- Поиск по трекам, исполнителям, жанрам и поджанрам
- Страницы жанров и поджанров со списком треков и плейлистом
- Плейлисты: создание, добавление треков, изменение порядка, удаление
- Встроенный аудиоплеер с плейлистом и переключением треков
- Смена светлой и тёмной темы
- REST API с аутентификацией по API-ключу
- Адаптивный дизайн для мобильных устройств

---

## 3. Технологии

Backend

Flask 3.1.3
Flask-RESTful 0.3.10
Flask-Login 0.6.3
Flask-WTF 1.3.0
Flask-Mail 0.10.0
SQLAlchemy 2.0.49
sqlalchemy-serializer 1.6.3
Werkzeug 3.1.8
WTForms 3.2.1
APScheduler 3.11.2
itsdangerous 2.2.0
python-dotenv 1.2.2
email-validator 2.3.0
requests 2.33.1

Frontend
Bootstrap 5.3.0
Select2 4.1.0
jQuery 3.6.0
AudioMass
Google Fonts (Inter, Courier Prime, Bytesized)

Инструменты
Git
Figma
SQLite

---

## 4. Архитектура и структура проекта

### 4.1. Структура папок и файлов

### 4.2. Логика работы основных модулей

**Авторизация:**

- Flask-Login управляет сессиями
- `login_user()` / `logout_user()` — вход/выход
- `@login_required` защищает приватные страницы

**API:**

- Flask-RESTful обрабатывает эндпоинты
- `check_api_key()` проверяет заголовок `X-API-Key`
- Для обычных пользователей API-ключ подставляется в шаблоны

**Плеер:**

- Клиентский класс `RadioPlayer` (HTML5 Audio)
- Поддерживает плейлисты и одиночное воспроизведение
- Синхронизирует иконки воспроизведения

**База данных:**

- SQLAlchemy ORM
- Все сессии закрываются через `with` (контекстный менеджер)
- `joinedload()` для жадной загрузки связанных объектов

### 4.3. Модели базы данных

**User**

- `id`, `username`, `email`, `password` (хеш), `confirmed`, `modified_date`

**Track**

- `id`, `title`, `genre_id`, `subgenres`, `file_path`, `users_id`
- `likes_count`, `views_count`, `intop_count`, `created_at`

**Genre**

- `id`, `title`

**Dump**

- `id`, `track_id`, `dumped_at`

**Playlist**

- `id`, `user_id`, `title`, `created_at`

**PlaylistTrack** (связующая таблица)

- `id`, `playlist_id`, `track_id`, `order`

**ApiKey**

- `id`, `key`, `name`, `created_at`, `is_active`

> Ключевое поле `intop_count` обновляется раз в неделю планировщиком APScheduler.

---

## 5. Установка и запуск

### 5.1. Клонирование репозитория

```bash
git clone https://github.com/your-username/RadioSvobodi.git
cd RadioSvobodi
```

### 5.2. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 5.3. Настройка переменных окружения

### 5.4. Инициализация базы данных

База данных создаётся автоматически при первом запуске.

### 5.5. Заполнение тестовыми данными (опционально)

```bash
python test.py
```

Скрипт создаст:

- 6 тестовых пользователей
- 35 треков в разных жанрах
- Лайки, плейлисты, поджанры

### 5.7. Запуск сервера

```bash
python main.py
Сервер запустится по адресу: http://127.0.0.1:5000
```

---

## 6. API документация

> [!IMPORTANT]
> Все запросы к API требуют заголовок `X-API-Key` с валидным ключом.

### 6.1 Эндпоинты

#### Треки

| Метод  | URL                   | Описание           |
|--------|-----------------------|--------------------|
| GET    | /api/tracks           | Список всех треков |
| GET    | /api/tracks/{id}      | Получить трек      |
| POST   | /api/tracks           | Создать трек       |
| PUT    | /api/tracks/{id}      | Обновить трек      |
| DELETE | /api/tracks/{id}      | Удалить трек       |
| POST   | /api/tracks/{id}/like | Лайкнуть трек      |

> [!TIP]
> Параметр `genre_id` (целое число) — опциональный фильтр. Если указать его в GET-запросе (`/api/tracks?genre_id=1`),
> API вернёт только треки выбранного жанра.

##### POST /api/tracks - тело запроса

```
{
    "title": "Название",
    "genre_id": 1,
    "file_path": "/путь/к/файлу.mp3",
    "users_id": 1,
    "subgenres": "рок,поп",
    "collaborations": "2,3"
}
```

#### GET /api/tracks/{id} - ответ

```
{
    "track": {
        "id": 1,
        "title": "Название",
        "genre_id": 1,
        "subgenres": "рок",
        "file_path": "/путь.mp3",
        "users_id": 1,
        "likes_count": 5,
        "views_count": 10,
        "intop_count": 0,
        "created_at": "2024-01-01 12:00:00",
        "collaborations": ""
    }
}
```

### Пользователи

| Метод  | URL             | Описание              |
|--------|-----------------|-----------------------|
| GET    | /api/users      | Список пользователей  |
| GET    | /api/users/{id} | Получить пользователя |
| POST   | /api/users      | Создать пользователя  |
| DELETE | /api/users/{id} | Удалить пользователя  |

#### POST /api/users - тело запроса

```
{
    "username": "user123",
    "email": "user@example.com",
    "password": "pass123"
}
```

#### GET /api/users/{id} - ответ

```
{
    "user": {
        "id": 1,
        "username": "user123",
        "email": "user@example.com",
        "modified_date": "2024-01-01 12:00:00"
    }
}
```

### Жанры

| Метод  | URL              | Описание      |
|--------|------------------|---------------|
| GET    | /api/genres      | Список жанров |
| GET    | /api/genres/{id} | Получить жанр |
| POST   | /api/genres      | Создать жанр  |
| DELETE | /api/genres/{id} | Удалить жанр  |

#### POST /api/genres - тело запроса

```
{
    "title": "Рок"
}
```

### Статистика

| Метод | URL        | Описание         |
|-------|------------|------------------|
| GET   | /api/stats | Общая статистика |

#### GET /api/stats - ответ

```
{
"stats": {
    "total_tracks": 10,
    "total_users": 5,
    "total_likes": 25,
    "total_views": 100,
    "top_tracks": [
            {"id": 1, "title": "Песня", "views": 50}
        ]
    }
}
```

### Управление API ключами (только админ)

| Метод  | URL            | Описание            |
|--------|----------------|---------------------|
| GET    | /api/keys      | Список ключей       |
| POST   | /api/keys      | Создать ключ        |
| DELETE | /api/keys/{id} | Деактивировать ключ |

#### POST /api/keys - тело запроса

```
{
    "name": "Telegram Bot"
}
```

#### POST /api/keys - ответ

```
{
    "api_key": "сгенерированный_ключ",
    "name": "Telegram Bot",
    "message": "API key created"
}
```

### Плейлисты

| Метод  | URL                                   | Описание                       |
|--------|---------------------------------------|--------------------------------|
| GET    | /api/playlists                        | Список плейлистов пользователя |
| POST   | /api/playlists                        | Создать плейлист               |
| DELETE | /api/playlists/{id}                   | Удалить плейлист               |
| GET    | /api/playlists/{id}/tracks            | Получить треки плейлиста       |
| POST   | /api/playlists/{id}/tracks            | Добавить трек в плейлист       |
| DELETE | /api/playlists/{id}/tracks/{track_id} | Удалить трек из плейлиста      |
| PUT    | /api/playlists/{id}/tracks/{track_id} | Изменить порядок трека         |

#### POST /api/playlists - тело запроса

```bash
{
"title": "Мой плейлист"
}
```

#### POST /api/playlists/{id}/tracks - тело запроса

```bash
{
"track_id": 5
}
```

#### PUT /api/playlists/{id}/tracks/{track_id} - тело запроса

```bash
{
"direction": "up" // или "down"
}
```

> [!NOTE]
> Параметр `order` в ответе определяет позицию трека в плейлисте (начинается с 0).

### 6.2 Коды ошибок

| Код | Значение                          |
|-----|-----------------------------------|
| 200 | Успех                             |
| 201 | Создано                           |
| 400 | Неверные данные                   |
| 401 | Неверный или отсутствует API ключ |
| 403 | Недостаточно прав                 |
| 404 | Не найдено                        |
| 409 | Уже существует                    |

### 6.3 Пример запроса (curl)

#### Получить все треки

```bash
curl -X GET http://127.0.0.1:5000/api/tracks \
-H "X-API-Key: ваш_ключ"
```

#### Создать трек

```bash
curl -X POST http://127.0.0.1:5000/api/tracks \
-H "X-API-Key: ваш_ключ" \
-H "Content-Type: application/json" \
-d '{"title":"Моя песня","genre_id":1,"file_path":"/music.mp3","users_id":1}'
```

#### Поставить лайк

```bash
curl -X POST http://127.0.0.1:5000/api/tracks/1/like \
-H "X-API-Key: ваш_ключ" \
-H "Content-Type: application/json" \
-d '{"user_id": 1}'
```

#### Пример запроса (Python)

```python
import requests

headers = {"X-API-Key": "ваш_ключ"}

# Получить треки
response = requests.get("http://127.0.0.1:5000/api/tracks", headers=headers)

# Создать трек
data = {
    "title": "Моя песня",
    "genre_id": 1,
    "file_path": "/music.mp3",
    "users_id": 1
}
response = requests.post("http://127.0.0.1:5000/api/tracks",
                         json=data,
                         headers=headers)
```

---

## 7. База данных

### 7.1. Общая схема

Проект использует SQLite (в разработке) и ORM SQLAlchemy. Все модели наследуются от `SqlAlchemyBase` и
`SerializerMixin` (для удобной сериализации в JSON).

### 7.2. Таблицы и связи

Таблицы и связи:

Users (пользователи)
id (Integer, первичный ключ)
username (String, уникальный)
email (String, уникальный)
password (String, хеш пароля)
modified_date (DateTime)
confirmed (Boolean)

Tracks (треки)
id (Integer, первичный ключ)
title (String)
genre_id (Integer, внешний ключ → genres.id)
subgenres (String, поджанры через запятую)
file_path (String)
users_id (Integer, внешний ключ → users.id)
likes_count (Integer)
views_count (Integer)
intop_count (Integer)
created_at (DateTime)

Genres (жанры)
id (Integer, первичный ключ)
title (String)

Dump (свалка)
id (Integer, первичный ключ)
track_id (Integer, внешний ключ → tracks.id)
dumped_at (DateTime)

Playlists (плейлисты)
id (Integer, первичный ключ)
user_id (Integer, внешний ключ → users.id)
title (String)
created_at (DateTime)

PlaylistTracks (связь плейлистов и треков)
id (Integer, первичный ключ)
playlist_id (Integer, внешний ключ → playlists.id)
track_id (Integer, внешний ключ → tracks.id)
order (Integer, порядок трека)

Likes (лайки)
id (Integer, первичный ключ)
user_id (Integer, внешний ключ → users.id)
track_id (Integer, внешний ключ → tracks.id)

ApiKeys (API-ключи)
id (Integer, первичный ключ)
key (String, уникальный)
name (String)
created_at (DateTime)
is_active (Boolean)

Связи между таблицами:

users → tracks (один-ко-многим)
users → playlists (один-ко-многим)
users → likes (один-ко-многим)
users → api_keys (один-ко-многим)
tracks → dump (один-к-одному)
tracks → playlist_tracks (один-ко-многим)
tracks → likes (один-ко-многим)
genres → tracks (один-ко-многим)
playlists → playlist_tracks (один-ко-многим)

```

---

## 8. Интерфейс

### 8.1. Общая стилистика

### 8.2. Структура страниц

#### Главная (`/`)

#### Свалка (`/dump`)

#### Поиск (`/search`)

#### Страницы жанра и поджанра (`/genre/<id>`, `/subgenre/<name>`)

#### Плейлисты (`/playlists`)

#### Страница плейлиста (`/playlist/<id>`)

#### Загрузка трека (`/upload-track`)

#### Аудиоредактор (`/editor`)

### 8.3. Мини-плеер

### 8.4. Шторка (боковое меню)

### 8.5. Смена темы

### 8.6. Адаптив

---

## 9. Планы и дальнейшее развитие

### 9.1. Что уже реализовано

- Полноценная система аккаунтов (регистрация, вход, подтверждение email).
- Загрузка и прослушивание треков.
- Свалка (рандомный трек, лайки).
- Топ треков и исполнителей с фильтром по жанрам.
- Поиск по всем категориям (треки, исполнители, жанры, поджанры).
- Плейлисты (создание, добавление треков, порядок, удаление).
- Смена светлой/тёмной темы.
- Встроенный аудиоредактор AudioMass.
- REST API с аутентификацией по API-ключу.
- Адаптивный дизайн.

### 9.2. Что можно добавить в будущем

#### Для пользователей

#### Для контента

#### Технические улучшения

#### Интеграции

### 9.4. Идеи для «REZISTORKA»

---

## 👥 Авторы

- **cecsv** — разработка бэкенда, API, базы данных, фронтенда
- **mjvorp** — дизайн в Figma, страницы профиля и настроек

Проект выполнен в рамках проектной работы.

