# This file is a part of the powerscan_scenario project
#
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.

LF = chr(10)  # Line Feed
CR = chr(13)  # Carriage Return
ESC = chr(27)  # Escape

# Step action type
NO_ACTION = "no_action"
ACTION_MENU = "menu"
ACTION_QUANTITY = "quantity"
ACTION_SCAN = "scan"
ACTION_CONFIRM = "confirm"
ACTION_STOP = "stop"

# available button
BUTTON_LEFT = '<'
BUTTON_MIDDLE = '='
BUTTON_RIGHT = '>'

# available returned sound
SOUND_SHORTHIGHT = "shorthight"
SOUND_SHORTLOW = "shortlow"
SOUND_LONGLOW = "longlow"
SOUND_GOODREAD = "goodread"
SOUND_BADREAD = "badread"
SOUND_WAIT = "wait"
