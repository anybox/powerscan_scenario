# This file is a part of the powerscan_scenario project
#
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from unittest import TestCase
from ..scannerbase import TestingScannerBase
from ..common import (NO_ACTION, BUTTON_LEFT, BUTTON_MIDDLE, BUTTON_RIGHT,
                      SOUND_SHORTHIGHT, SOUND_SHORTLOW, SOUND_LONGLOW,
                      SOUND_GOODREAD, SOUND_BADREAD, SOUND_WAIT)


class TestScannerBase(TestCase):

    def test_format(self):
        base = TestingScannerBase()
        res = base.format(action_type=NO_ACTION, display=['Hello World !!!'])
        self.assertEqual(
            res, '\x1b[2J\x1b[0mHello World !!!\x1b[1B\x1b[G\x1b[3q\r')

    def test_format_menu(self):
        base = TestingScannerBase()
        data = ['test line 1', 'test line 2', 'test line 3', 'test line 4',
                'test line 5', 'test line 6', 'test line 7', 'test line 8']
        counter = 2
        self.assertEqual(
            base.format_menu(data, counter),
            '\x1b[7mtest line 3\x1b[1B\x1b[G\x1b[0mtest line 4\x1b[1B\x1b[G'
            '\x1b[0mtest line 5\x1b[1B\x1b[G\x1b[0mtest line 6\x1b[1B\x1b[G')

    def test_format_scan(self):
        base = TestingScannerBase()
        data = ['test line 1', 'test line 2', 'test line 3', 'test line 4']
        self.assertEqual(
            base.format_scan(data),
            '\x1b[0mtest line 1\x1b[1B\x1b[G\x1b[0mtest line 2\x1b[1B\x1b[G'
            '\x1b[0mtest line 3\x1b[1B\x1b[G\x1b[0mtest line 4\x1b[1B\x1b[G')

    def test_format_quantity(self):
        base = TestingScannerBase()
        data = ['test line 1', 'test line 2', 'test line 3', 'test line 4']
        counter = 11
        self.assertEqual(
            base.format_quantity(data, counter),
            '\x1b[0mtest line 1\x1b[1B\x1b[G\x1b[0mtest line 2\x1b[1B\x1b[G'
            '\x1b[0mtest line 3\x1b[1B\x1b[G\x1b[0mtest line 4\x1b[1B\x1b[G'
            '\x1b[7m       11       \x1b[7m-    \x1b[0m \x1b[7m ok \x1b[0m '
            '\x1b[7m    +\x1b[1B\x1b[G'
        )

    def test_format_confirm_1_line(self):
        base = TestingScannerBase()
        data = ['test line 1']
        buttons = {BUTTON_LEFT: 'l', BUTTON_MIDDLE: 'm', BUTTON_RIGHT: 'r'}
        self.assertEqual(
            base.format_confirm(data, buttons),
            '\x1b[0mtest line 1\x1b[1B\x1b[G\x1b[0m\x1b[1B\x1b[G\x1b[0m\x1b[1B'
            '\x1b[G\x1b[7ml    \x1b[0m \x1b[7mm   \x1b[0m \x1b[7m    r\x1b[1B'
            '\x1b[G'
        )

    def test_format_confirm_1_line_without_buttons(self):
        base = TestingScannerBase()
        data = ['test line 1']
        buttons = {}
        self.assertEqual(
            base.format_confirm(data, buttons),
            '\x1b[0mtest line 1\x1b[1B\x1b[G\x1b[0m\x1b[1B\x1b[G\x1b[0m\x1b[1B'
            '\x1b[G\x1b[0m      \x1b[0m     \x1b[0m     \x1b[1B\x1b[G'
        )

    def test_format_confirm_2_lines(self):
        base = TestingScannerBase()
        data = ['test line 1', 'test line 2']
        buttons = {BUTTON_LEFT: 'l', BUTTON_MIDDLE: 'm', BUTTON_RIGHT: 'r'}
        self.assertEqual(
            base.format_confirm(data, buttons),
            '\x1b[0mtest line 1\x1b[1B\x1b[G\x1b[0mtest line 2\x1b[1B\x1b[G'
            '\x1b[0m\x1b[1B\x1b[G\x1b[7ml    \x1b[0m \x1b[7mm   \x1b[0m \x1b'
            '[7m    r\x1b[1B\x1b[G'
        )

    def test_format_confirm_3_lines(self):
        base = TestingScannerBase()
        data = ['test line 1', 'test line 2', 'test line 3']
        buttons = {BUTTON_LEFT: 'l', BUTTON_MIDDLE: 'm', BUTTON_RIGHT: 'r'}
        self.assertEqual(
            base.format_confirm(data, buttons),
            '\x1b[0mtest line 1\x1b[1B\x1b[G\x1b[0mtest line 2\x1b[1B\x1b[G'
            '\x1b[0mtest line 3\x1b[1B\x1b[G\x1b[7ml    \x1b[0m \x1b'
            '[7mm   \x1b[0m \x1b[7m    r\x1b[1B\x1b[G'
        )

    def test_format_sound_shorthight(self):
        base = TestingScannerBase()
        sound = SOUND_SHORTHIGHT
        self.assertEqual(base.format_sound(sound), '[0q')

    def test_format_sound_shortlow(self):
        base = TestingScannerBase()
        sound = SOUND_SHORTLOW
        self.assertEqual(base.format_sound(sound), '[1q')

    def test_format_sound_longlow(self):
        base = TestingScannerBase()
        sound = SOUND_LONGLOW
        self.assertEqual(base.format_sound(sound), '[2q')

    def test_format_sound_goodread(self):
        base = TestingScannerBase()
        sound = SOUND_GOODREAD
        self.assertEqual(base.format_sound(sound), '[3q')

    def test_format_sound_goodread_default(self):
        base = TestingScannerBase()
        sound = None
        self.assertEqual(base.format_sound(sound), '[3q')

    def test_format_sound_badread(self):
        base = TestingScannerBase()
        sound = SOUND_BADREAD
        self.assertEqual(base.format_sound(sound), '[4q')

    def test_format_sound_wait(self):
        base = TestingScannerBase()
        sound = SOUND_WAIT
        self.assertEqual(base.format_sound(sound), '[5q')
