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


class TweakDock(Gtk.Overlay):

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

        label = Gtk.Label(_('Custom dock'))
        label.set_name('special')
        label.set_alignment(0, 0.5)
        box.add(label)

        listbox0 = Gtk.ListBox()
        box.add(listbox0)

        self.options = {}
        for index in range(0, 3):
            self.options[index] = Gtk.Switch()
            self.options[index].set_valign(Gtk.Align.CENTER)

        dock_position = Gtk.ListStore(str, str)
        dock_position.append([_('Left'), 'LEFT'])
        dock_position.append([_('Right'), 'RIGHT'])
        dock_position.append([_('Top'), 'TOP'])
        dock_position.append([_('Bottom'), 'BOTTOM'])

        self.options['dock-position'] = Gtk.ComboBox.new()
        self.options['dock-position'].set_model(dock_position)
        cell1 = Gtk.CellRendererText()
        self.options['dock-position'].pack_start(cell1, True)
        self.options['dock-position'].add_attribute(cell1, 'text', 0)

        listbox0.add(SettingRow(_('Dock position'),
                                _('Set the dock position on the screen.'),
                                self.options['dock-position']))

        listbox0.add(SettingRow(_('Enable minimize click action'),
                                _('Minimize when clicking on a running app.'),
                                self.options[0]))

        listbox0.add(SettingRow(_('Reduce dock length'),
                                _('Reduce the dock container to icons.'),
                                self.options[1]))

        listbox0.add(SettingRow(_('Force straight corner'),
                                _('Make the borders in the dash non rounded.'),
                                self.options[2]))

        label1 = Gtk.Label('Monitor')
        label1.set_name('special')
        label1.set_alignment(0, 0.5)
        box.add(label1)

        listbox1 = Gtk.ListBox()
        box.add(listbox1)

        for index in range(3, 5):
            self.options[index] = Gtk.Switch()
            self.options[index].set_valign(Gtk.Align.CENTER)

        listbox1.add(SettingRow(_('Isolate monitors'),
                                _('Provide monitor isolation'),
                                self.options[3]))
        listbox1.add(SettingRow(_('Multi monitor'),
                                _('Enable multi monitor dock'),
                                self.options[4]))

        label2 = Gtk.Label('Show in dock')
        label2.set_name('special')
        label2.set_alignment(0, 0.5)
        box.add(label2)

        listbox2 = Gtk.ListBox()
        box.add(listbox2)

        for index in range(5, 9):
            self.options[index] = Gtk.Switch()
            self.options[index].set_valign(Gtk.Align.CENTER)

        listbox2.add(SettingRow(_('Hide applications button'),
                                _('Hide applications button'),
                                self.options[5]))
        listbox2.add(SettingRow(_('Show apps at top'),
                                _('Show application button at top'),
                                self.options[6]))
        listbox2.add(SettingRow(_('Hide favorites'),
                                _('Hide favorites apps'),
                                self.options[7]))
        listbox2.add(SettingRow(_('Hide running'),
                                _('Hide running apps'),
                                self.options[8]))

        self.__load_default_states()

    def update(self):
        self.__load_default_states()

    def __load_default_states(self):
        settings = Gio.Settings.new(
            'org.gnome.shell.extensions.dash-to-dock')

        dock_position = variant_to_value(
            settings.get_user_value('dock-position'))
        print('===', dock_position, '===')
        if dock_position is None:
            select_value_in_combo(self.options['dock-position'], 'LEFT')
        else:
            print(dock_position)
            select_value_in_combo(self.options['dock-position'], dock_position)

        self.options[0].set_state(variant_to_value(
            settings.get_user_value('click-action')) == 'minimize')
        self.options[1].set_state(variant_to_value(
            settings.get_user_value('extend-height')) is False)
        self.options[2].set_state(variant_to_value(
            settings.get_user_value('force-straight-corner')) is True)
        self.options[3].set_state(variant_to_value(
            settings.get_user_value('isolate-monitors')) is True)
        self.options[4].set_state(variant_to_value(
            settings.get_user_value('multi-monitor')) is True)
        self.options[5].set_state(variant_to_value(
            settings.get_user_value('show-show-apps-button')) is False)
        self.options[6].set_state(variant_to_value(
            settings.get_user_value('show-apps-at-top')) is True)
        self.options[7].set_state(variant_to_value(
            settings.get_user_value('show-favorites')) is False)
        self.options[8].set_state(variant_to_value(
            settings.get_user_value('show-running')) is False)

    def set_selected(self):
        settings = Gio.Settings.new(
            'org.gnome.shell.extensions.dash-to-dock')
        dock_position = get_selected_value_in_combo(
            self.options['dock-position'])
        if dock_position == 'LEFT':
            settings.reset('dock-position')
        else:
            print(dock_position)
            settings.set_string('dock-position', dock_position)
        if self.options[0].get_active() is True:
            settings.set_string('click-action', 'minimize')
        else:
            settings.reset('click-action')
        if self.options[1].get_active() is True:
            settings.set_boolean('extend-height', False)
        else:
            settings.reset('extend-height')
        if self.options[2].get_active() is True:
            settings.set_boolean('force-straight-corner', True)
        else:
            settings.reset('force-straight-corner')
        if self.options[3].get_active() is True:
            settings.set_boolean('isolate-monitors', True)
        else:
            settings.reset('isolate-monitors')
        if self.options[4].get_active() is True:
               settings.set_boolean('multi-monitor', True)
        else:
            settings.reset('multi-monitor')
        if self.options[5].get_active() is False:
            settings.reset('show-show-apps-button')
        else:
            settings.set_boolean('show-show-apps-button', False)
            
        if self.options[6].get_active() is True:
            settings.set_boolean('show-apps-at-top', True)
        else:
            settings.reset('show-apps-at-top')
        if self.options[7].get_active() is False:
            settings.reset('show-favorites')
        else:
            settings.set_boolean('show-favorites', False)
        if self.options[8].get_active() is False:
            settings.reset('show-running')
        else:
            settings.set_boolean('show-running', False)
        self.__load_default_states()
