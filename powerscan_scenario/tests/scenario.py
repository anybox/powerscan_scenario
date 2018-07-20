# This file is a part of the powerscan_scenario project
#
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from ..scenario import Scenario
from ..decorator import step, transition
from sqlalchemy import Column, String, Integer


class EmptyScenario(Scenario):
    label = 'Empty Scenario'
    version = '1.0.0'
    sequence = 50


class OneScenario(Scenario):
    label = 'One Scenario'
    version = '1.0.0'
    sequence = 50
    dev = True
    scan_stop = "stop"

    def create_models(self, SQLBase):

        class TestProduct(SQLBase):
            __tablename__ = "test_product"

            scan = Column(String, primary_key=True, nullable=False)
            qty = Column(Integer, default=0)

        self.TestProduct = TestProduct

    @step(is_first_step=True)
    def scan(self, session, scanner, scan):
        if scan:
            product = session.query(self.TestProduct).get(scan)
            if not product:
                product = self.TestProduct(scan=scan)
                session.add(product)

            product.qty += 1

        return {
            'display': ['Scan a product']
        }

    @step()
    def stop(self, *a):
        return {
            'action_type': self.Stop,
        }

    @transition(froms=['scan'], to='stop', sequence=1)
    def to_stop(self, session, scanner, scan):
        return scan == self.scan_stop

    @transition(froms=['scan'], to='scan', sequence=2)
    def to_scan(self, *a):
        return True
