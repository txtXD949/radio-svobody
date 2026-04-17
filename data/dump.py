import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Dump(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'dump'

    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True)
    track_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('tracks.id'))
    dumped_at = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now())

    track = orm.relationship('Track')
