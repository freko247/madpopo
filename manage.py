#!/usr/bin/env python
from migrate.versioning.shell import main

import config

if __name__ == '__main__':
    d = {'host': config.SQL_HOST,
         'user': config.SQL_USER,
         'dbname': config.SQL_DBNAME,
         'password': config.SQL_PASSWORD,
         'driver': config.SQL_DRIVER,
         }
    url = '%(driver)s://%(user)s:%(password)s@%(host)s/%(dbname)s' % d
    main(url=url, repository='db_repo')
