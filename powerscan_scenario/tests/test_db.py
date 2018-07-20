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
from contextlib import contextmanager
from sqlalchemy.exc import IntegrityError


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


@contextmanager
def dbmanager(**kwargs):
    db = DBManager(**kwargs)
    session = db.session
    try:
        yield db, session
    finally:
        session.rollback()
        session.expunge_all()
        session.close_all()
        db.engine.dispose()


class TestDBManager(TestCase):

    def drop_and_create_db_if_exist(self, url):
        if database_exists(url):
            drop_database(url)

        create_database(url)

    def test_create_tables(self):
        url = 'postgresql+psycopg2:///powerscan_scenario'
        config = {'sqlalchemy_url': url}
        self.drop_and_create_db_if_exist(url)
        with dbmanager(configuration=config) as (db, session):
            session.query(db.Scenario).count()  # table exist

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
        with dbmanager(configuration=config, scenarios=scenarios) as (db,
                                                                      session):
            session.query(db.Scenario).count()  # table exist

        self.assertFalse(hasattr(scenario, 'TestProduct'))

    def test_create_tables_with_dev_scenario_with_allow_dev(self):
        url = 'postgresql+psycopg2:///powerscan_scenario'
        config = {'sqlalchemy_url': url, 'allow_dev': True}
        scenario = OneScenario(config)
        scenarios = {'test': scenario}
        self.drop_and_create_db_if_exist(url)
        with dbmanager(configuration=config, scenarios=scenarios) as (db,
                                                                      session):
            session.query(db.Scenario).count()  # table exist
            self.assertTrue(hasattr(scenario, 'TestProduct'))
            session.query(scenario.TestProduct).count()  # table exist

    def test_update_all_scenarios(self):
        url = 'postgresql+psycopg2:///powerscan_scenario'
        config = {'sqlalchemy_url': url}
        self.drop_and_create_db_if_exist(url)
        with dbmanager(configuration=config) as (db, session):
            session.add(db.Scenario(name="test_scenario", label="Test",
                                    version='1.0.0', sequence=10))
            session.flush()
            session.add(db.Step(name="test_step", scenario="test_scenario",
                                method_name_on_scenario="test"))
            session.flush()
            session.add(db.Transition(name="test_transition", sequence=1,
                                      scenario="test_scenario",
                                      from_step='test_step',
                                      to_step='test_step',
                                      method_name_on_scenario="test"))
            session.flush()
            db.update_all_scenarios()
            self.assertFalse(session.query(db.Scenario).count())

    def test_update_all_scenarios_with_job(self):
        url = 'postgresql+psycopg2:///powerscan_scenario'
        config = {'sqlalchemy_url': url}
        self.drop_and_create_db_if_exist(url)
        with dbmanager(configuration=config) as (db, session):
            session.add(db.Scenario(name="test_scenario", label="Test",
                                    version='1.0.0', sequence=10))
            session.flush()
            session.add(db.Step(name="test_step", scenario="test_scenario",
                                method_name_on_scenario="test"))
            session.add(db.Job(scenario_name="test_scenario"))
            session.flush()
            session.add(db.Transition(name="test_transition", sequence=1,
                                      scenario="test_scenario",
                                      from_step='test_step',
                                      to_step='test_step',
                                      method_name_on_scenario="test"))
            session.flush()
            with self.assertRaises(IntegrityError):
                db.update_all_scenarios()

    def test_update_all_scenarios_other_version(self):
        url = 'postgresql+psycopg2:///powerscan_scenario'
        config = {'sqlalchemy_url': url}
        scenario = OneScenario(config)
        scenarios = {'test': scenario}
        self.drop_and_create_db_if_exist(url)
        with dbmanager(configuration=config, scenarios=scenarios) as (db,
                                                                      session):
            scenario = session.query(db.Scenario).get('test')
            self.assertEqual(scenario.version, '1.0.0')
            scenario.version = '0.1.0'
            session.flush()
            db.update_all_scenarios()
            self.assertEqual(scenario.version, '1.0.0')
