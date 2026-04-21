import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Like(SqlAlchemyBase):
    __tablename__ = 'likes'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    track_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('tracks.id'))

    user = orm.relationship('User')
    track = orm.relationship('Track')
