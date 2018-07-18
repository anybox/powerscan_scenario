# This file is a part of the powerscan_scenario project
#
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from unittest import TestCase
from ..scenario import get_scenarios_from_entry_points


class TestLoadScenario(TestCase):

    def test_get_scenarios_from_entry_points(self):
        scenarios = get_scenarios_from_entry_points({})
        self.assertIn('test', scenarios)
