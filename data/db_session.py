import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session


def global_init(db_file: str):
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception('No file')

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    print('Connecting...')

    engine = sa.create_engine(conn_str, echo=False, max_overflow=40, pool_size=20, pool_timeout=60)
    __factory = orm.sessionmaker(bind=engine)

    from . import __all_models

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()


SqlAlchemyBase = orm.declarative_base()

__factory = None
