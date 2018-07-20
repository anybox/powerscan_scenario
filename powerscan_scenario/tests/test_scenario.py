# This file is a part of the powerscan_scenario project
#
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from unittest import TestCase
from ..scenario import get_scenarios_from_entry_points, ScenarioException
from ..db import DBManager
from .common import drop_and_create_db_if_exist
from .scenario import EmptyScenario
from ..decorator import transition, DecoratorException


class TestLoadScenario(TestCase):

    def test_get_scenarios_from_entry_points(self):
        scenarios = get_scenarios_from_entry_points({})
        self.assertIn('test', scenarios)

    def test_load_empty_scenario(self):
        url = 'postgresql+psycopg2:///powerscan_scenario'
        config = {'sqlalchemy_url': url}
        scenario = EmptyScenario(config)
        scenarios = {'test': scenario}
        drop_and_create_db_if_exist(url)
        with self.assertRaises(ScenarioException):
            DBManager(configuration=config, scenarios=scenarios)

    def test_load_empty_decorator_transition(self):
        with self.assertRaises(DecoratorException):

            class WrongTransaction(EmptyScenario):

                @transition()
                def empty_decorator(self, *a):
                    return True
