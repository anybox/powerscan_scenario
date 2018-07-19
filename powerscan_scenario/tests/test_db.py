# This file is a part of the powerscan_scenario project
#
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from unittest import TestCase
from ..db import DBManager, DBManagerException
import sqlalchemy
from copy import copy
from sqlalchemy_utils.functions import database_exists, create_database, orm
from .scenario import OneScenario


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


class TestDBManager(TestCase):

    def drop_and_create_db_if_exist(self, url):
        if database_exists(url):
            drop_database(url)

        create_database(url)

    def test_create_tables(self):
        url = 'postgresql+psycopg2:///powerscan_scenario'
        config = {'sqlalchemy_url': url}
        self.drop_and_create_db_if_exist(url)
        db = DBManager(configuration=config)
        session = db.session
        session.query(db.Scenario).count()  # table exist
        session.expunge_all()
        session.close_all()
        db.engine.dispose()

    def test_create_tables_with_missing_sqlalchemy_url(self):
        with self.assertRaises(DBManagerException):
            DBManager(configuration={})

    def test_create_tables_with_missing_config(self):
        with self.assertRaises(DBManagerException):
            DBManager()

    def test_create_tables_with_dev_scenario_without_allow_dev(self):
        url = 'postgresql+psycopg2:///powerscan_scenario'
        config = {'sqlalchemy_url': url}
        scenario = OneScenario(config)
        scenarios = {'test': scenario}
        self.drop_and_create_db_if_exist(url)
        db = DBManager(configuration=config, scenarios=scenarios)
        session = db.session
        session.query(db.Scenario).count()  # table exist
        self.assertFalse(hasattr(scenario, 'TestProduct'))
        session.expunge_all()
        session.close_all()
        db.engine.dispose()

    def test_create_tables_with_dev_scenario_with_allow_dev(self):
        url = 'postgresql+psycopg2:///powerscan_scenario'
        config = {'sqlalchemy_url': url, 'allow_dev': True}
        scenario = OneScenario(config)
        scenarios = {'test': scenario}
        self.drop_and_create_db_if_exist(url)
        db = DBManager(configuration=config, scenarios=scenarios)
        session = db.session
        session.query(db.Scenario).count()  # table exist
        self.assertTrue(hasattr(scenario, 'TestProduct'))
        session.query(scenario.TestProduct).count()  # table exist
        session.expunge_all()
        session.close_all()
        db.engine.dispose()
