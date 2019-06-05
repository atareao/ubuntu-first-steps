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
import glob
import json
import mimetypes
import urllib
import subprocess
import comun
from comun import _
from sidewidget import SideWidget
from utils import get_desktop_environment
from settings import SettingRow
from utils import variant_to_value, select_value_in_combo
from utils import get_selected_value_in_combo


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
                            'Blender is an integrated 3d suite for modelling, animation, rendering, post-production, interactive creation and playback (games)',
                            'blender']
        self.packages[6] = ['gufw',
                            'gufw is an easy and intuitive way to manage your Linux firewall.',
                            'gufw']
        self.packages[7] = ['Inkscape',
                            'Inkscape is an illustration editor which has everything needed to create professional-quality computer art.',
                            'inkscape']
        self.packages[8] = ['Steam',
                            'Inkscape is an illustration editor which has everything needed to create professional-quality computer art',
                            'steam']
        self.packages[9] = ['FileZilla',
                            'FileZilla is a complete FTP client.',
                            'filezilla']
        self.packages[10] = ['Flameshot',
                             'Powerful and simple to use screenshot software',
                             'flameshot']

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
                self.is_installed(self.packages[index][2]))

    def set_selected(self):
        to_install = []
        installed_ppas = self.get_installed_ppas()
        for index in range(0, len(self.packages)):
            if self.options[index].get_state() is True and \
                    self.is_installed(self.packages[index][2]) is False:
                to_install.append(self.packages[index][2])
        return to_install

    def is_installed(self, package):
        args = ['dpkg-query', '-W', '-f=\'${Status}\'', package]
        proc = subprocess.Popen(args,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.DEVNULL)
        return proc.stdout.read().decode() == '\'install ok installed\''