# This file is a part of the powerscan_scenario project
#
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.


class DecoratorException(Exception):
    pass


def step(name=None, is_first_step=False, is_final_step=False):
    def wrap(function):
        function.is_a_step = True
        function.step_definition = dict(
            name=name or function.__name__,
            is_first_step=is_first_step,
            is_final_step=is_final_step,
            method_name_on_scenario=function.__name__,
        )

        return function

    return wrap


def transition(name=None, froms=None, to=None, sequence=None):
    none_entries = []
    if not froms:
        none_entries.append('froms')

    if not to:
        none_entries.append('to')

    if sequence is None:
        none_entries.append('sequence')

    if none_entries:
        raise DecoratorException('%r must not to be None' % none_entries)

    def wrap(function):
        function.is_a_transition = True
        function.transition_definition = dict(
            name=name or function.__name__, froms=froms,
            to=to, sequence=sequence,
            method_name_on_scenario=function.__name__)

        return function

    return wrap
