# This file is a part of the powerscan_scenario project
#
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from sqlalchemy import (create_engine, MetaData, Column, String, Integer,
                        Boolean, ForeignKey, ForeignKeyConstraint, JSON, and_,
                        or_)
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
        self.update_all_scenarios()

    def close(self):
        self.session.rollback()
        self.session.expunge_all()
        self.session.close_all()
        self.engine.dispose()

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
            dev = Column(Boolean, default=False)

        self.Scenario = Scenario

    def create_model_step(self):

        class Step(self.DBBase):
            __tablename__ = "step"

            name = Column(String, nullable=False, primary_key=True)
            scenario = Column(String,
                              ForeignKey('scenario.name', ondelete="CASCADE"),
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
                    [self.Step.scenario, self.Step.name],
                    ondelete="CASCADE"
                ),
                ForeignKeyConstraint(
                    [scenario, to_step],
                    [self.Step.scenario, self.Step.name],
                    ondelete="CASCADE"
                ),
            )

        self.Transition = Transition

    def create_model_job(self):

        class Job(self.DBBase):
            __tablename__ = "job"

            id = Column(Integer, primary_key=True, nullable=False)
            scenario_name = Column(
                String, ForeignKey('scenario.name', ondelete="RESTRICT"),
                nullable=False)
            scenario = relationship('Scenario', backref='jobs')
            properties = Column(JSON, default={})

        self.Job = Job

    def create_model_scanner(self):

        class Scanner(self.DBBase):
            __tablename__ = "scanner"

            code = Column(Integer, primary_key=True, nullable=False)
            job_id = Column(Integer, ForeignKey('job.id', ondelete='RESTRICT'))
            job = relationship('Job', backref="scanners")
            scenario = Column(String)
            step = Column(String)
            properties = Column(JSON, default={})
            step_result = Column(JSON, default={})

            __table_args__ = (
                ForeignKeyConstraint(
                    [scenario, step],
                    [self.Step.scenario, self.Step.name],
                    ondelete="RESTRICT"
                ),
            )

        self.Scanner = Scanner

    def create_scenarios_models(self):
        for scenario in self.scenarios.values():
            if not self.config.get('allow_dev') and scenario.dev:
                continue

            scenario.create_models(self.DBBase)

    def delete_scenario(self, scenario):
        query = self.session.query(self.Scenario)
        query.filter_by(name=scenario).delete()

    def add_scenario(self, scenario_name):
        scenario_ = self.scenarios[scenario_name]
        session = self.session
        session.add(self.Scenario(
            name=scenario_name,
            **{x: getattr(scenario_, x)
               for x in ('label', 'sequence', 'version', 'dev')}))
        session.flush()
        steps, transitions = scenario_.get_steps_and_transitions()
        for step in steps:
            self.add_step(scenario_name, steps[step])

        session.flush()
        for transition in transitions:
            self.add_transition(scenario_name, transitions[transition])

        session.flush()

    def update_scenario(self, scenario):
        scenario_ = self.scenarios[scenario.name]
        session = self.session
        if scenario_.version != scenario.version:
            scenario_.update_tables(session, scenario.version)

        for attr in ('label', 'sequence', 'version', 'dev'):
            setattr(scenario, attr, getattr(scenario_, attr))

        steps, transitions = scenario_.get_steps_and_transitions()
        self.update_all_steps(scenario, steps)
        self.update_all_transitions(scenario, transitions)

    def update_all_scenarios(self):
        session = self.session
        scenarios = list(self.scenarios.keys())
        query = session.query(self.Scenario)
        query = query.filter(self.Scenario.name.notin_(scenarios))
        for scenario in query.all():
            self.delete_scenario(scenario.name)

        for scenario_name in scenarios:
            scenario = session.query(self.Scenario).get(scenario_name)
            if scenario is None:
                self.add_scenario(scenario_name)
            else:
                self.update_scenario(scenario)

    def delete_step(self, step):
        query = self.session.query(self.Step)
        query.filter_by(name=step).delete()

    def add_step(self, scenario_name, step):
        self.session.add(self.Step(
            scenario=scenario_name, **step))

    def update_step(self, step, step_definition):
        for attr in step_definition:
            setattr(step, attr, step_definition[attr])

    def update_all_steps(self, scenario, steps):
        session = self.session
        query = session.query(self.Step)
        query = query.filter(self.Step.scenario == scenario.name)
        query = query.filter(self.Step.name.notin_(list(steps.keys())))
        for step in query.all():
            self.delete_step(step.name)

        for step_name in steps:
            query = session.query(self.Step)
            query = query.filter(self.Step.scenario == scenario.name)
            query = query.filter(self.Step.name == step_name)
            step = query.one_or_none()
            if step is None:
                self.add_step(scenario.name, steps[step_name])
            else:
                self.update_step(step, steps[step_name])

    def delete_transition(self, transition):
        query = self.session.query(self.Transition)
        query = query.filter_by(
            name=transition.name, to_step=transition.to_step,
            from_step=transition.from_step)
        query.delete()

    def add_transition(self, transition_name, transition):
        self.session.add(self.Transition(
            scenario=transition_name, **transition))

    def update_transition(self, transition, transition_definition):
        for attr in transition_definition:
            setattr(transition, attr, transition_definition[attr])

    def update_all_transitions(self, scenario, transitions):
        session = self.session
        query = session.query(self.Transition)
        query = query.filter(self.Transition.scenario == scenario.name)
        where_clause = []
        for name, to_step, from_step in transitions:
            where_clause.append(~and_(
                self.Transition.name == name,
                self.Transition.to_step == to_step,
                self.Transition.from_step == from_step))
        query = query.filter(or_(*where_clause))
        for transition in query.all():
            self.delete_transition(transition)

        for transition_name in transitions:
            query = session.query(self.Transition)
            query = query.filter(self.Transition.scenario == scenario.name)
            where_clause = []
            for name, to_step, from_step in transitions:
                where_clause.append(and_(
                    self.Transition.name == name,
                    self.Transition.to_step == to_step,
                    self.Transition.from_step == from_step))
            query = query.filter(or_(*where_clause))
            transition = query.one_or_none()
            if transition is None:
                self.add_transition(scenario.name, transitions[transition_name])
            else:
                self.update_transition(transition, transitions[transition_name])

    # def get_contextual_connect(self):
    #     return self.engine.contextual_connect()
