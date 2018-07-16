.. This file is a part of the powerscan_scenario project
..
..    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
..
.. This Source Code Form is subject to the terms of the Mozilla Public License,
.. v. 2.0. If a copy of the MPL was not distributed with this file,You can
.. obtain one at http://mozilla.org/MPL/2.0/.

.. image:: https://travis-ci.org/anybox/powerscan_scenario.svg?branch=master
    :target: https://travis-ci.org/anybox/powerscan_scenario
    :alt: Build status

.. image:: https://coveralls.io/repos/github/anybox/powerscan_scenario/badge.svg?branch=master
    :target: https://coveralls.io/github/anybox/powerscan_scenario?branch=master
    :alt: Coverage

.. image:: https://img.shields.io/pypi/v/powerscan_scenario.svg
   :target: https://pypi.python.org/pypi/powerscan_scenario/
   :alt: Version status
   

PowerScan Scenario
==================

Scenario engine for PowerScan (Datalogic scanner)

Each scenario is described in the class, This class is loaded by the setuptools 
entry point ``powerscan.scenario``.

Define a new scenario
---------------------

Each scenario have to inherit from **powerscan_scenario.Scenario**.

::

    from powerscan_scenario.scenario import Scenario


    class MyScenario(Scenario):
        version = '1.0.0'
        label = 'My scenario'


These attributes are saved in the table **scenario**, and are required
+----------------------+-----------------------------------------------------------+
| Attribute            | Description                                               |
+======================+===========================================================+
| version              | current version of the scenario                           |
+----------------------+-----------------------------------------------------------+
| label                | label of the scenario display on the scaner screen        |
+----------------------+-----------------------------------------------------------+

Some hooks can be overwritten 
+-----------------------------------------+--------------------------------------------------------------+
| Method                                  | Description                                                  |
+=========================================+==============================================================+
| create_tables (session)                 | * session : an instance of SQLAlchemy Session instance.      |
|                                         |                                                              |
|                                         | Called when the scenario is added in the table of            |
|                                         | **scenario**, The scenario can create some table for this    |
|                                         | own need to stock data                                       |
+-----------------------------------------+--------------------------------------------------------------+
| update_tables (session, latest_version) | * session : an instance of SQLAlchemy Session instance.      |
|                                         | * latest_version : The version saved on the table            |
|                                         |                                                              |
|                                         | Called when the application **powerscan_scenario** is        |
|                                         | started and the version of the scenario is different         |
+-----------------------------------------+--------------------------------------------------------------+
| initialize_job (session, job)           | * session : an instance of SQLAlchemy Session instance.      |
|                                         | * job : instance of table **job**, a job represent the       |
|                                         |   execution of one scenario                                  |
|                                         |                                                              |
|                                         | Called when a job is added in the table **job**.             |
|                                         | this hook allow to add some data from another system         |
+-----------------------------------------+--------------------------------------------------------------+
| release_job (session, job)              | * session : an instance of SQLAlchemy Session instance.      |
|                                         | * job : instance of table **job**, a job represent the       |
|                                         |   execution of one scenario                                  |
|                                         |                                                              |
|                                         | Called before delete the job from the table.                 |
|                                         | this hook allow to send, remove and clean data               |
+-----------------------------------------+--------------------------------------------------------------+

Add step in the scenario
------------------------

The decorator **powerscan_scenario.decorator.step** is a helper to define a step in the scenario

::

    from powerscan_scenario.scenario import Scenario
    from powerscan_scenario.decorator import step


    class MyScenario(Scenario):
        version = '1.0.0'
        label = 'My scenario'

        @step()
        def foo(self, session, job, scanner, entry):
            # action to do
            return {
                'display': [],  # list of string to display
                'buttons': {},  # button label
                'action_type: '',  # Type of the next action to do
                'sound': '',  # sound to play
            }

These parameters of decorator are saved in the table **step**
+----------------------+-----------------------------------------------------------+
| parameter            | Description                                               |
+======================+===========================================================+
| code                 | name of the step for this scenario, if empty the code is  |
|                      | the name of the method                                    |
+----------------------+-----------------------------------------------------------+
| is_started_step      | boolean (default False). The scenario must have got one   |
|                      | and only one step with this attribute to True value       |
|                      |                                                           |
|                      | This attribute mean that this step is the first step of   |
|                      | the scenario                                              |
+----------------------+-----------------------------------------------------------+
| is_stoped_step       | boolean (default False). The scenario must have got one   |
|                      | or more step(s) with this attribute to True value         |
|                      |                                                           |
|                      | This attribute mean that this step stop the job           |
+----------------------+-----------------------------------------------------------+

The parameters of step method are
+----------------------+-----------------------------------------------------------+
| parameter            | Description                                               |
+======================+===========================================================+
| session              | An instance of a SQLAlchemy Session                       |
+----------------------+-----------------------------------------------------------+
| job                  | The instance of the current job                           |
+----------------------+-----------------------------------------------------------+
| scanner              | The instance of the scanner which have given the entry    |
|                      | data                                                      |
+----------------------+-----------------------------------------------------------+
| entry                | entry received from the scanner                           |
+----------------------+-----------------------------------------------------------+

The step method return a dict with some key, this dict over writting their default values
+----------------------+-----------------------------------------------------------+
| key                  | Description                                               |
+======================+===========================================================+
| display              | List of String, to display on the screen of the scanner,  |
|                      | Each line is limited by X characters                      |
|                      |                                                           |
|                      | The maximum size can be decreased by the action_type      |
|                      | **confirm** or definition of buttons key                  |
+----------------------+-----------------------------------------------------------+
| buttons              | dict of buttons. The available button keys are:           |
|                      |                                                           |
|                      | * **<** or Scenario.LeftButton                            |
|                      | * **=** or Scenario.MiddleButton                          |
|                      | * **>** or Scenario.RightButton                           |
|                      |                                                           |
|                      | The value is the label to display, the maximum size is X  |
+----------------------+-----------------------------------------------------------+
| action_type          | Defined the type of action wanted for the user            |
|                      |                                                           |
|                      | * **no_action** or Scenario.NoAction : Return the         |
|                      |   available scenarios                                     |
|                      | * **menu** or Scenario.Menu : The display is seen as      |
|                      |   a Menu of selected action by buttons                    |
|                      | * **quantity** or Scenario.Quantity : The display is seen |
|                      |   as a confirmation of the quantity:                      |
|                      | * **scan** or Scenario.Scan : The display is seen as      |
|                      |   an ask, and the return waiting is a barcode             |
+----------------------+-----------------------------------------------------------+
| entry                | entry received from the scanner                           |
+----------------------+-----------------------------------------------------------+


AnyBlok is released under the terms of the `Mozilla Public License`.
