import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Playlist(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'playlists'

    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True)
    tracks_id = sqlalchemy.Column(sqlalchemy.String)  # через запятую названия под жарнов (без пробелаов)
