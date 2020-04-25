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
