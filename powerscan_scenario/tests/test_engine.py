# This file is a part of the powerscan_scenario project
#
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from unittest import TestCase
from ..db import DBManager
from ..engine import Engine, Process
from ..scannerbase import TestingScannerBase
from .common import drop_and_create_db_if_exist
from ..common import ACTION_MENU, ACTION_SCAN, ACTION_STOP, BUTTON_MIDDLE
from .scenario import OneScenario
from time import sleep
import threading


class TestEngine(TestCase):

    def test_run_and_close(self):
        url = 'postgresql+psycopg2:///powerscan_scenario'
        config = {'sqlalchemy_url': url, 'allow_dev': True}
        scenario = OneScenario(config)
        scenarios = {'test': scenario}
        drop_and_create_db_if_exist(url)
        dbmanager = DBManager(configuration=config, scenarios=scenarios)
        base = TestingScannerBase()
        engine = Engine(config, base, dbmanager)
        thread = threading.Thread(target=engine.start)
        thread.start()
        sleep(0.1)
        engine.stop()
        thread.join()

    def test_one_scenario(self):
        url = 'postgresql+psycopg2:///powerscan_scenario'
        scanner_code = 1000
        config = {'sqlalchemy_url': url, 'allow_dev': True}
        scenario = OneScenario(config)
        scenarios = {'test': scenario}
        drop_and_create_db_if_exist(url)
        dbmanager = DBManager(
            configuration=config, scenarios=scenarios,
            isolation_level="READ UNCOMMITTED")  # only unittest
        session = dbmanager.session
        base = TestingScannerBase()
        engine = Engine(config, base, dbmanager)
        thread = threading.Thread(target=engine.start)
        thread.start()

        base.sent_from_base(scanner_code, '')
        self.assertEqual(
            base.sent_to(scanner_code),
            {
                'action_type': ACTION_MENU,
                'buttons': {},
                'counter': 0,
                'display': ['One Scenario', Process._reload],
                'sound': 'goodread',
            })

        base.sent_from_base(scanner_code, BUTTON_MIDDLE)
        self.assertEqual(
            base.sent_to(scanner_code),
            {
                'action_type': ACTION_SCAN,
                'buttons': {},
                'counter': 0,
                'display': ['Scan a product'],
                'sound': 'goodread',
            })

        sleep(0.01)
        main_query = session.query(scenario.TestProduct)
        query_p1 = main_query.filter_by(scan='product1')
        query_p2 = main_query.filter_by(scan='product2')
        query_p3 = main_query.filter_by(scan='product3')
        self.assertEqual(query_p1.count(), 0)
        self.assertEqual(query_p2.count(), 0)
        self.assertEqual(query_p3.count(), 0)

        base.sent_from_base(scanner_code, 'product1')
        self.assertEqual(
            base.sent_to(scanner_code),
            {
                'action_type': ACTION_SCAN,
                'buttons': {},
                'counter': 0,
                'display': ['Scan a product'],
                'sound': 'goodread',
            })

        sleep(0.01)
        self.assertEqual(query_p1.count(), 1)
        self.assertEqual(query_p1.one().qty, 1)
        self.assertEqual(query_p2.count(), 0)
        self.assertEqual(query_p3.count(), 0)

        base.sent_from_base(scanner_code, 'product2')
        self.assertEqual(
            base.sent_to(scanner_code),
            {
                'action_type': ACTION_SCAN,
                'buttons': {},
                'counter': 0,
                'display': ['Scan a product'],
                'sound': 'goodread',
            })

        sleep(0.01)
        self.assertEqual(query_p1.count(), 1)
        self.assertEqual(query_p1.one().qty, 1)
        self.assertEqual(query_p2.count(), 1)
        self.assertEqual(query_p2.one().qty, 1)
        self.assertEqual(query_p3.count(), 0)

        base.sent_from_base(scanner_code, 'product3')
        self.assertEqual(
            base.sent_to(scanner_code),
            {
                'action_type': ACTION_SCAN,
                'buttons': {},
                'counter': 0,
                'display': ['Scan a product'],
                'sound': 'goodread',
            })

        sleep(0.01)
        self.assertEqual(query_p1.count(), 1)
        self.assertEqual(query_p1.one().qty, 1)
        self.assertEqual(query_p2.count(), 1)
        self.assertEqual(query_p2.one().qty, 1)
        self.assertEqual(query_p3.count(), 1)
        self.assertEqual(query_p3.one().qty, 1)

        base.sent_from_base(scanner_code, 'product2')
        self.assertEqual(
            base.sent_to(scanner_code),
            {
                'action_type': ACTION_SCAN,
                'buttons': {},
                'counter': 0,
                'display': ['Scan a product'],
                'sound': 'goodread',
            })

        sleep(0.01)
        self.assertEqual(query_p1.count(), 1)
        self.assertEqual(query_p1.one().qty, 1)
        self.assertEqual(query_p2.count(), 1)
        self.assertEqual(query_p2.one().qty, 2)
        self.assertEqual(query_p3.count(), 1)
        self.assertEqual(query_p3.one().qty, 1)

        base.sent_from_base(scanner_code, 'product3')
        self.assertEqual(
            base.sent_to(scanner_code),
            {
                'action_type': ACTION_SCAN,
                'buttons': {},
                'counter': 0,
                'display': ['Scan a product'],
                'sound': 'goodread',
            })

        sleep(0.01)
        self.assertEqual(query_p1.count(), 1)
        self.assertEqual(query_p1.one().qty, 1)
        self.assertEqual(query_p2.count(), 1)
        self.assertEqual(query_p2.one().qty, 2)
        self.assertEqual(query_p3.count(), 1)
        self.assertEqual(query_p3.one().qty, 2)

        base.sent_from_base(scanner_code, 'product3')
        self.assertEqual(
            base.sent_to(scanner_code),
            {
                'action_type': ACTION_SCAN,
                'buttons': {},
                'counter': 0,
                'display': ['Scan a product'],
                'sound': 'goodread',
            })

        sleep(0.01)
        self.assertEqual(query_p1.count(), 1)
        self.assertEqual(query_p1.one().qty, 1)
        self.assertEqual(query_p2.count(), 1)
        self.assertEqual(query_p2.one().qty, 2)
        self.assertEqual(query_p3.count(), 1)
        self.assertEqual(query_p3.one().qty, 3)
        self.assertEqual(main_query.count(), 3)

        base.sent_from_base(scanner_code, scenario.scan_stop)
        self.assertEqual(
            base.sent_to(scanner_code),
            {
                'action_type': ACTION_STOP,
                'buttons': {},
                'counter': 0,
                'display': [],
                'sound': 'goodread',
            })

        # TODO test release job

        base.sent_from_base(scanner_code, BUTTON_MIDDLE)
        self.assertEqual(
            base.sent_to(scanner_code),
            {
                'action_type': ACTION_MENU,
                'buttons': {},
                'counter': 0,
                'display': ['One Scenario', Process._reload],
                'sound': 'goodread',
            })

        engine.stop()
        thread.join()
        dbmanager.close()
