# This file is a part of the powerscan_scenario project
#
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from .config import (Configuration, get_argparse_config_from_entrypoint,
                     initialize_logging)
from .scannerbase import ScannerBase
from .scenario import get_scenarios_from_entry_points
from argparse import ArgumentParser
from logging import getLogger

logger = getLogger(__name__)


def powerscan_scenario():
    config = Configuration()
    config.set_configfile_section('POWERSCAN_SCENARIO')
    parser = ArgumentParser(description='powerscan scenario')
    get_argparse_config_from_entrypoint(
        parser, 'powerscan_scenario.argparse', config)
    args = parser.parse_args()
    config.update(dict(args._get_kwargs()))
    initialize_logging(config)
    scenarios = get_scenarios_from_entry_points(config)
    base = ScannerBase(serialport=config.get('serial_port'),
                       baudrate=config.get('serial_baudrate'))
    logger.info("Start powerscan scenario")
    base, scenarios
    # TODO get scenarios from entry points
    # TODO initialize db and alter it if need
    # TODO Start ScenarScan


def powerscan_config():
    config = Configuration()
    config.set_configfile_section('POWERSCAN_CONFIG')
    parser = ArgumentParser(
        description='powerscan : update scanner configuration')
    get_argparse_config_from_entrypoint(
        parser, 'powerscan_config.argparse', config)
    args = parser.parse_args()
    config.update(dict(args._get_kwargs()))
    initialize_logging(config)
    base = ScannerBase(serialport=config.get('serial_port'),
                       baudrate=config.get('serial_baudrate'))
    logger.info("Start powerscan config")
    base.configure_scanner(config.get('scanner_code'),
                           config.get('scanner_configfile'))
