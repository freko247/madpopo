# -*- coding:utf-8 -*-
import sqlalchemy
from sqlalchemy.orm import scoped_session, sessionmaker

import config

session = scoped_session(sessionmaker())


def init_db():
    d = {'host': config.SQL_HOST,
         'user': config.SQL_USER,
         'dbname': config.SQL_DBNAME,
         'password': config.SQL_PASSWORD,
         'driver': config.SQL_DRIVER,
         }
    connection_string = '%(driver)s://%(user)s:%(password)s@%(host)s/%(dbname)s' % d
    engine = sqlalchemy.create_engine(connection_string)
    session.remove()
    session.configure(bind=engine, autoflush=False, expire_on_commit=False)
    return engine
