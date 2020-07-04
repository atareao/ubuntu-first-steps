#!/usr/bin/env python3
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
    gi.require_version('Handy', '0.0')
except Exception as e:
    print(e)
    exit(1)
from gi.repository import Gtk
from gi.repository import Handy
from comun import _
from settings import SettingRow
from utils import is_installed


class TweakPackages(Gtk.Overlay):

    def __init__(self):
        Gtk.Overlay.__init__(self)
        self.__set_repositories()
        self.__set_ui()

    def __set_repositories(self):
        self.packages = {}
        self.packages[0] = ['VLC',
                            'VLC is the VideoLAN project\'s media player.',
                            'vlc']
        self.packages[1] = ['GIMP',
                            'GIMP is an advanced picture editor',
                            'gimp']
        self.packages[2] = ['gimp-plugin-registry',
                            '',
                            'gimp-plugin-registry']
        self.packages[3] = ['gmic',
                            '',
                            'gmic']
        self.packages[4] = ['gimp-gmic',
                            '',
                            'gimp-gmic']
        self.packages[5] = ['Blender',
                            'Blender is an integrated 3d suite for modelling, \
animation, rendering, post-production, interactive creation and playback \
(games)',
                            'blender']
        self.packages[6] = ['gufw',
                            'gufw is an easy and intuitive way to manage your \
Linux firewall.',
                            'gufw']
        self.packages[7] = ['Inkscape',
                            'Inkscape is an illustration editor which has  \
everything needed to create professional-quality computer art.',
                            'inkscape']
        self.packages[8] = ['Steam',
                            'Inkscape is an illustration editor which has \
everything needed to create professional-quality computer art',
                            'steam']
        self.packages[9] = ['FileZilla',
                            'FileZilla is a complete FTP client.',
                            'filezilla']
        self.packages[10] = ['Flameshot',
                             'Powerful and simple to use screenshot software',
                             'flameshot']
        self.packages[11] = ['Sushi',
                             'Preview tool for the GNOME Shell desktop',
                             'gnome-sushi']
        self.packages[12] = ['Weather',
                             'The weather in your desktop via GNOME',
                             'gnome-weather']
        self.packages[13] = ['Geary',
                             'Geary is an open-source e-mail client for the \
Linux desktop',
                             'geary']
        self.packages[14] = ['Caffeine',
                             'Lock Screen Inhibitor',
                             'caffeine']
        self.packages[15] = ['Corebird',
                             'The Twitter application for the Linux Desktop',
                             'corebird']

    def __set_ui(self):
        handycolumn = Handy.Column()
        handycolumn.set_maximum_width(700)
        handycolumn.set_margin_top(24)
        self.add(handycolumn)

        box = Gtk.Box.new(Gtk.Orientation.VERTICAL, 5)
        handycolumn.add(box)

        label0 = Gtk.Label(_('Applications'))
        label0.set_name('special')
        label0.set_alignment(0, 0.5)
        box.add(label0)

        listbox0 = Gtk.ListBox()
        box.add(listbox0)

        self.options = {}
        for index in range(0, len(self.packages)):
            self.options[index] = Gtk.Switch()
            self.options[index].set_valign(Gtk.Align.CENTER)
            listbox0.add(SettingRow(self.packages[index][0],
                                    self.packages[index][1],
                                    self.options[index]))
            self.options[index].set_state(
                is_installed(self.packages[index][2]))

    def update(self):
        for index in range(0, len(self.packages)):
            self.options[index].set_state(
                is_installed(self.packages[index][2]))

    def set_selected(self):
        to_install = []
        to_remove = []
        for index in range(0, len(self.packages)):
            if self.options[index].get_state() is True:
                if is_installed(self.packages[index][2]) is False:
                    to_install.append(self.packages[index][2])
            else:
                if is_installed(self.packages[index][2]) is True:
                    to_remove.append(self.packages[index][2])
        return to_install, to_remove
