# This file is a part of the powerscan_scenario project
#
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from ..scenario import Scenario
from sqlalchemy import Column, String, Integer


class OneScenario(Scenario):
    label = 'One Scenario'
    version = '1.0.0'
    sequence = 50
    dev = True

    def create_models(self, SQLBase):

        class TestProduct(SQLBase):
            __tablename__ = "test_product"

            scan = Column(String, primary_key=True, nullable=False)
            qty = Column(Integer, default=0)

        self.TestProduct = TestProduct
