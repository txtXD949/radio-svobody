from itsdangerous import URLSafeTimedSerializer
from flask import current_app
from flask_mail import Message
from utils.mail_init import mail


def generate_conf_token(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt='email-confirm')


def conf_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt='email-confirm',
            max_age=expiration
        )
    except:
        return None
    return email


def send_conf_email(user_email, username):
    token = generate_conf_token(user_email)
    conf_url = f'http://127.0.0.1:5000/confirm/{token}'  # TODO: потом свой домен вписать

    html = f"""
    <h2>Добро пожаловать в RadioSvobodi, {username}!</h2>
    <p>Для подтверждения email перейдите по ссылке:</p>
    <a href="{conf_url}">{conf_url}</a>
    <p>Ссылка действительна 1 час.</p>
    """
    msg = Message(
        'Подтверждение email',
        recipients=[user_email],
        html=html
    )
    mail.send(msg)
