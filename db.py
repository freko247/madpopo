# -*- coding:utf-8 -*-
import sqlalchemy
from sqlalchemy.orm import scoped_session, sessionmaker
import sqlalchemy.engine.url as url

import config

session = scoped_session(sessionmaker())


def init_db():
    engine_url = url.URL(
        drivername=config.SQL_DRIVER,
        host=config.SQL_HOST,
        username=config.SQL_USER,
        password=config.SQL_PASSWORD,
        database=config.SQL_DBNAME,
        query={'charset': 'utf8'}
    )
    engine = sqlalchemy.create_engine(engine_url, encoding='utf-8')
    session.remove()
    session.configure(bind=engine, autoflush=False, expire_on_commit=False)
    return engine
