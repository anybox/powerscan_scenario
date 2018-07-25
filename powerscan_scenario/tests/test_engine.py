# This file is a part of the powerscan_scenario project
#
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from unittest import TestCase
from ..db import DBManager
from ..engine import Engine
from ..scannerbase import TestingScannerBase
from .common import drop_and_create_db_if_exist
from .scenario import OneScenario


class TestEngine(TestCase):

    def test_one_scenario(self):
        url = 'postgresql+psycopg2:///powerscan_scenario'
        config = {'sqlalchemy_url': url}
        scenario = OneScenario(config)
        scenarios = {'test': scenario}
        drop_and_create_db_if_exist(url)
        dbmanager = DBManager(configuration=config, scenarios=scenarios)
        base = TestingScannerBase()
        engine = Engine(config, base, dbmanager)
        dbmanager.close()
