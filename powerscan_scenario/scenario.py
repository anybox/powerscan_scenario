# This file is a part of the powerscan_scenario project
#
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from pkg_resources import iter_entry_points
from . import common
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
    multi_job = False

    LeftButton = common.BUTTON_LEFT
    MiddleButton = common.BUTTON_MIDDLE
    RightButton = common.BUTTON_RIGHT

    NoAction = common.NO_ACTION
    Menu = common.ACTION_MENU
    Quantity = common.ACTION_QUANTITY
    Scan = common.ACTION_SCAN
    Confirm = common.ACTION_CONFIRM
    Stop = common.ACTION_STOP

    ShortHight = common.SOUND_SHORTHIGHT
    ShortLow = common.SOUND_SHORTLOW
    LongLow = common.SOUND_LONGLOW
    GoodRead = common.SOUND_GOODREAD
    BadRead = common.SOUND_BADREAD
    Wait = common.SOUND_WAIT

    def __init__(self, configuration):
        self.config = configuration

    def create_models(self, SQLBase):
        pass  # TODO

    def update_tables(self, session, latest_version):
        pass  # TODO

    def set_job_label(self, job):
        raise ScenarioException("No 'set_job_label' on %r" % self)

    def get_steps_and_transitions(self):  # noqa
        steps = {}
        transitions = {}
        step_methods = []
        transition_methods = []

        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if hasattr(attr, 'is_a_step') and attr.is_a_step:
                step_methods.append(attr.step_definition)
            elif hasattr(attr, 'is_a_transition') and attr.is_a_transition:
                transition_methods.append(attr.transition_definition)

        if not step_methods:
            raise ScenarioException('%r no step defined' % self)

        if not transition_methods:
            raise ScenarioException('%r no transition defined' % self)

        for step in step_methods:
            name = step['name']
            if name in steps:
                raise Exception(
                    'In the scenarion %r, the step %r already exit' % (
                        self, name))

            steps[name] = step

        for transition in transition_methods:
            transition = transition.copy()
            name = transition['name']
            to_step = transition.pop('to')
            for from_step in transition.pop('froms'):
                if (name, to_step, from_step) in transitions:
                    raise Exception(
                        'In the sceranrio %r, transition %r already exit' % (
                            self, (name, to_step, from_step)))

                transition.update(dict(to_step=to_step, from_step=from_step))
                transitions[(name, to_step, from_step)] = transition

        return steps, transitions
