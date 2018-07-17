# This file is a part of the powerscan_scenario project
#
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
import os
import sys
from setuptools import setup, find_packages


if sys.version_info < (3, 4):
    sys.stderr.write("This package requires Python 3.4 or newer. "
                     "Yours is " + sys.version + os.linesep)
    sys.exit(1)

requires = [
    'sqlalchemy',
    'sqlalchemy-utils',
    'argparse',
    'alembic',
]

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst'), 'r', encoding='utf-8') as readme:
    README = readme.read()

setup(
    name="powerscan_scenario",
    version='0.1.0',
    author="Jean-Sébastien Suzanne",
    author_email="jssuzanne@anybox.fr",
    description="Scenario engine for datalogic scanner",
    license="MPL2",
    long_description=README,
    url="https://github.com/anybox/powerscan_scenario",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=requires,
    tests_require=requires + ['nose'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
    ],
    entry_points={
        'console_scripts': [
            'powerscan_scenario=powerscan_scenario.scripts:powerscan_scenario',
            'powerscan_config=powerscan_scenario.scripts:powerscan_config',
        ],
        'powerscan_scenario.argparse': [],
        'powerscan_config.argparse': [],
        'powerscan_scenario.scenario': [],
    },
    extras_require={},
)
