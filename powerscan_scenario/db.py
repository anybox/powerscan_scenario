# This file is a part of the powerscan_scenario project
#
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from sqlalchemy import (create_engine, MetaData, Column, String, Integer,
                        Boolean, ForeignKey, ForeignKeyConstraint, JSON)
from sqlalchemy.orm import relationship, scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import NullPool
from logging import getLogger

logger = getLogger(__name__)


class DBManagerException(Exception):
    pass


class DBManager:

    def __init__(self, configuration=None, scenarios=None):
        if configuration is None:
            raise DBManagerException('No configuration to initialize DBManager')

        self.config = configuration
        if scenarios is None:
            scenarios = {}  # in this case only the base model will be created

        self.scenarios = scenarios
        self.connect_to_database()
        self.create_model_scenario()
        self.create_model_step()
        self.create_model_transition()
        self.create_model_job()
        self.create_model_scanner()
        self.create_scenarios_models()
        self.metadata.create_all(self.engine)
        session_factory = sessionmaker(bind=self.engine)
        self.Session = scoped_session(session_factory)

    @property
    def session(self):
        return self.Session()

    def connect_to_database(self):
        if 'sqlalchemy_url' not in self.config:
            raise DBManagerException('No sqlalchemy_url in the configuration')

        kwargs = {
            'strategy': 'threadlocal',
            'isolation_level': 'SERIALIZABLE',
        }
        url = self.config['sqlalchemy_url']
        if url.startswith('sqlite:'):
            kwargs.setdefault('poolclass', NullPool)

        logger.info('Connect to the database %r ', url)
        self.engine = create_engine(url, **kwargs)
        self.metadata = MetaData()
        self.DBBase = declarative_base(metadata=self.metadata)

    def create_model_scenario(self):

        class Scenario(self.DBBase):
            __tablename__ = "scenario"

            name = Column(String, primary_key=True, nullable=False)
            sequence = Column(Integer, nullable=False)
            label = Column(String, nullable=False)
            version = Column(String, nullable=False)
            dev = Column(Boolean, nullable=False)

        self.Scenario = Scenario

    def create_model_step(self):

        class Step(self.DBBase):
            __tablename__ = "step"

            name = Column(String, nullable=False, primary_key=True)
            scenario = Column(String, ForeignKey('scenario.name'),
                              primary_key=True, nullable=False)
            is_first_step = Column(Boolean, default=False)
            is_final_step = Column(Boolean, default=False)
            method_name_on_scenario = Column(String, nullable=False)

        self.Step = Step

    def create_model_transition(self):

        class Transition(self.DBBase):
            __tablename__ = "transition"

            name = Column(String, nullable=False, primary_key=True)
            scenario = Column(String, primary_key=True, nullable=False)
            from_step = Column(String, primary_key=True, nullable=False)
            to_step = Column(String, primary_key=True, nullable=False)
            sequence = Column(Integer, nullable=False)
            method_name_on_scenario = Column(String, nullable=False)

            __table_args__ = (
                ForeignKeyConstraint(
                    [scenario, from_step],
                    [self.Step.scenario, self.Step.name]),
                ForeignKeyConstraint(
                    [scenario, to_step],
                    [self.Step.scenario, self.Step.name]),
            )

        self.Transition = Transition

    def create_model_job(self):

        class Job(self.DBBase):
            __tablename__ = "job"

            id = Column(Integer, primary_key=True, nullable=False)
            scenario_name = Column(String, ForeignKey('scenario.name'),
                                   nullable=False)
            scenario = relationship('Scenario', backref='jobs')
            properties = Column(JSON, default={})

        self.Job = Job

    def create_model_scanner(self):

        class Scanner(self.DBBase):
            __tablename__ = "scanner"

            code = Column(Integer, primary_key=True, nullable=False)
            job_id = Column(Integer, ForeignKey('job.id'), nullable=False)
            job = relationship('Job', backref="scanners")
            scenario = Column(String, nullable=False)
            step = Column(String, nullable=False)
            properties = Column(JSON, default={})
            step_result = Column(JSON, default={})

            __table_args__ = (
                ForeignKeyConstraint(
                    [scenario, step],
                    [self.Step.scenario, self.Step.name]),
            )

        self.Scanner = Scanner

    def create_scenarios_models(self):
        for scenario in self.scenarios.values():
            if not self.config.get('allow_dev') and scenario.dev:
                continue

            scenario.create_models(self.DBBase)

    # def get_contextual_connect(self):
    #     return self.engine.contextual_connect()
