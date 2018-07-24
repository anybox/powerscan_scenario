# This file is a part of the powerscan_scenario project
#
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
import serial
from .common import (LF, CR, ESC, ACTION_MENU, ACTION_CONFIRM, ACTION_STOP,
                     ACTION_SCAN, NO_ACTION, ACTION_QUANTITY, SOUND_SHORTHIGHT,
                     SOUND_SHORTLOW, SOUND_LONGLOW, SOUND_GOODREAD,
                     SOUND_BADREAD, SOUND_WAIT, BUTTON_LEFT, BUTTON_MIDDLE,
                     BUTTON_RIGHT)
from logging import getLogger

logger = getLogger(__name__)


class ScannerBase:

    def __init__(self, serialport=None, baudrate=None):
        """
        Open a serial connection rs232 or USB

        :param serialport: serial port connected with the scanner base
        :param baudrate: connection speed with the scanner base
        """
        logger.info("Connection with scanner base: port=%r baudrate=%r",
                    serialport, baudrate)
        try:
            self.serial = serial.Serial(serialport)
            self.serial.baudrate = baudrate
            if self.serial.isOpen():
                logger.debug(
                    'The serial port has already used, force the close')
                self.close()

            self.serial.open()
        except serial.serialutil.SerialException as e:
            logger.critical(
                "Connection failed with the scanner base")
            exit(0)

    def close(self):
        """
        Close the connection with the scanner base
        """
        self.serial.sendBreak()
        self.serial.close()
        self.logger.info("The connection is closed")

    def reception(self):
        """
        Read the serial and identify which scan send data
        @return: Scanner number and message
        """
        res = self.serial.readline()
        (scanner, message) = (res[0:4], res[4:])
        message = message.replace(CR, '').replace(LF, '')
        self.logger.debug(
            "Received from the scanner base : scanner=%r, message=%r",
            scanner, message)
        return (scanner, message)

    def send(self, scanner, message):
        """
        Send to the scanner the current message by the Serial connection
        with scanner base
        :param scanner: numero du scanner
        :param message: message a envoyer
        """
        data = scanner + message
        self.logger.debug(
            "Send to the scanner (%r) the message : %r",
            scanner, message)
        self.serial.write(data)

    def format_menu(self, data, counter):
        """
        cast the data to send to be understanding by scanner for
        display a menu
        :param data: list of string to display as menu
        :param counter: position of the cursor on the menu
        """
        res = ""
        for i, m in enumerate(data):
            if i == counter:
                res += ESC + "[7m"
            elif i < counter:
                continue
            elif i > counter + 3:
                continue
            else:
                res += ESC + "[0m"

            res += m + ESC + "[1B" + ESC + "[G"

        return res

    def format_scan(self, data):
        """
        cast the data to send to be understanding by scanner for
        display an ask of scan
        :param data: list of string to display the asking
        """
        res = ""
        for m in data:
            res += ESC + "[0m" + m + ESC + "[1B" + ESC + "[G"

        return res

    def format_quantity(self, data, counter):
        """
        cast the data to send to be understanding by scanner for
        display a confirmation of quantity
        :param data: list of string to display the asking
        :param counter: quantity to display
        """
        res = ""
        for i, m in enumerate(data):
            if i > 3:
                continue

            res += ESC + "[0m" + m + ESC + "[1B" + ESC + "[G"

        res += ESC + "[7m" + str(counter).center(16)
        res += ESC + "[7m" + '-'.ljust(5) + ESC + "[0m" + " "
        res += ESC + "[7m" + 'ok'.center(4) + ESC + "[0m" + " "
        res += ESC + "[7m" + '+'.rjust(5)
        res += ESC + "[1B" + ESC + "[G"
        return res

    def format_confirm(self, data, buttons):
        """
        cast the data to send to be understanding by scanner for
        display a confirmation
        :param data: list of string to display the asking
        :param buttons: dict with the confirmation buttons
        """
        res = ""
        tmpdata = []
        tmpdata.extend(data)
        if len(data) == 1:
            tmpdata.extend(["", ""])
        elif len(data) == 2:
            tmpdata.append("")
        for i, m in enumerate(tmpdata):
            if i > 3:
                continue

            res += ESC + "[0m" + m + ESC + "[1B" + ESC + "[G"

        m = buttons.get(BUTTON_LEFT, None)
        if m is not None:
            m = str(m)[:5]
            res += ESC + "[7m" + m.ljust(5) + ESC + "[0m" + " "
        else:
            res += ESC + "[0m" + " " * 6

        m = buttons.get(BUTTON_MIDDLE, None)
        if m is not None:
            m = str(m)[:4]
            res += ESC + "[7m" + m.ljust(4) + ESC + "[0m" + " "
        else:
            res += ESC + "[0m" + " " * 5

        m = buttons.get(BUTTON_RIGHT, None)
        if m is not None:
            m = str(m)[:5]
            res += ESC + "[7m" + m.rjust(5)
        else:
            res += ESC + "[0m" + " " * 5

        res += ESC + "[1B" + ESC + "[G"
        return res

    def format_sound(self, sound):
        """
        cast the sound to send to be understanding by scanner
        :param sound: sound to play
        """
        res = ""
        if sound == SOUND_SHORTHIGHT:
            res += "[0q"
        elif sound == SOUND_SHORTLOW:
            res += "[1q"
        elif sound == SOUND_LONGLOW:
            res += "[2q"
        elif sound == SOUND_GOODREAD:
            res += "[3q"
        elif sound == SOUND_BADREAD:
            res += "[4q"
        elif sound == SOUND_WAIT:
            res += "[5q"
        else:  # SOUND_GOODREAD
            res += "[3q"

        return res

    def format(self, action_type=None, display=None, counter=None,
               buttons=None, sound=None):
        """
        cast  the display in function the action_type, counter and buttons.
        The sound is an helper for the final user

        :param action_type: Available action defined in common.py
        :param display: message to cast to send to the scanner
        :param counter: counter use to determinate the cursor
        :param buttons: dict with the buttons labels
        :param sound: sound to play with the display
        """
        res = ESC + "[2J"
        if action_type == ACTION_MENU:
            res += self.format_menu(display, counter)
        elif action_type in (ACTION_SCAN, NO_ACTION):
            res += self.format_scan(display)
        elif action_type in (ACTION_CONFIRM, ACTION_STOP):
            res += self.format_confirm(display, buttons)
        elif action_type == ACTION_QUANTITY:
            res += self.format_quantity(display, counter)

        res += ESC
        res += self.format_sound(sound)
        res += CR
        return res

    def configure_scanner(self, scanner_code, configfile):
        pass  # TODO


class ScannerBaseConsol:

    def close(self):
        logger.info('Close %r', self)

    def reception(self):
        scan = input("Scanner number : ")
        message = input("Scanner message : ")
        return (scan, message)

    def send(self, scanner_code, message):
        print("scanner code : ", scanner_code)
        print(message)

    def format(self, action_type=None, display=None, counter=None,
               buttons=None, sound=None):
        res = ""
        if action_type == ACTION_MENU:
            for pos, line in enumerate(display):
                if pos == counter:
                    res += " * : "
                else:
                    res += "   : "
                res += str(line) + '\n'
        elif action_type in (ACTION_SCAN, NO_ACTION):
            res += '\n'.join(display)
        elif action_type in (ACTION_CONFIRM, ACTION_STOP):
            res += '\n'.join(display)
            res += '\n' + str(buttons)
        elif action_type == ACTION_QUANTITY:
            res += '\n'.join(display)
            res += '\n'.join(counter)

        return res
