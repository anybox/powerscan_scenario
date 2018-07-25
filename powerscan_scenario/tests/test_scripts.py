# This file is a part of the powerscan_scenario project
#
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from unittest import TestCase
from ..scripts import initialize_config, get_engine
from .common import drop_and_create_db_if_exist


class TestScript(TestCase):

    def test_initialize_config(self):
        config = initialize_config(
            description='powerscan scenario',
            section='POWERSCAN_SCENARIO',
            entry_point='powerscan_scenario.argparse',
            parser_args=['-u', 'postgresql+psycopg2:///powerscan_scenario',
                         '--allow-dev', '-m', 'CONSOL', '-l', 'DEBUG']
        )
        self.assertEqual(config, {
            'serial_baudrate': 38400,
            'mode': 'CONSOL',
            'allow_dev': True,
            'logging_level': 'DEBUG',
            'serial_port': '/dev/ttyUSB0',
            'sqlalchemy_url': 'postgresql+psycopg2:///powerscan_scenario',
        })

    def test_get_engine(self):
        url = 'postgresql+psycopg2:///powerscan_scenario'
        config = {
            'mode': 'CONSOL',
            'allow_dev': True,
            'logging_level': 'DEBUG',
            'sqlalchemy_url': url,
        }
        drop_and_create_db_if_exist(url)
        get_engine(config)
