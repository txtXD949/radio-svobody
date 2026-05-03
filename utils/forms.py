from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import EmailField, PasswordField, BooleanField, SubmitField, StringField
from wtforms.fields.choices import SelectField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    """Форма авторизации"""
    email = EmailField('Email', validators=[DataRequired(), Email(message='Введите корректный email')])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('ВОЙТИ')


class RegisterForm(FlaskForm):
    """Форма регистрации"""
    username = StringField('Имя', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email(message='Введите корректный email')])
    password = PasswordField('Пароль', validators=[DataRequired()])
    repeat_password = PasswordField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('РЕГИСТРАЦИЯ')


class TrackForm(FlaskForm):
    """Форма загрузки нового трека"""
    title = StringField('Название', validators=[DataRequired()])
    audio_file = FileField('Аудиофайл (.mp3)', validators=[
        FileRequired(),                                                         # файл обязательный
        FileAllowed(['mp3', 'wav', 'ogg'], 'Аудиофайлы MP3')  # разрешенные файлы
    ])
    genre_id = SelectField('Жанр', coerce=int, validators=[DataRequired()])  # coerce=int — преобразует в int
    subgenres = StringField('Поджанры (через запятую без пробелов)')
    submit = SubmitField('КИНУТЬ В СВАЛКУ')


class PlaylistForm(FlaskForm):
    """Форма создания плейлиста"""
    title = StringField('Название плейлиста', validators=[DataRequired()])
    submit = SubmitField('СОЗДАТЬ')
