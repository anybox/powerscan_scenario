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

AnyBlok is released under the terms of the `Mozilla Public License`.

Installation of powerscan_scenario
----------------------------------

This project is open source the package can be installed from:

* `pip <http://pypi.python.org/pypi/pip>`_ or a similar tool::
  ::

      pip install powerscan_scenario

* source on github
  ::

      git clone git@github.com:anybox/powerscan_scenario.git
      cd powerscan_scenario
      python setup.py install

Running Tests
-------------

To run tests with ``nose``::

    pip install nose
    nosetests powerscan_scenario/tests

Dependencies
------------

The install process will ensure that `SQLAlchemy <http://www.sqlalchemy.org>`_, 
`Alembic <http://alembic.readthedocs.org/>`_,
`SQLAlchemy-Utils <http://sqlalchemy-utils.readthedocs.org/>`_ are installed, 
in addition to other dependencies.

The latest version of them is strongly recommended.

The integrator choose the BBD to use by powerscan

Console script
--------------

powerscan_scenario
~~~~~~~~~~~~~~~~~~

This script load the scenario(s) from the entry points  and loop to wait the scan from scanners to play job from scenario

+----------------------+-----------------------------------------------------------+
| option               | Description                                               |
+======================+===========================================================+
| -c --configfile      | file of configuration, part [POWERSCAN_SCENARIO]          |
+----------------------+-----------------------------------------------------------+
| -p --serial-port     | define which serial port to use                           |
|                      |                                                           |
|                      | * default : /dev/ttyUSB0                                  |
|                      | * configfile key : serial_port                            |
+----------------------+-----------------------------------------------------------+
| -b --serial-baudrate | define baudrate to the connection with the scanner base   |
|                      |                                                           |
|                      | * default : 38400                                         |
|                      | * type : int                                              |
|                      | * configfile key : serial_baudrate                        |
+----------------------+-----------------------------------------------------------+
| -d --allow-dev       | Allow to use the scenario where **dev** attribute is True |
|                      |                                                           |
|                      | * action : store_true                                     |
|                      | * configfile key : allow_dev                              |
+----------------------+-----------------------------------------------------------+
| -u --sqlalchemy-url  | url for sqlalchemy database                               |
|                      |                                                           |
|                      | * default :                                               |
|                      | * configfile key : sqlalchemy_url                         |
+----------------------+-----------------------------------------------------------+
| -m --mode            | mode for scanner base                                     |
|                      |                                                           |
|                      | * default : base                                          |
|                      | * choices :                                               |
|                      |                                                           |
|                      |   + BASE: use the datalogic base                          |
|                      |   + CONSOL: the datalogic base is remplaced by terminal   |
|                      |   + FILE: list of commande defined in file                |
|                      |                                                           |
|                      | * configfile key : mode                                   |
+----------------------+-----------------------------------------------------------+
| --mode-file          | File loaded by **mode=FILE** options                      |
|                      |                                                           |
|                      | * default :                                               |
|                      | * configfile key : mode_file                              |
+----------------------+-----------------------------------------------------------+
| -l --logging-level   | logging level general status                              |
|                      |                                                           |
|                      | * default : INFO                                          |
|                      | * choices :                                               |
|                      |                                                           |
|                      |   + NOTSET                                                |
|                      |   + DEBUG                                                 |
|                      |   + INFO                                                  |
|                      |   + WARNING                                               |
|                      |   + ERROR                                                 |
|                      |   + CRITICAL                                              |
|                      |                                                           |
|                      | * configfile key : logging_level                          |
+----------------------+-----------------------------------------------------------+
| --logging-configfile | file of configuration for python logging                  |
|                      |                                                           |
|                      | * default :                                               |
|                      | * configfile key : logging_configfile                     |
+----------------------+-----------------------------------------------------------+

.. note::

    The entry point ``powerscan_scenario.argparse`` allow to improve the configuration

powerscan_config
~~~~~~~~~~~~~~~~

This script load the configuration into a scanner

+-------------------------+-----------------------------------------------------------+
| option                  | Description                                               |
+=========================+===========================================================+
| -c --configfile         | file of configuration, part [POWERSCAN_CONFIG]            |
+-------------------------+-----------------------------------------------------------+
| -p --serial-port        | define which serial port to use                           |
|                         |                                                           |
|                         | * default : /dev/ttyUSB0                                  |
|                         | * configfile key : serial_port                            |
+-------------------------+-----------------------------------------------------------+
| -s --scanner-code       | code of the scanner                                       |
|                         |                                                           |
|                         | * default :                                               |
|                         | * configfile key : scanner_code                           |
+-------------------------+-----------------------------------------------------------+
| -k --scanner-configfile | file of configuration of the scanner                      |
|                         |                                                           |
|                         | * default :                                               |
|                         | * configfile key : scanner_configfile                     |
+-------------------------+-----------------------------------------------------------+
| --logging-level         | logging level general status                              |
|                         |                                                           |
|                         | * default : INFO                                          |
|                         | * choices :                                               |
|                         |                                                           |
|                         |   + NOTSET                                                |
|                         |   + DEBUG                                                 |
|                         |   + INFO                                                  |
|                         |   + WARNING                                               |
|                         |   + ERROR                                                 |
|                         |   + CRITICAL                                              |
|                         |                                                           |
|                         | * configfile key : logging_level                          |
+-------------------------+-----------------------------------------------------------+
| --logging-configfile    | file of configuration for python logging                  |
|                         |                                                           |
|                         | * default :                                               |
|                         | * configfile key : logging_configfile                     |
+-------------------------+-----------------------------------------------------------+

.. warning::

    TODO miss available option for **--scanner-configfile**


Define a new scenario
---------------------

Each scenario have to inherit from **powerscan_scenario.Scenario**.

::

    # module.path.myscenario.py

    from powerscan_scenario.scenario import Scenario


    class MyScenario(Scenario):
        version = '1.0.0'
        label = 'My scenario'
        sequence = 1

    //
    # setup.py
    setup(
        ...
        entry_points={
            'powerscan_scenario.scenario': [
                'myscenario=module.path.myscenario:MyScenario',
            ],
        }
    )

.. note::

    The name of the entry point is the code of the scenario, This code is the primary key
    of the table **scenario**

These attributes are saved in the table **scenario**, and are required

+----------------------+-----------------------------------------------------------+
| Attribute            | Description                                               |
+======================+===========================================================+
| version              | current version of the scenario                           |
+----------------------+-----------------------------------------------------------+
| label                | label of the scenario display on the scaner screen max 16 |
+----------------------+-----------------------------------------------------------+
| sequence             | Order the scenario in the available scenario list (100)   |
+----------------------+-----------------------------------------------------------+
| dev                  | Boolean if **True** the scenario will be not displayed in |
|                      | the menu of the available scenarios list.                 |
+----------------------+-----------------------------------------------------------+

Some hooks can be overwritten 

+-----------------------------------------+--------------------------------------------------------------+
| Method                                  | Description                                                  |
+=========================================+==============================================================+
| create_models (SQLAbase)                | * SQLAbase : The Base class of SQLAlchemy to define a Model. |
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
        sequence = 1

        @step()
        def foo(self, session, scanner, entry):
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
| name                 | name of the step for this scenario, if empty the code is  |
|                      | the name of the method                                    |
+----------------------+-----------------------------------------------------------+
| is_first_step        | boolean (default False). The scenario must have got one   |
|                      | and only one step with this attribute to True value       |
|                      |                                                           |
|                      | This attribute mean that this step is the first step of   |
|                      | the scenario                                              |
+----------------------+-----------------------------------------------------------+
| is_final_step        | boolean (default False). The scenario must have got one   |
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
|                      | Each line is limited by 16 characters                     |
|                      |                                                           |
|                      | The maximum size can be decreased by the action_type      |
|                      | **confirm** or definition of buttons key                  |
+----------------------+-----------------------------------------------------------+
| buttons              | dict of buttons. The available button keys are:           |
|                      |                                                           |
|                      | * **<** or **Scenario.LeftButton**                        |
|                      | * **=** or **Scenario.MiddleButton**                      |
|                      | * **>** or **Scenario.RightButton**                       |
|                      |                                                           |
|                      | The value is the label to display, the maximum size is 5  |
|                      | for **<** and **>**, and only 4 for **=**                 |
+----------------------+-----------------------------------------------------------+
| action_type          | Defined the type of action wanted for the user            |
|                      |                                                           |
|                      | * **no_action** or **Scenario.NoAction** : Return the     |
|                      |   available scenarios                                     |
|                      | * **menu** or **Scenario.Menu** : The display is seen as  |
|                      |   a Menu of selected action by buttons                    |
|                      | * **quantity** or **Scenario.Quantity** : The display is  |
|                      |   seen as a confirmation of the quantity:                 |
|                      |                                                           |
|                      |   + **<** or **Scenario.LeftButton**: decrease the        |
|                      |     quantity                                              |
|                      |   + **=** or **Scenario.MiddleButton**: confirm the       |
|                      |     quantity                                              |
|                      |   + **>** or **Scenario.RightButton**: increase the       |
|                      |     quantity                                              |
|                      |                                                           |
|                      | * **scan** or **Scenario.Scan**: The display is seen as   |
|                      |   an ask, and the return waiting is a barcode (default)   |
|                      | * **confirm** or **Scenario.Confirm**: The display is     |
|                      |   seen as an ask and button as answer, the buttons must   |
|                      |   be defined                                              |
|                      | * **stop** or **Scenario.Stop** : Stop the current job    |
|                      |   and return the available scenario                       |
+----------------------+-----------------------------------------------------------+
| sound                | Sound played at this step:                                |
|                      |                                                           |
|                      | * **shorthight** or **Scenario.ShortHight**               |
|                      | * **shortlow** or **Scenario.ShortLow**                   |
|                      | * **longlow** or **Scenario.LongLow**                     |
|                      | * **goodread** or **Scenario.GoodRead** (default)         |
|                      | * **badread** or **Scenario.BadRead**                     |
+----------------------+-----------------------------------------------------------+


Add transition between steps
----------------------------

The decorator **powerscan_scenario.decorator.transition** is a helper to define a transition between steps

::

    from powerscan_scenario.scenario import Scenario
    from powerscan_scenario.decorator import step
    from powerscan_scenario.decorator import transition


    class MyScenario(Scenario):
        version = '1.0.0'
        label = 'My scenario'
        sequence = 1

        @step()
        def foo(self, session, scanner, entry):
            # action to do

        @step()
        def bar(self, session, scanner, entry):
            # action to do

        @transition(froms=['foo'], to='bar', sequence=1)
        def check_transition_from_foo_to_var(self, session, scanner, entry):
            return ...  # True or False

These parameters of decorator are saved in the table **transition**

+----------------------+-----------------------------------------------------------+
| parameter            | Description                                               |
+======================+===========================================================+
| name                 | name of the transition for this scenario, if empty the    |
|                      | name is the name of the method                            |
+----------------------+-----------------------------------------------------------+
| froms                | name of the steps before the transition, If the value is  |
|                      | None then all the step will be selected                   |
+----------------------+-----------------------------------------------------------+
| to                   | name of the step targeting by the transition              |
+----------------------+-----------------------------------------------------------+
| sequence             | number use to order the transition for the senario        |
+----------------------+-----------------------------------------------------------+

The parameters of step method are

+----------------------+-----------------------------------------------------------+
| parameter            | Description                                               |
+======================+===========================================================+
| session              | An instance of a SQLAlchemy Session                       |
+----------------------+-----------------------------------------------------------+
| scanner              | The instance of the scanner which have given the entry    |
|                      | data                                                      |
+----------------------+-----------------------------------------------------------+
| entry                | entry received from the scanner                           |
+----------------------+-----------------------------------------------------------+

the method must return a boolean:

* True: The transition is checked, the step targeting will be executed
* False: pass to the next transition

Existing SQLAlchemy's models
----------------------------

**powerscan_scenario.models.Scenario**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This model saved the scenario coming from the entry points ``powerscan_scenario.scenario``.

.. warning::

    This model is readonly, the data can not be modify by the ORM.

**powerscan_scenario.models.Step**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This model saved the step coming from the decorator step.

.. warning::

    This model is readonly, the data can not be modify by the ORM.

**powerscan_scenario.models.Transition**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This model saved the transition coming from the decorator transition.

.. warning::

    This model is readonly, the data can not be modify by the ORM.

**powerscan_scenario.models.Job**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This model saved the job for one scenario.

.. warning::

    This model is readonly, only the column properties (json) is available to write.

**powerscan_scenario.models.Scanner**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This model saved the scanner used for one job. The entries is created by powerscan_scenario.

.. warning::

    This model is readonly, only the column properties (json) is available to write.

Example **Put products to their location in a warehouse**
---------------------------------------------------------

::

    from powerscan_scenario.scenario import Scenario
    from powerscan_scenario.decorator import step
    from powerscan_scenario.decorator import transition
    from sqlalchemy import Column, String, Integer
    from sqlalchemy.orm import relationship
    from .api import get_data, send_data


    class PutProductInLocation(Scenario):
        version = '1.0.0'
        label = 'Move products'
        sequence = 100
        stop_code = '.....'

        def create_models(self, SQLAbase):

            class ProductLocation(SQLAbase):
                __tablename__ = "product_location"

                job_id = Column(Integer, nullable=False, ForeignKey('job.id')
                job = relationship('Job')
                product = Column(String, nullable=False, primary_key=True)
                location = Column(String, nullable=False)
                location_label = Column(String, nullable=False)
                quantity = Column(Integer)
                quantity_count = Column(Integer, default=0)

            self.ProductLocation = ProductLocation

        def initialize_job(self, session, job):
            for (product, location, location_label, quantity) in get_data():
                session.add(self.ProductLocation(
                    job=job, product=product, location=location, 
                    location_label=location_label, quantity=quantity))

        def release_job(self, session, job):
            query = session.query([self.ProductLocation]).filter_by(job=job)
            send_data([
                (x.product, x.location, x.quantity_count)
                for x in query.filter_by(job=job).all()])

            query.delete()

        @step(is_first_step=True)
        def scan_product(self, session, scanner, entry):
            if entry:
                # come from step scan_location
                query = session.query([self.ProductLocation])
                query = query.filter(self.ProductLocation.job == scanner.job)
                query = query.filter(self.ProductLocation.product == scanner.properties['product'])
                query = query.filter(self.ProductLocation.location == entry)
                query = query.filter(self.ProductLocation.quantity_count < self.ProductLocation.quantity)
                line = query.first()
                line.quantity_count += 1

            scanner.properties = {'location_label': '', 'product': '', location: ''}
            return {
                'display': ['Scan a product'],
            }

        @step(is_first_step=True)
        def scan_another_product(self, session, scanner, entry):
            return {
                'display': ['Scan a product'],
                'sound': self.BadRead,
            }

        @step()
        def scan_location(self, session, scanner, entry):
            sound = self.BadRead
            if not scanner.properties['location_label']:
                query = session.query([self.ProductLocation])
                query = query.filter(self.ProductLocation.job == scanner.job)
                query = query.filter(self.ProductLocation.product == entry)
                query = query.filter(self.ProductLocation.quantity_count < self.ProductLocation.quantity)
                line = query.first()

                scanner.properties.update({'location_label': line.location_label, location: line.location, 'product': entry})
                sound = self.GoodRead

            return {
                'display': ['Scan the location', scanner.properties['location_label']],
                'sound': sound,
            }

        @step()
        def stop(self, session, scanner, entry):
            return {'action_type': cls.Stop}

        @transition(froms=['scan_product'], to='stop', sequence=1)
        def transition_stop(self, session, scanner, entry):
            return entry == self.stop_code

        @transition(froms=['scan_product', 'scan_another_product'], to='scan_location', sequence=2)
        def transition_product_ok(self, session, scanner, entry):
            query = session.query([self.ProductLocation])
            query = query.filter(self.ProductLocation.job == scanner.job)
            query = query.filter(self.ProductLocation.product == entry)
            query = query.filter(self.ProductLocation.quantity_count < self.ProductLocation.quantity)
            return query.count() > 0

        @transition(froms=['scan_product', 'scan_another_product'], to='scan_another_product', sequence=3)
        def transition_product_ko(self, session, scanner, entry):
            return True

        @transition(froms=['scan_location'], to='scan_product', sequence=1)
        def transition_location_ok(self, session, scanner, entry):
            return scanner.properties['location'] == entry

        @transition(froms=['scan_location'], to='scan_location', sequence=2)
        def transition_product_ko(self, session, scanner, entry):
            return True

Author
------

Jean-Sébastien Suzanne

CHANGELOG
---------

1.0.0 (not released)
~~~~~~~~~~~~~~~~~~~~
