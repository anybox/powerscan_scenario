# This file is a part of the powerscan_scenario project
#
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from unittest import TestCase
from ..config import (
    add_scenario_argparse_config, add_config_argparse_config,
    add_logging_argparse_config, get_argparse_config_from_entrypoint
)


class MockArgumentValue:

    def __init__(self, **kwargs):
        self.default = None
        self.type = str
        self.__dict__.update(kwargs)


class MockArgumentParser:

    def add_argument_group(self, *args, **kwargs):
        return MockArgumentParser()

    def add_argument(self, *args, **kwargs):
        return MockArgumentValue(**kwargs)


class GiveParser:

    @classmethod
    def setUpClass(cls):
        super(GiveParser, cls).setUpClass()
        cls.parser = MockArgumentParser()


class TestScenarioArgParse(GiveParser, TestCase):

    def test_get_config_from_entry_point(self):
        get_argparse_config_from_entrypoint(
            self.parser, 'powerscan_scenario.argparse')

    def test_add_scenario_argparse_config(self):
        add_scenario_argparse_config(self.parser)

    def test_add_logging_argparse_config(self):
        add_logging_argparse_config(self.parser)


class TestConfigArgParse(GiveParser, TestCase):

    def test_get_config_from_entry_point(self):
        get_argparse_config_from_entrypoint(
            self.parser, 'powerscan_config.argparse')

    def test_add_config_argparse_config(self):
        add_config_argparse_config(self.parser)
