#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# start-here is an application that helps you to tweak Ubuntu,
# after install a new version of Ubuntu. First stepts with Ubuntu.
#
# Copyright © 2019  Lorenzo Carbonell (aka atareao)
# <lorenzo.carbonell.cerezo at gmail dotcom>
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
    gi.require_version('GObject', '2.0')
    gi.require_version('Handy', '0.0')
except Exception as e:
    print(e)
    exit(1)
from gi.repository import GObject
from gi.repository import Handy


class SettingRow(Handy.ActionRow):

    def __init__(self, title, subtitle, widget):
        Handy.ActionRow.__init__(self)

        self.__populate_widget(title, subtitle, widget)

    def __populate_widget(self, title, subtitle, widget):
        self.set_title(title)
        self.set_subtitle(subtitle)
        self.add_action(widget)


class SettingExpanderRow(Handy.ExpanderRow):
    toggled = GObject.Property(type=bool, default=False)

    def __init__(self, title, subtitle):
        Handy.ExpanderRow.__init__(self)

        self.__populate_widget(title, subtitle)

    def __populate_widget(self, title, subtitle):
        self.set_title(title)
        self.set_subtitle(subtitle)

        # Hackish solution until libhandy have a property for that
        expander_toggled_btn = self.get_children()[0].get_children()[3]
        expander_toggled_btn.bind_property("active", self, "toggled",
                                           GObject.BindingFlags.BIDIRECTIONAL)
