# This file is a part of the powerscan_scenario project
#
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from pkg_resources import iter_entry_points
import os
from os.path import isfile
from configparser import ConfigParser
from logging import (config, NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL,
                     basicConfig, getLogger)
logger = getLogger(__name__)

LEVELS = {
    'NOTSET': NOTSET,
    'DEBUG': DEBUG,
    'INFO': INFO,
    'WARNING': WARNING,
    'ERROR': ERROR,
    'CRITICAL': CRITICAL
}


class ConfigurationException(Exception):
    pass


def initialize_logging(Configuration):
    level = LEVELS.get(Configuration.get('logging_level'))
    logging_configfile = Configuration.get('logging_configfile')

    if logging_configfile:
        config.fileConfig(logging_configfile)

    if level:
        basicConfig(level=level)


class Configuration(dict):

    configfile_section = None

    def set_configfile_section(self, section):
        self.configfile_section = section

    def parse_configfile(self, configfile):
        if self.configfile_section is None:
            raise ConfigurationException("No configfile section name")

        if not isfile(configfile):
            raise ConfigurationException(
                "No such file or not a regular file: %r " % configfile)

        cparser = ConfigParser()
        cparser.read(configfile)
        sections = cparser.items(self.configfile_section)
        for opt, value in sections:
            if value:
                self[opt] = value

    def update(self, dict2):
        dict2 = dict([(x, y) for x, y in dict2.items() if y is not None])
        if 'configfile' in dict2:
            configfile = os.path.abspath(dict2['configfile'])
            self.parse_configfile(configfile)

        super(Configuration, self).update(dict2)


def get_argparse_config_from_entrypoint(parser, entry_point,
                                        default_configuration):
    logger.info('powerscan_scenario load %r configuration' % entry_point)
    for i in iter_entry_points(entry_point):
        i.load()(parser, default_configuration)


def add_logging_argparse_config(parser, default_configuration):
    group = parser.add_argument_group('Powerscan logging')
    group.add_argument('-l', '--logging-level', dest='logging_level',
                       choices=['NOTSET', 'DEBUG', 'INFO', 'WARNING',
                                'ERROR', 'CRITICAL'])
    group.add_argument('--logging-configfile', dest='logging_configfile',
                       help="Relative path of the logging config file")
    default_configuration.update(dict(logging_level='INFO'))


def add_scenario_argparse_config(parser, default_configuration):
    group = parser.add_argument_group('Powerscan scenario')
    group.add_argument('-c', '--configfile', dest='configfile',
                       help="Relative path of the config file")
    group.add_argument('-p', '--serial-port', dest='serial_port',
                       help="Serial port used by the scanner")
    group.add_argument(
        '-b', '--serial-baudrate', dest='serial_baudrate', type=int,
        help="baudrate used by the connection with scanner base")
    group.add_argument('-d', '--allow-dev', dest='allow_dev',
                       action='store_true',
                       help="Allow the scenario in mode dev")
    group.add_argument('-u', '--sqlalchemy-url', dest='sqlalchemy_url',
                       help="SQLAlchemy url to connect to the database")
    default_configuration.update(dict(serial_port='/dev/ttyUSB0',
                                      serial_baudrate=38400))


def add_config_argparse_config(parser, default_configuration):
    group = parser.add_argument_group('Powerscan config')
    group.add_argument('-c', '--configfile', dest='configfile',
                       help="Relative path of the config file")
    group.add_argument('-p', '--serial-port', dest='serial_port',
                       help="Serial port used by the scanner")
    group.add_argument(
        '-b', '--serial-baudrate', dest='serial_baudrate', type=int,
        help="baudrate used by the connection with scanner base")
    group.add_argument('-s', '--scanner-code', dest='scanner_code',
                       help="Code of the scanner")
    group.add_argument('-k', '--scanner-configfile', dest='scanner_configfile',
                       help="Relative path of the config file for the scanner")
    default_configuration.update(dict(serial_port='/dev/ttyUSB0',
                                      serial_baudrate=38400))
