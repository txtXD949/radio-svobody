# RadioSvobodi API

API для музыкального сервиса.

## Запуск

```
bash
python main.py
```

При первом запуске в консоли появится ADMIN API KEY. Сохраните его.

## Аутентификация

Все запросы требуют заголовок X-API-Key с валидным ключом.

```headers = {"X-API-Key": "ваш_ключ"}```

# Эндпоинты

## Треки

| Метод  | URL                   | Описание           |
|--------|-----------------------|--------------------|
| GET    | /api/tracks           | Список всех треков |
| GET    | /api/tracks/{id}      | Получить трек      |
| POST   | /api/tracks           | Создать трек       |
| PUT    | /api/tracks/{id}      | Обновить трек      |
| DELETE | /api/tracks/{id}      | Удалить трек       |
| POST   | /api/tracks/{id}/like | Лайкнуть трек      |

#### POST /api/tracks - тело запроса

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

## Пользователи

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

## Жанры

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

## Статистика

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

## Управление API ключами (только админ)

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

## Коды ошибок

| Код | Значение                          |
|-----|-----------------------------------|
| 200 | Успех                             |
| 201 | Создано                           |
| 400 | Неверные данные                   |
| 401 | Неверный или отсутствует API ключ |
| 403 | Недостаточно прав                 |
| 404 | Не найдено                        |
| 409 | Уже существует                    |

## Пример запроса (curl)

bash

### Получить все треки

```
curl -X GET http://127.0.0.1:5000/api/tracks \
-H "X-API-Key: ваш_ключ"
```

### Создать трек

```
curl -X POST http://127.0.0.1:5000/api/tracks \
-H "X-API-Key: ваш_ключ" \
-H "Content-Type: application/json" \
-d '{"title":"Моя песня","genre_id":1,"file_path":"/music.mp3","users_id":1}'
```

### Поставить лайк

```
curl -X POST http://127.0.0.1:5000/api/tracks/1/like \
-H "X-API-Key: ваш_ключ"
```

## Пример запроса (Python)

```
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
