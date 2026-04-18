from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, BooleanField, SubmitField, StringField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email(message='Введите корректный email')])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('ВОЙТИ')


class RegisterForm(FlaskForm):
    username = StringField('Имя', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email(message='Введите корректный email')])
    password = PasswordField('Пароль', validators=[DataRequired()])
    repeat_password = PasswordField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('РЕГИСТРАЦИЯ')
