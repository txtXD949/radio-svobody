from itsdangerous import URLSafeTimedSerializer
from flask import current_app
from flask_mail import Message
from utils.mail_init import mail


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
    token = generate_conf_token(user_email)
    conf_url = f'http://127.0.0.1:5000/confirm/{token}'  # TODO: потом свой домен вписать

    # HTML-тело письма
    html = f"""
    <h2>Добро пожаловать в RadioSvobodi, {username}!</h2>
    <p>Для подтверждения email перейдите по ссылке:</p>
    <a href="{conf_url}">{conf_url}</a>
    <p>Ссылка действительна 1 час.</p>
    """
    msg = Message(
        'Подтверждение email',  # Тема письма
        recipients=[user_email],       # Кому отправляем
        html=html                      # Содержимое
    )
    mail.send(msg)  # Отправка через настроенный SMTP
