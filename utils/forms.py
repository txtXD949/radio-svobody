from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import EmailField, PasswordField, BooleanField, SubmitField, StringField
from wtforms.fields.choices import SelectField
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


class TrackForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    audio_file = FileField('Аудиофайл (.mp3)', validators=[
        FileRequired(),
        FileAllowed(['mp3', 'wav', 'ogg'], 'Аудиофайлы MP3')
    ])
    genre_id = SelectField('Жанр', coerce=int, validators=[DataRequired()])
    subgenres = StringField('Поджанры (через запятую без пробелов)')
    submit = SubmitField('КИНУТЬ В СВАЛКУ')


class PlaylistForm(FlaskForm):
    title = StringField('Название плейлиста', validators=[DataRequired()])
    submit = SubmitField('СОЗДАТЬ')

