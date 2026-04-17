import sqlalchemy
import datetime
import secrets
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class ApiKey(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'api_keys'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    key = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)  # название сервиса
    created_at = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now())
    is_active = sqlalchemy.Column(sqlalchemy.Boolean, default=True)

    @staticmethod
    def generate_key():
        return secrets.token_urlsafe(32)
