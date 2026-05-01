from data import db_session
from data.api_key import ApiKey


def create_apikey(name):
    """Создание и получение API ключа"""
    with db_session.create_session() as session:
        admin_key = ApiKey(
            key=ApiKey.generate_key(),
            name=name
        )
        session.add(admin_key)
        session.commit()
    return admin_key