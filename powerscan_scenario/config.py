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


def get_argparse_config_from_entrypoint(parser, entry_point):
    logger.info('powerscan_scenario load %r configuration' % entry_point)
    for i in iter_entry_points(entry_point):
        i.load()(parser)


def add_logging_argparse_config(parser):
    group = parser.add_argument_group('Powerscan logging')
    group.add_argument('--logging-level', dest='logging_level',
                       choices=['NOTSET', 'DEBUG', 'INFO', 'WARNING',
                                'ERROR', 'CRITICAL'], default='INFO')
    group.add_argument('--logging-configfile', dest='logging_configfile',
                       help="Relative path of the logging config file")


def add_scenario_argparse_config(parser):
    group = parser.add_argument_group('Powerscan scenario')
    group.add_argument('-c', '--configfile', dest='configfile',
                       help="Relative path of the config file")
    group.add_argument('-p', '--serial-port', dest='serial_port',
                       default='/dev/ttyUSB0',
                       help="Serial port used by the scanner")
    group.add_argument('-u', '--sqlalchemy-url', dest='sqlalchemy_url',
                       help="SQLAlchemy url to connect to the database")


def add_config_argparse_config(parser):
    group = parser.add_argument_group('Powerscan config')
    group.add_argument('-c', '--configfile', dest='configfile',
                       help="Relative path of the config file")
    group.add_argument('-p', '--serial-port', dest='serial_port',
                       default='/dev/ttyUSB0',
                       help="Serial port used by the scanner")
    group.add_argument('-s', '--scanner-code', dest='scanner_code',
                       help="Code of the scanner")
    group.add_argument('-k', '--scanner-configfile', dest='scanner_configfile',
                       help="Relative path of the config file for the scanner")
