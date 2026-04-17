import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Track(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'tracks'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    genre_id = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey('genres.id'), nullable=False)
    subgenres = sqlalchemy.Column(sqlalchemy.String)  # через запятую названия под жарнов (без пробелаов)
    file_path = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    users_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    likes_count = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    views_count = sqlalchemy.Column(sqlalchemy.Integer, default=0)  # прослушивания трека
    intop_count = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    created_at = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now())

    collaborations = sqlalchemy.Column(sqlalchemy.String, default='')  # через запятую id пользователей (без пробелаов)

    genre = orm.relationship('Genre')
    user = orm.relationship('User')
