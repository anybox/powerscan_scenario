# This file is a part of the powerscan_scenario project
#
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from logging import getLogger
from time import sleep
import threading
from copy import deepcopy
from .common import (NO_ACTION, ACTION_MENU, ACTION_CONFIRM, ACTION_SCAN,
                     ACTION_QUANTITY, ACTION_STOP,
                     BUTTON_LEFT, BUTTON_MIDDLE, BUTTON_RIGHT,
                     SOUND_BADREAD, SOUND_GOODREAD)


logger = getLogger(__name__)


class Engine:

    def __init__(self, configuration, scanner_base, dbmanager):
        self.config = configuration
        self.scanner_base = scanner_base
        self.dbmanager = dbmanager
        self.engine_loop = False

    def start(self):
        self.engine_loop = True
        while self.engine_loop:
            try:
                (scannercode, scan) = self.scanner_base.reception()
                if scannercode:
                    threading.Thread(
                        target=self.process, args=(scannercode, scan)).start()
                    pass  # TODO async process

                sleep(0.01)
            except KeyboardInterrupt:
                self.engine_loop = False
            except Exception as e:
                logger.exception(e)

        self.scanner_base.close()
        self.dbmanager.close()

    def process(self, scannercode, scan):
        Process(self.config, self.scanner_base, self.dbmanager,
                scannercode).execute(scan)


class Process:

    __new = "## New !! ##"
    __reload = "## Reload !! ##"
    __cancel = "## Cancel !! ##"

    def __init__(self, configuration, scanner_base, dbmanager, scannercode):
        self.config = configuration
        self.scanner_base = scanner_base
        self.dbmanager = dbmanager
        self.session = dbmanager.session
        scanner = self.session.query(dbmanager.Scanner).get(scannercode)
        if scanner is None:
            scanner = dbmanager.Scanner(
                code=scannercode,
                step_result=dict(
                    action_type=NO_ACTION, display=[], counter=0, buttons={},
                    sound=SOUND_GOODREAD)
            )
            self.session.add(scanner)
            self.session.flush()

        self.scanner = scanner
        scanner.error = False
        logger.debug('New process for scanner : %r', scanner)
        self.next_state = deepcopy(scanner.step_result)
        self.is_final_step = False

    def execute(self, scan):
        try:
            self._execute(scan)
        except Exception as err:
            logger.exception(err)
            self.display_error()

        message = self.scanner_base.format(**self.next_state)
        self.scanner_base.send(self.scanner.code, message)

        if self.is_final_step:
            try:
                self.reset_job()
            except Exception as err:
                logger.exception(err)

            self.clean_scanner()
        elif self.scanner.error is False:
            self.scanner.step_result = self.next_state

        self.session.commit()
        self.session.close()

    def reset_job(self):
        pass

    def clean_scanner(self):
        pass

    def display_error(self):
        self.next_state = dict(
            action_type=ACTION_CONFIRM,
            display=['Erreur', 'Contacter', 'le support', 'applicatif'],
            counter=0,
            buttons={BUTTON_MIDDLE: ' OK'},
            sound=SOUND_BADREAD)
        self.scanner.error = True

    def display_scenario_menu(self):
        self.scanner.job = None
        self.scanner.scenario = None
        self.scanner.step = None
        self.session.flush()
        query = self.session.query(self.dbmanager.Scenario)
        if not self.config.get('allow_dev'):
            query = query.filter_by(dev=False)

        query = query.order_by(self.dbmanager.Scenario.sequence)
        self.next_state = dict(
            display=[x.label for x in query.all()] + [self.__reload],
            action_type=ACTION_MENU, counter=0, buttons={},
            sound=SOUND_GOODREAD)

    def display_job_menu(self, scenario):
        query = self.session.query(self.dbmanager.Job)
        query = query.filter_by(scenario=scenario)
        query = query.order_by(self.dbmanager.Job.id)
        self.next_state = dict(
            display=([x.label for x in query.all()] +
                     [self.__new, self.__cancel]),
            action_type=ACTION_MENU, counter=0, buttons={},
            sound=SOUND_GOODREAD)

    def create_job(self, scenario):
        job = self.dbmanager.Job(scenario_name=scenario, properties={})
        self.session.add(job)
        self.session.flush()
        return job

    def run_job(self, scenario_label=None, job_label=None, job=None):
        if scenario_label:
            query = self.session.query(self.dbmanager.Scenario)
            query = query.filter_by(label=scenario_label)
            scenario = query.one()
            if scenario.multi_job:
                self.scanner.scenario = scenario.name
                self.session.flush()
                self.display_job_menu(scenario)
                return
            else:
                job = self.create_job(scenario.name)
        elif job_label:
            query = self.session.query(self.dbmanager.job)
            query = query.filter_by(label=job_label)
            job = query.one()

        if job is None:
            self.display_error()
            return

        query = self.session.query(self.dbmanager.Step)
        query = query.filter_by(scenario=job.scenario_name,
                                is_first_step=True)
        step = query.one()
        self.scanner.job = job
        self.scanner.scenario = step.scenario
        self.session.flush()
        self.execute_step(step, None)

    def get_next_step(self, scan):
        query = self.session.query(self.dbmanager.Transition)
        query = query.filter_by(scenario=self.scanner.scenario,
                                from_step=self.scanner.step)
        query = query.order_by(self.dbmanager.Transition.sequence)
        for transition in query.all():
            if self.execute_transition(transition, scan):
                query = self.session.query(self.dbmanager.Step)
                query = query.filter_by(scenario=self.scanner.scenario,
                                        name=transition.to_step)
                return query.one()
        else:
            return None

    def execute_step(self, step, scan):
        scenario = self.dbmanager.scenarios[step.scenario]
        self.next_state = dict(
            display=[], action_type=ACTION_SCAN, counter=0, buttons={},
            sound=SOUND_GOODREAD)
        self.next_state.update(
            getattr(scenario, step.method_name_on_scenario)(
                self.session, self.scanner, scan))
        if step.is_final_step:
            self.is_final_step = True

        self.scanner.step = step.name

    def execute_transition(self, transition, scan):
        scenario = self.dbmanager.scenarios[transition.scenario]
        return getattr(scenario, transition.method_name_on_scenario)(
                self.session, self.scanner, scan)

    def _execute_menu(self, scan):
        display = self.next_state['display']
        if (
            scan == BUTTON_RIGHT and
            self.next_state['counter'] < len(display) - 1
        ):
            self.next_state['counter'] += 1
        elif scan == BUTTON_LEFT and self.next_state['counter'] > 0:
            self.next_state['counter'] -= 1
        elif scan == BUTTON_MIDDLE:
            label = display[self.next_state['counter']]
            if not self.scanner.scenario:
                if label == self.__reload:
                    self.display_scenario_menu()
                else:
                    self.run_job(scenario_label=label)
            elif not self.scanner.job:
                if label == self.__cancel:
                    self.display_scenario_menu()
                elif label == self.__new:
                    job = self.create_job(self.scanner.scenario)
                    scenario = self.dbmanager.scenarios[
                        self.scanner.scenario]
                    scenario.set_job_label(job)
                    self.run_job(job=job)
            elif not self.scanner.step:
                self.run_job(job=self.scanner.job)
            else:
                query = self.session.query(self.dbmanager.Step)
                query = query.filter_by(scenario=self.scanner.scenario,
                                        step=self.scanner.step)
                self.execute_step(query.one(), scan)

    def _execute_scan(self, scan):
        if scan in (BUTTON_LEFT, BUTTON_RIGHT):
            return  # TODO check display size and counter, multi line
        elif scan == BUTTON_MIDDLE:
            return
        else:
            step = self.get_next_step(scan)
            if step:
                self.execute_step(step, scan)
            else:
                self.display_error()

    def _execute_quantity(self, scan):
        if scan == BUTTON_RIGHT:
            self.next_state['counter'] += 1
        elif scan == BUTTON_LEFT:
            self.next_state['counter'] -= 1
        elif scan == BUTTON_MIDDLE:
            step = self.get_next_step(self.next_state['counter'])
            if step:
                self.execute_step(step, scan)
            else:
                self.display_error()

    def _execute_confirm(self, scan):
        if self.next_state['buttons'].get(scan, None) is not None:
            step = self.get_next_step(self.next_state['counter'])
            if step:
                self.execute_step(step, scan)
            else:
                self.display_error()

    def _execute_stop(self, scan):
        # if no scanner run job, then the job will be terminate
        job = self.scanner.job
        query = self.session.query(self.dbmanager.Scanner)
        query = query.filter_by(job=job)
        if query.count() == 0:
            self.is_final_step = True

        self.display_scenario_menu()

    def _execute(self, scan):
        action = self.next_state['action_type']
        if action == NO_ACTION:
            self.display_scenario_menu()
        elif action == ACTION_MENU:
            self._execute_menu(scan)
        elif action == ACTION_SCAN:
            self._execute_scan(scan)
        elif action == ACTION_QUANTITY:
            self._execute_quantity(scan)
        elif action == ACTION_CONFIRM:
            self._execute_confirm(scan)
        elif action == ACTION_STOP:
            self._execute_stop(scan)
