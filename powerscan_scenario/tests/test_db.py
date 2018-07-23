# This file is a part of the powerscan_scenario project
#
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from unittest import TestCase
from ..db import DBManager, DBManagerException
from .scenario import OneScenario
from contextlib import contextmanager
from sqlalchemy.exc import IntegrityError
from .common import drop_and_create_db_if_exist


@contextmanager
def dbmanager(**kwargs):
    db = DBManager(**kwargs)
    try:
        yield db
    finally:
        db.close()


class TestDBManager(TestCase):

    def test_create_tables(self):
        url = 'postgresql+psycopg2:///powerscan_scenario'
        config = {'sqlalchemy_url': url}
        drop_and_create_db_if_exist(url)
        with dbmanager(configuration=config) as db:
            db.session.query(db.Scenario).count()  # table exist

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
        drop_and_create_db_if_exist(url)
        with dbmanager(configuration=config, scenarios=scenarios) as db:
            db.session.query(db.Scenario).count()  # table exist

        self.assertFalse(hasattr(scenario, 'TestProduct'))

    def test_create_tables_with_dev_scenario_with_allow_dev(self):
        url = 'postgresql+psycopg2:///powerscan_scenario'
        config = {'sqlalchemy_url': url, 'allow_dev': True}
        scenario = OneScenario(config)
        scenarios = {'test': scenario}
        drop_and_create_db_if_exist(url)
        with dbmanager(configuration=config, scenarios=scenarios) as db:
            db.session.query(db.Scenario).count()  # table exist
            self.assertTrue(hasattr(scenario, 'TestProduct'))
            db.session.query(scenario.TestProduct).count()  # table exist

    def test_update_all_scenarios(self):
        url = 'postgresql+psycopg2:///powerscan_scenario'
        config = {'sqlalchemy_url': url}
        drop_and_create_db_if_exist(url)
        with dbmanager(configuration=config) as db:
            session = db.session
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
        drop_and_create_db_if_exist(url)
        with dbmanager(configuration=config) as db:
            session = db.session
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
        drop_and_create_db_if_exist(url)
        with dbmanager(configuration=config, scenarios=scenarios) as db:
            scenario = db.session.query(db.Scenario).get('test')
            self.assertEqual(scenario.version, '1.0.0')
            scenario.version = '0.1.0'
            db.session.flush()
            db.update_all_scenarios()
            self.assertEqual(scenario.version, '1.0.0')

    def test_update_all_scenarios_delete_step(self):
        url = 'postgresql+psycopg2:///powerscan_scenario'
        config = {'sqlalchemy_url': url}
        scenario = OneScenario(config)
        scenarios = {'test': scenario}
        drop_and_create_db_if_exist(url)
        with dbmanager(configuration=config, scenarios=scenarios) as db:
            session = db.session
            session.add(db.Step(name='test_step', scenario='test',
                                method_name_on_scenario='test'))
            session.flush()
            self.assertTrue(
                session.query(db.Step).filter_by(name='test_step').count())
            db.update_all_scenarios()
            self.assertFalse(
                session.query(db.Step).filter_by(name='test_step').count())

    def test_update_all_scenarios_delete_transition(self):
        url = 'postgresql+psycopg2:///powerscan_scenario'
        config = {'sqlalchemy_url': url}
        scenario = OneScenario(config)
        scenarios = {'test': scenario}
        drop_and_create_db_if_exist(url)
        with dbmanager(configuration=config, scenarios=scenarios) as db:
            session = db.session
            session.add(db.Transition(name='test_transition', scenario='test',
                                      from_step='stop', to_step='stop',
                                      sequence=1,
                                      method_name_on_scenario='test'))
            session.flush()
            self.assertTrue(session.query(db.Transition).filter_by(
                name='test_transition').count())
            db.update_all_scenarios()
            self.assertFalse(session.query(db.Transition).filter_by(
                name='test_transition').count())
