#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# mainwindow.py
#
# This file is part of yoaup (YouTube Audio Player)
#
# Copyright (C) 2017
# Lorenzo Carbonell Cerezo <lorenzo.carbonell.cerezo@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import gi
try:
    gi.require_version('Gtk', '3.0')
    gi.require_version('Gdk', '3.0')
    gi.require_version('Gio', '2.0')
    gi.require_version('GLib', '2.0')
    gi.require_version('GObject', '2.0')
    gi.require_version('GdkPixbuf', '2.0')
    gi.require_version('Notify', '0.7')
except Exception as e:
    print(e)
    exit(1)
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Gio
from gi.repository import GLib
from gi.repository import GObject
from gi.repository import GdkPixbuf
from gi.repository import Notify
from gi.repository import Handy
import os
import json
import mimetypes
import urllib
import comun
from comun import _
from sidewidget import SideWidget
from utils import get_desktop_environment
from settings import SettingRow
from utils import variant_to_value, select_value_in_combo
from utils import get_selected_value_in_combo


class TweakPrivacy(Gtk.Overlay):

    def __init__(self):
        Gtk.Overlay.__init__(self)
        self.__set_ui()

    def __set_ui(self):
        handycolumn = Handy.Column()
        handycolumn.set_maximum_width(700)
        handycolumn.set_margin_top(24)
        self.add(handycolumn)

        box = Gtk.Box.new(Gtk.Orientation.VERTICAL, 5)
        handycolumn.add(box)

        label0 = Gtk.Label(_('Peripherals'))
        label0.set_name('special')
        label0.set_alignment(0, 0.5)
        box.add(label0)

        listbox0 = Gtk.ListBox()
        box.add(listbox0)

        self.options = {}
        for index in range(0, 3):
            self.options[index] = Gtk.Switch()
            self.options[index].set_valign(Gtk.Align.CENTER)

        listbox0.add(SettingRow(_('Disable camera'),
                                _('Avoid applications to use the camera.'),
                                self.options[0]))
        listbox0.add(SettingRow(_('Disable microphone'),
                                _('Avoid applications to use the microphone.'),
                                self.options[1]))
        listbox0.add(SettingRow(_('Disable sound outp'),
                                _('Avoid applications to play sound.'),
                                self.options[2]))

        label1 = Gtk.Label(_('Identity'))
        label1.set_name('special')
        label1.set_alignment(0, 0.5)
        box.add(label1)

        listbox1 = Gtk.ListBox()
        box.add(listbox1)

        self.options[3] = Gtk.Switch()
        self.options[3].set_valign(Gtk.Align.CENTER)

        listbox1.add(SettingRow(_('Hide identity'),
                                _('Hide personal information.'),
                                self.options[3]))

        label2 = Gtk.Label(_('Remember'))
        label2.set_name('special')
        label2.set_alignment(0, 0.5)
        box.add(label2)

        listbox2 = Gtk.ListBox()
        box.add(listbox2)

        for index in range(4, 8):
            self.options[index] = Gtk.Switch()
            self.options[index].set_valign(Gtk.Align.CENTER)

        listbox2.add(SettingRow(_('Forget application usage'),
                                _('Forget application usage.'),
                                self.options[4]))

        listbox2.add(SettingRow(_('Forget recent files'),
                                _('Forget recent files.'),
                                self.options[5]))

        listbox2.add(SettingRow(_('Remove temporary files'),
                                _('Remove old temporary files automatically.'),
                                self.options[6]))

        listbox2.add(SettingRow(_('Remove trash files'),
                                _('Remove old trash files automatically.'),
                                self.options[7]))

        label3 = Gtk.Label(_('Statistics'))
        label3.set_name('special')
        label3.set_alignment(0, 0.5)
        box.add(label3)

        listbox3 = Gtk.ListBox()
        box.add(listbox3)

        for index in range(8, 10):
            self.options[index] = Gtk.Switch()
            self.options[index].set_valign(Gtk.Align.CENTER)

        listbox3.add(SettingRow(_('Send technical problems'),
                                _('Send technical problems.'),
                                self.options[8]))

        listbox3.add(SettingRow(_('Send software usage'),
                                _('Send softwarew usage statistics.'),
                                self.options[9]))

        self.__load_default_states()

    def __load_default_states(self):
        settings = Gio.Settings.new(
            'org.gnome.desktop.privacy')
        self.options[0].set_state(variant_to_value(
            settings.get_user_value('disable-camera')) is True)
        self.options[1].set_state(variant_to_value(
            settings.get_user_value('disable-microphone')) is True)
        self.options[2].set_state(variant_to_value(
            settings.get_user_value('disable-sound-output')) is True)
        self.options[3].set_state(variant_to_value(
            settings.get_user_value('hide-identity')) is True)
        self.options[4].set_state(variant_to_value(
            settings.get_user_value('remember-app-usage')) is False)
        self.options[5].set_state(variant_to_value(
            settings.get_user_value('remember-recent-files')) is False)
        self.options[6].set_state(variant_to_value(
            settings.get_user_value('remove-old-temp-files')) is True)
        self.options[7].set_state(variant_to_value(
            settings.get_user_value('remove-old-trash-files')) is True)
        self.options[8].set_state(variant_to_value(
            settings.get_user_value('report-technical-problems')) is True)
        self.options[9].set_state(variant_to_value(
            settings.get_user_value('send-software-usage-stats')) is True)

    def set_selected(self):
        settings = Gio.Settings.new(
            'org.gnome.desktop.privacy')
        if self.options[0].get_active() is True:
            settings.set_boolean('disable-camera', True)
        else:
            settings.reset('disable-camera')
        if self.options[1].get_active() is True:
            settings.set_boolean('disable-microphone', True)
        else:
            settings.reset('disable-microphone')
        if self.options[2].get_active() is True:
            settings.set_boolean('disable-sound-output', True)
        else:
            settings.reset('disable-sound-output')
        if self.options[3].get_active() is True:
            settings.set_boolean('hide-identity', True)
        else:
            settings.reset('hide-identity')
        if self.options[4].get_active() is True:
            settings.set_boolean('remember-app-usage', False)
        else:
            settings.reset('remember-app-usage')
        if self.options[5].get_active() is True:
            settings.set_boolean('remember-recent-files', False)
        else:
            settings.reset('remember-recent-files')
        if self.options[6].get_active() is True:
            settings.set_boolean('remove-old-temp-files', True)
        else:
            settings.reset('remove-old-temp-files')
        if self.options[7].get_active() is True:
            settings.set_boolean('remove-old-trash-files', True)
        else:
            settings.reset('remove-old-trash-files')
        if self.options[8].get_active() is True:
            settings.set_boolean('report-technical-problems', True)
        else:
            settings.reset('report-technical-problems')
        if self.options[9].get_active() is True:
            settings.set_boolean('send-software-usage-stats', True)
        else:
            settings.reset('send-software-usage-stats')
