import sqlalchemy
from .db_session import SqlAlchemyBase

from sqlalchemy_serializer import SerializerMixin


class Genre(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'genres'

    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
