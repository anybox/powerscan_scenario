# This file is a part of the powerscan_scenario project
#
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from logging import getLogger
from time import sleep


logger = getLogger(__name__)


class Engine:

    def __init__(self, scanner_base, dbmanager):
        self.scanner_base = scanner_base
        self.dbmanager = dbmanager
        self.engine_loop = False

    def start(self):
        self.engine_loop = True
        while self.engine_loop:
            try:
                (scannercode, scan) = self.scanner_base.reception()
                if not scannercode:
                    pass  # TODO async process

                sleep(0.01)
            except KeyboardInterrupt:
                self.engine_loop = False
            except Exception as e:
                logger.exception(e)

        self.scanner_base.close()
        self.dbmanager.close()
