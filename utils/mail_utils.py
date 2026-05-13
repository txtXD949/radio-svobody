import os
import requests

from itsdangerous import URLSafeTimedSerializer
from flask import current_app


def generate_conf_token(email):
    """Создаёт подписанный токен для подтверждения email (действует 1 час по умолчанию)"""
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt='email-confirm')  # URL-safe токен


def conf_token(token, expiration=3600):
    """Проверяет токен и возвращает email, если он валиден и не истёк"""
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt='email-confirm',
            max_age=expiration  # Время жизни токена
        )
    except:
        return None  # Токен недействителен или истёк
    return email


def send_conf_email(user_email, username):
    """Отправляет письмо со ссылкой для подтверждения email"""
    token = generate_conf_token(user_email)  # генерация токена
    conf_url = f'http://rezistorka.ru/confirm/{token}'  # генерация ссылок  # для проверки rezistorka.ru замените на 127.0.0.1:80 или 127.0.0.1:5000

    api_key = os.getenv('UNISENDER_API_KEY')  # API ключ
    from_email = os.getenv('UNISENDER_FROM_EMAIL')  # адрес отправителя
    from_name = 'rezistorka'  # имя отправителя
    subject = 'Подтверждение почты'

    # HTML-тело письма
    html = f"""
    <h2>Добро пожаловать в rezistorka, {username}!</h2>
    <p>Для подтверждения email перейдите по ссылке:</p>
    <a href="{conf_url}">{conf_url}</a>
    <p>Ссылка действительна 1 час.</p>
    """

    url = 'https://goapi.unisender.ru/ru/transactional/api/v1'  # эндпоинт API Unisender для отправки email

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-API-KEY': api_key
    }

    params = {
        'message': {
            'recipients': [
                {
                    'email': user_email  # почта получателя
                }
            ],
            'body': {
                'html': html  # HTML-тело письма
            },
            'subject': subject,  # тема письма
            'from_email': from_email,  # отправитель (наша почта на домен)
            'from_name': from_name,  # имя (наш сайт)
            'track_links': 1,  # следить за ссылками
            'track_read': 1  # следить за прочтением
        }
    }

    response = requests.post(url + '/email/send.json', json=params,
                             headers=headers)  # отправка POST-запроса к API Unisender Go
    print(response.status_code, response.json())
    return response.json()
