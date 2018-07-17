# This file is a part of the powerscan_scenario project
#
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from unittest import TestCase
import tempfile
from ..config import (
    add_scenario_argparse_config, add_config_argparse_config, Configuration,
    add_logging_argparse_config, get_argparse_config_from_entrypoint,
    ConfigurationException, initialize_logging
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
            self.parser, 'powerscan_scenario.argparse', {})

    def test_configuration(self):
        conf = Configuration()
        conf.set_configfile_section('POWERSCAN_SCENARIO')
        dict2 = {'serial_port': '/dev/ttyUSB0'}
        conf.update(dict2)
        self.assertEqual(conf, dict2)

    def test_configuration_with_configfile(self):
        conf = Configuration()
        conf.set_configfile_section('POWERSCAN_SCENARIO')
        with tempfile.NamedTemporaryFile('w') as fp:
            fp.write('[POWERSCAN_SCENARIO]\nserial_port = /dev/ttyUSB0')
            fp.seek(0)
            conf.update(dict(configfile=fp.name))
            self.assertEqual(conf, {
                'configfile': fp.name,
                'serial_port': '/dev/ttyUSB0'})

    def test_configuration_with_configfile_without_section(self):
        conf = Configuration()
        with tempfile.NamedTemporaryFile('w') as fp:
            fp.write('[POWERSCAN_SCENARIO]\nserial_port = /dev/ttyUSB0')
            fp.seek(0)
            with self.assertRaises(ConfigurationException):
                conf.update(dict(configfile=fp.name))

    def test_configuration_with_configfile_is_not_a_file(self):
        conf = Configuration()
        conf.set_configfile_section('POWERSCAN_SCENARIO')
        with self.assertRaises(ConfigurationException):
            conf.update(dict(configfile='not a file'))

    def test_add_scenario_argparse_config(self):
        default_configuration = {}
        add_scenario_argparse_config(self.parser, default_configuration)
        self.assertEqual(default_configuration,
                         {'serial_port': '/dev/ttyUSB0',
                          'serial_baudrate': 38400})

    def test_add_logging_argparse_config(self):
        default_configuration = {}
        add_logging_argparse_config(self.parser, default_configuration)
        self.assertEqual(default_configuration, {'logging_level': 'INFO'})


class TestConfigArgParse(GiveParser, TestCase):

    def test_get_config_from_entry_point(self):
        get_argparse_config_from_entrypoint(
            self.parser, 'powerscan_config.argparse', {})

    def test_add_config_argparse_config(self):
        default_configuration = {}
        add_config_argparse_config(self.parser, default_configuration)
        self.assertEqual(default_configuration,
                         {'serial_port': '/dev/ttyUSB0',
                          'serial_baudrate': 38400})


class TestLogging(TestCase):

    def test_with_empty_configuration(self):
        config = {}
        initialize_logging(config)

    def test_with_logging_level(self):
        config = {'logging_level': 'INFO'}
        initialize_logging(config)

    def test_with_config_file(self):
        with tempfile.NamedTemporaryFile('w') as fp:
            file_ = """
[loggers]
keys=root

[handlers]
keys=consoleHandler

[formatters]
keys=consoleFormatter

[logger_root]
level=INFO
handlers=consoleHandler

[handler_consoleHandler]
class=StreamHandler
level=INFO
args=(sys.stdout,)

[formatter_consoleFormatter]
format=%(levelname)s - %(name)s:%(message)s
datefmt=
"""

            fp.write(file_)
            fp.seek(0)

            config = {'logging_configfile': fp.name}
            initialize_logging(config)
