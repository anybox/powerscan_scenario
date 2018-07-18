# This file is a part of the powerscan_scenario project
#
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from pkg_resources import iter_entry_points
from logging import getLogger
logger = getLogger(__name__)


class ScenarioException(Exception):
    pass


def get_scenarios_from_entry_points(configuration):
    scenarios = {}
    for i in iter_entry_points('powerscan_scenario.scenario'):
        scenario = i.load()(configuration)
        if i.name in scenarios:
            raise ScenarioException(
                "A scenario with the name %r has already loaded" % i.name)

        scenarios[i.name] = scenario
        logger.info('scenario %r loaded' % i.name)

    return scenarios


class Scenario:
    version = '0.0.0'
    label = None
    sequence = 100
    dev = False

    def __init__(self, configuration):
        self.config = configuration
