# This file is a part of the powerscan_scenario project
#
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
import sqlalchemy
from copy import copy
from sqlalchemy_utils.functions import database_exists, create_database, orm


def drop_database(url):
    url = copy(sqlalchemy.engine.url.make_url(url))
    url.database = 'postgres'
    engine = sqlalchemy.create_engine(url)
    text = 'DROP DATABASE {0}'.format(orm.quote(engine, 'powerscan_scenario'))
    cnx = engine.connect()
    cnx.execute("ROLLBACK")
    cnx.execute(text)
    cnx.execute("commit")
    cnx.close()


def drop_and_create_db_if_exist(url):
    if database_exists(url):
        drop_database(url)

    create_database(url)
