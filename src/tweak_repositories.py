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
import glob
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


class TweakRepositories(Gtk.Overlay):

    def __init__(self):
        Gtk.Overlay.__init__(self)
        self.__set_repositories()
        self.__set_ui()

    def __set_repositories(self):
        self.ppas = {}
        self.ppas[0] = ['LibreOffice Fresh',
                        'Latest stable release of the LibreOffice office \
suite',
                        'libreoffice/ppa']
        self.ppas[1] = ['Grub Customizer',
                        'If you want to customize the GRUB screen of your \
system',
                        'danielrichter2007/grub-customizer']
        self.ppas[2] = ['WebUpd8',
                        'PPA containing a lot of useful applications that are \
mostly updated to their latest versions',
                        'nilarimogard/webupd8']
        self.ppas[3] = ['FreeCAD',
                        'Latest stable release of FreeCAD',
                        'freecad-maintainers/freecad-stable']
        self.ppas[4] = ['Inkscape',
                        'Latest stable release of Inkscape',
                        'inkscape.dev/stable']
        self.ppas[5] = ['OBS Studio',
                        'Latest stable release of OBS Studio',
                        'obsproject/obs-studio']
        self.ppas[6] = ['Handbrake',
                        'Latest stable release of Handbrake',
                        'stebbins/handbrake-releases']
        self.ppas[7] = ['Lutris',
                        'Latest stable release of Lutris',
                        'lutris-team/lutris']
        self.ppas[8] = ['Gimp',
                        'Latest stable release of Gimp',
                        'otto-kesselgulasch/gimp']
        self.ppas[9] = ['Blender',
                        'Latest stable release of Blender',
                        'thomas-schiex/blender']
        self.ppas[10] = ['Audacity',
                         'Unofficial. Most recent relase version of Audacity',
                         'buntuhandbook1/audacity']

    def __set_ui(self):
        handycolumn = Handy.Column()
        handycolumn.set_maximum_width(700)
        handycolumn.set_margin_top(24)
        self.add(handycolumn)

        box = Gtk.Box.new(Gtk.Orientation.VERTICAL, 5)
        handycolumn.add(box)

        label0 = Gtk.Label(_('Repositories'))
        label0.set_name('special')
        label0.set_alignment(0, 0.5)
        box.add(label0)

        listbox0 = Gtk.ListBox()
        box.add(listbox0)

        self.options = {}
        installed_ppas = self.get_installed_ppas()
        for index in range(0, len(self.ppas)):
            self.options[index] = Gtk.Switch()
            self.options[index].set_valign(Gtk.Align.CENTER)
            listbox0.add(SettingRow(self.ppas[index][0],
                                    self.ppas[index][1],
                                    self.options[index]))
            self.options[index].set_state(
                self.ppas[index][2] in installed_ppas)

    def update(self):
        installed_ppas = self.get_installed_ppas()
        for index in range(0, len(self.ppas)):
            self.options[index].set_state(
                self.ppas[index][2] in installed_ppas)

    def set_selected(self):
        to_install = []
        to_remove = []
        installed_ppas = self.get_installed_ppas()
        for index in range(0, len(self.ppas)):
            if self.options[index].get_state() is True:
                if self.ppas[index][2] not in installed_ppas:
                    to_install.append(self.ppas[index][2])
            else:
                if self.ppas[index][2] in installed_ppas:
                    to_remove.append(self.ppas[index][2])
        return to_install, to_remove

    def get_installed_ppas(self):
        ppas = []
        ppa_folder = '/etc/apt/sources.list.d'
        for ppa in glob.glob(os.path.join(ppa_folder, '*.list')):
            filename, extension = os.path.splitext(
                os.path.os.path.basename(ppa))
            ppa = '-'.join(filename.split('-')[:-1]).replace('-ubuntu', '')
            if ppa.count('-') > 1:
                data = ppa.split('-')
                ppa = '-'.join(data[:-1]) + '/' + data[-1]
            else:
                ppa = ppa.replace('-', '/')
            if ppa is not None and len(ppa) > 0:
                ppas.append(ppa)
        return ppas
