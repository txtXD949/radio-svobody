import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class PlaylistTrack(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'playlist_tracks'

    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True)
    playlist_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('playlists.id'))
    track_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('tracks.id'))
    order = sqlalchemy.Column(sqlalchemy.Integer, default=0)

    playlist = orm.relationship('Playlist')
    track = orm.relationship('Track')
