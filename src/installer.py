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
    gi.require_version('GLib', '2.0')
    gi.require_version('Vte', '2.91')
except Exception as e:
    print(e)
    exit(1)
from gi.repository import Gtk
from gi.repository import GLib
from gi.repository import Vte
import os
import sys
import time
import comun
import json
from comun import _
from doitinbackground import DoItInBackground
import utils

MARGIN = 5


class SmartTerminal(Vte.Terminal):
    def __init__(self, parent):
        Vte.Terminal.__init__(self)
        self.parent = parent
        self.diib = None

    def execute(self, commands):
        self.diib = DoItInBackground(self, commands)
        self.diib.connect('started', self.parent.start)
        self.diib.connect('done_one', self.parent.increase)
        self.diib.connect('ended', self.parent.end)
        self.diib.connect('stopped', self.parent.stopped)
        self.diib.start()

    def stop(self):
        if self.diib is not None:
            self.diib.stop()


class Installer(Gtk.Dialog):  # needs GTK, Python, Webkit-GTK
    # def __init__(self, ppas_to_install, ppas_to_remove, apps_to_install,
    #              apps_to_remove):
    def __init__(self, actions):
        Gtk.Dialog.__init__(self)
        self.set_title( _('Add ppa repository'))
        self.set_modal(True)
        self.set_destroy_with_parent(True)
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.set_icon_from_file(comun.ICON)
        self.set_size_request(600, 50)

        actions = json.loads(actions)
        self.ppas_to_install = actions['ppas_to_install']
        self.ppas_to_remove = actions['ppas_to_remove']
        self.apps_to_install = actions['apps_to_install']
        self.apps_to_remove = actions['apps_to_remove']

        box = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 10)
        box.set_border_width(5)
        self.get_content_area().add(box)

        grid = Gtk.Grid()
        grid.set_column_spacing(MARGIN)
        grid.set_row_spacing(MARGIN)
        box.add(grid)

        self.label = Gtk.Label.new('')
        self.label.set_halign(Gtk.Align.START)
        grid.attach(self.label, 0, 1, 2, 1)

        self.progressbar = Gtk.ProgressBar()
        grid.attach(self.progressbar, 0, 2, 4, 1)

        expander = Gtk.Expander()
        expander.connect('notify::expanded', self.on_expanded)
        grid.attach(expander, 0, 3, 4, 4)

        alignment = Gtk.Alignment()
        # alignment.set_padding(1, 0, 2, 2)
        alignment.props.xscale = 1
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        self.terminal = SmartTerminal(self)
        scrolledwindow.add(self.terminal)
        alignment.add(scrolledwindow)
        expander.add(alignment)

        hbox = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 5)
        grid.attach(hbox, 0, 8, 4, 1)

        self.button_cancel = Gtk.Button.new_with_label(_('Cancel'))
        self.button_cancel.connect('clicked', self.on_button_cancel_clicked)
        hbox.pack_start(self.button_cancel, False, False, 0)

        self.is_added = False
        self.value = 0.0
        self.is_installing = False
        self.show_all()
        self.progressbar.set_visible(False)
        self.label.set_visible(False)
        expander.set_expanded(True)
        time.sleep(1)
        self.start_installation()

    def end(self, anobject, ok, *args):
        self.is_installing = False
        self.button_cancel.set_label(_('Exit'))
        if ok is True:
            kind = Gtk.MessageType.INFO
            message = _('Installation completed!')
        else:
            kind = Gtk.MessageType.ERROR
            message = _('Installation NOT completed!')
        dialog = Gtk.MessageDialog()
        dialog.set_markup(message)
        dialog.set_property('message_type', kind)
        dialog.add_button(_('Ok'), Gtk.ButtonsType.OK)
        dialog.run()
        dialog.destroy()

    def stopped(self, anobject, *args):
        self.is_installing = False
        self.button_cancel.set_label(_('Exit'))
        self.destroy()

    def start(self, anobject, total, *args):
        self.is_installing = True
        self.label.set_visible(True)
        self.progressbar.set_visible(True)
        self.value = 0.0
        self.max_value = total

    def increase(self, anobject, command, *args):
        GLib.idle_add(self.label.set_text, _('Executing: %s') % command)
        self.value += 1.0
        fraction = self.value / self.max_value
        print(fraction)
        GLib.idle_add(self.progressbar.set_fraction, fraction)

    def decrease(self):
        self.value -= 1.0
        fraction = self.value / self.max_value
        GLib.idle_add(self.progressbar.set_fraction, fraction)

    def on_expanded(self, widget, data):
        if widget.get_property('expanded') is True:
            self.set_size_request(600, 300)
        else:
            self.set_size_request(600, 50)
            self.resize(600, 50)

    def on_button_cancel_clicked(self, button):
        if self.is_installing:
            dialog = Gtk.MessageDialog()
            dialog.set_markup(_('Do you want to stop the installation?'))
            dialog.set_property('message-type', Gtk.MessageType.INFO)
            dialog.add_button(_('Ok'), Gtk.ResponseType.OK)
            dialog.add_button(_('Cancel'), Gtk.ResponseType.CANCEL)
            ans = dialog.run()
            if dialog.run() == Gtk.ResponseType.OK:
                GLib.idle_add(dialog.hide)
                self.terminal.stop()
            GLib.idle_add(dialog.destroy)

    def show_info(self):
        self.progressbar.set_visible(True)
        self.label.set_visible(True)

    def start_installation(self):
        commands = []
        for ppa in self.ppas_to_install:
            commands.append('add-apt-repository -y {}'.format(ppa))
        for ppa in self.ppas_to_remove:
            commands.append('add-apt-repository -y -r {}'.format(ppa))
        if len(commands) > 0:
            commands.append('apt-get update')
            commands.append('apt-get upgrade')
        if len(self.apps_to_install) > 0:
            apps = ' '.join(self.apps_to_install)
            commands.append('apt-get -y install {}'.format(apps))
        if len(self.apps_to_remove) > 0:
            apps = ' '.join(self.apps_to_remove)
            commands.append('apt-get -y remove {}'.format(apps))
        print(commands)
        self.terminal.execute(commands)


def main(args):
    if os.geteuid() != 0:
        dialog = Gtk.MessageDialog()
        dialog.set_markup(_('You must be root to run this tool'))
        dialog.set_property('message-type', Gtk.MessageType.ERROR)
        dialog.add_button(_('Ok'), Gtk.ResponseType.OK)
        dialog.run()
        return
    installer = Installer(args)
    installer.run()
    installer.destroy()


if __name__ == '__main__':
    actions = {'ppas_to_install': ['ppa:atareao/atareao'],
               'ppas_to_remove': [],
               'apps_to_install': ['my-weather-indicator'],
               'apps_to_remove': []
    }
    main(actions)
    exit(0)
