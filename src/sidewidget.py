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
    gi.require_version('Gtk', '3.0')
    gi.require_version('GObject', '2.0')
except Exception as e:
    print(e)
    exit(1)
from gi.repository import Gtk
from gi.repository import GObject


class SideWidget(Gtk.ListBoxRow):
    __gsignals__ = {
        'clicked': (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE,
                         (object,)),
    }

    def __init__(self, text, iconname='face-angel'):
        Gtk.ListBoxRow.__init__(self)
        self.set_name('sidewidget')

        box = Gtk.Box(Gtk.Orientation.HORIZONTAL, 5)
        self.add(box)

        self.image = Gtk.Image.new_from_icon_name(iconname, Gtk.IconSize.BUTTON)
        box.pack_start(self.image, True, True, 0)

        self.label = Gtk.Label(text)
        self.label.set_alignment(0, 0.5)
        box.pack_start(self.label, True, True, 5)

        self.stack = None

    def set_text(text):
        self.label.set_text(text)

    def set_stack(self, stack):
        self.stack = stack
    
    def get_stack(self):
        return self.stack