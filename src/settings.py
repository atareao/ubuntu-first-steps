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
