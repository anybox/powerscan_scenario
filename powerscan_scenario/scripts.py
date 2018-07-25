# This file is a part of the powerscan_scenario project
#
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from .config import (Configuration, get_argparse_config_from_entrypoint,
                     initialize_logging)
from .scannerbase import ScannerBase, ScannerBaseConsol
from .scenario import get_scenarios_from_entry_points
from .db import DBManager
from .engine import Engine
from argparse import ArgumentParser
from logging import getLogger

logger = getLogger(__name__)


def initialize_config(section=None, description=None,
                      entry_point=None, parser_args=None):
    config = Configuration()
    config.set_configfile_section(section)
    parser = ArgumentParser(description=description)
    get_argparse_config_from_entrypoint(parser, entry_point, config)
    args = parser.parse_args(parser_args)
    config.update(dict(args._get_kwargs()))
    initialize_logging(config)
    return config


def get_engine(config):
    scenarios = get_scenarios_from_entry_points(config)
    dbmanager = DBManager(scenarios=scenarios, configuration=config)
    mode = config.get('mode')
    if mode == 'CONSOL':
        base = ScannerBaseConsol()
    else:
        base = ScannerBase(serialport=config.get('serial_port'),
                           baudrate=config.get('serial_baudrate'))
    logger.info("Start powerscan scenario")
    return Engine(config, base, dbmanager)


def powerscan_scenario():
    config = initialize_config(
        description='powerscan scenario',
        section='POWERSCAN_SCENARIO',
        entry_point='powerscan_scenario.argparse')
    get_engine(config).start()


def powerscan_config():
    config = initialize_config(
        description='powerscan : update scanner configuration',
        section='POWERSCAN_CONFIG',
        entry_point='powerscan_config.argparse')

    base = ScannerBase(serialport=config.get('serial_port'),
                       baudrate=config.get('serial_baudrate'))
    logger.info("Start powerscan config")
    base.configure_scanner(config.get('scanner_code'),
                           config.get('scanner_configfile'))
