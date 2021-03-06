#/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# This file is part of ubuntu-first-steps
#
# Copyright (c) 2020 Lorenzo Carbonell Cerezo <a.k.a. atareao>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE

import gi
try:
    gi.require_version('Gtk', '3.0')
    gi.require_version('Gio', '2.0')
    gi.require_version('Handy', '0.0')
except Exception as e:
    print(e)
    exit(1)
from gi.repository import Gtk
from gi.repository import Gio
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


class TweakDesktop(Gtk.Overlay):

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

        label0 = Gtk.Label(_('Custom desktop'))
        label0.set_name('special')
        label0.set_alignment(0, 0.5)
        box.add(label0)

        listbox0 = Gtk.ListBox()
        box.add(listbox0)

        self.options = {}
        for index in range(0, 2):
            self.options[index] = Gtk.Switch()
            self.options[index].set_valign(Gtk.Align.CENTER)

        icon_size = Gtk.ListStore(str, str)
        icon_size.append([_('Small'), 'small'])
        icon_size.append([_('Standard'), 'standard'])
        icon_size.append([_('Large'), 'large'])

        self.options['icon-size'] = Gtk.ComboBox.new()
        self.options['icon-size'].set_model(icon_size)
        cell1 = Gtk.CellRendererText()
        self.options['icon-size'].pack_start(cell1, True)
        self.options['icon-size'].add_attribute(cell1, 'text', 0)

        listbox0.add(SettingRow(_('Icon size'),
                                _('Set the icon size on the desktop.'),
                                self.options['icon-size']))

        listbox0.add(SettingRow(_('Hide home'),
                                _('Hide your user folder.'),
                                self.options[0]))

        listbox0.add(SettingRow(_('Hide trash'),
                                _('Hide the trash folder.'),
                                self.options[1]))

        label1 = Gtk.Label(_('Calendar'))
        label1.set_name('special')
        label1.set_alignment(0, 0.5)
        box.add(label1)

        listbox1 = Gtk.ListBox()
        box.add(listbox1)

        for index in range(2, 6):
            self.options[index] = Gtk.Switch()
            self.options[index].set_valign(Gtk.Align.CENTER)

        listbox1.add(SettingRow(_('Show week number'),
                                _('Show week number in calendar.'),
                                self.options[2]))

        listbox1.add(SettingRow(_('Hide date'),
                                _('Hide date in the watch'),
                                self.options[3]))

        listbox1.add(SettingRow(_('Show seconds'),
                                _('Show seconds in the watch'),
                                self.options[4]))

        listbox1.add(SettingRow(_('Show weekday'),
                                _('Show weekday in the watch'),
                                self.options[5]))

        label2 = Gtk.Label(_('Battery'))
        label2.set_name('special')
        label2.set_alignment(0, 0.5)
        box.add(label2)

        listbox2 = Gtk.ListBox()
        box.add(listbox2)

        self.options[6] = Gtk.Switch()
        self.options[6].set_valign(Gtk.Align.CENTER)

        listbox2.add(SettingRow(_('Show battery percentage'),
                                _('Show battery percentage.'),
                                self.options[6]))

        label3 = Gtk.Label(_('Experimental'))
        label3.set_name('special')
        label3.set_alignment(0, 0.5)
        box.add(label3)

        listbox3 = Gtk.ListBox()
        box.add(listbox3)

        self.options[7] = Gtk.Switch()
        self.options[7].set_valign(Gtk.Align.CENTER)

        listbox3.add(SettingRow(_('Enable HiDPI Fractional Scaling'),
                                _('Enable experimenal HiDPI Fractional \
Scaling.'),
                                self.options[7]))

        self.__load_default_states()

    def update(self):
        self.__load_default_states()

    def __load_default_states(self):
        settings = Gio.Settings.new(
            'org.gnome.shell.extensions.desktop-icons')

        icon_size = variant_to_value(
            settings.get_user_value('icon-size'))
        if icon_size is None:
            select_value_in_combo(self.options['icon-size'], 'small')
        else:
            select_value_in_combo(self.options['icon-size'], icon_size)

        self.options[0].set_state(variant_to_value(
            settings.get_user_value('show-home')) is False)
        self.options[1].set_state(variant_to_value(
            settings.get_user_value('show-trash')) is False)

        settings = Gio.Settings.new(
            'org.gnome.desktop.calendar')

        self.options[2].set_state(variant_to_value(
            settings.get_user_value('show-weekdate')) is True)

        settings = Gio.Settings.new(
            'org.gnome.desktop.interface')

        self.options[3].set_state(variant_to_value(
            settings.get_user_value('clock-show-date')) is False)

        self.options[4].set_state(variant_to_value(
            settings.get_user_value('clock-show-seconds')) is True)

        self.options[5].set_state(variant_to_value(
            settings.get_user_value('clock-show-weekday')) is True)

        self.options[6].set_state(variant_to_value(
            settings.get_user_value('show-battery-percentage')) is True)

        settings = Gio.Settings.new(
            'org.gnome.mutter')
        self.options[7].set_state(variant_to_value(
            settings.get_user_value('experimental-features')) is not None)

    def set_selected(self):
        settings = Gio.Settings.new(
            'org.gnome.shell.extensions.desktop-icons')

        icon_size = get_selected_value_in_combo(
            self.options['icon-size'])
        if icon_size == 'small':
            settings.reset('icon-size')
        else:
            settings.set_string('icon-size', icon_size)
        if self.options[0].get_active() is True:
            settings.set_boolean('show-home', False)
        else:
            settings.reset('show-home')
        if self.options[1].get_active() is True:
            settings.set_boolean('show-trash', False)
        else:
            settings.reset('show-trash')

        settings = Gio.Settings.new(
            'org.gnome.desktop.calendar')

        if self.options[2].get_active() is True:
            settings.set_boolean('show-weekdate', True)
        else:
            settings.reset('show-weekdate')

        settings = Gio.Settings.new(
            'org.gnome.desktop.interface')
        if self.options[3].get_active() is True:
            settings.set_boolean('clock-show-date', False)
        else:
            settings.reset('clock-show-date')
        if self.options[4].get_active() is True:
            settings.set_boolean('clock-show-seconds', True)
        else:
            settings.reset('clock-show-seconds')
        if self.options[5].get_active() is True:
            settings.set_boolean('clock-show-weekday', True)
        else:
            settings.reset('clock-show-weekday')
        if self.options[6].get_active() is True:
            settings.set_boolean('show-battery-percentage', True)
        else:
            settings.reset('show-battery-percentage')

        settings = Gio.Settings.new(
            'org.gnome.mutter')
        if self.options[7].get_active() is True:
            if os.environ.get('XDG_SESSION_TYPE') == 'x11':
                settings.set_strv('experimental-features',
                                  ['x11-randr-fractional-scaling'])
            else:
                settings.set_strv('experimental-features',
                                  ['scale-monitor-framebuffer'])
        else:
            settings.reset('experimental-features')
