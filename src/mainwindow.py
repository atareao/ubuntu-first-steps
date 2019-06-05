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
import json
import mimetypes
import urllib
import comun
from comun import _
from sidewidget import SideWidget
from utils import get_desktop_environment
from settings import SettingRow
from tweak_dock import TweakDock
from tweak_desktop import TweakDesktop
from tweak_privacy import TweakPrivacy
from tweak_repositories import TweakRepositories
from tweak_packages import TweakPackages
from installer import Installer


DEFAULT_CURSOR = Gdk.Cursor(Gdk.CursorType.ARROW)
WAIT_CURSOR = Gdk.Cursor(Gdk.CursorType.WATCH)

if get_desktop_environment() == 'cinnamon':
    additional_components = ''
else:
    additional_components = '#progressbar,\n'
CSS = '''
window hdycolumn box list row combobox{
    padding-top: 10px;
    padding-bottom: 10px;
}
#sidewidget{
    padding: 10px;
}
window hdycolumn box list row{
    background-color: #ffffff;
    padding: 2px 8px;
    margin: 0;
    border: 1px solid #c3c9d0;
    border-bottom: 0px;
    color: #2d2d34;
}
window hdycolumn box list row:hover{
    background-color: #e0e0e1;
}
window hdycolumn box list row:selected{
    background-color: #e0e0e1;
}
window hdycolumn box list row:last-child{
    border-bottom: 1px solid #c3c9d0;
}

window hdycolumn box list row separator {
    background-color: #c3c9d0;
}

#special{
    font-size: 14px;
    font-weight:bold;
    color: #403f38;
    margin-bottom: 8px;
}

#label:hover,
#label{
    color: rgba(1, 1, 1, 1);
}
#label:selected{
    color: rgba(0, 1, 0, 1);
}
%s
#button:hover,
#button {
    border-image: none;
    background-image: none;
    background-color: rgba(0, 0, 0, 0);
    border-color: rgba(0, 0, 0, 0);
    border-image: none;
    border-radius: 0;
    border-width: 0;
    border-style: solid;
    text-shadow: 0 0 rgba(0, 0, 0, 0);
    box-shadow: 0 0 rgba(0, 0, 0, 0), 0 0 rgba(0, 0, 0, 0);
}
#button:hover{
    background-color: rgba(0, 0, 0, 0.1);
}''' % (additional_components)


class MainWindow(Gtk.ApplicationWindow):
    __gsignals__ = {
        'text-changed': (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE,
                         (object,)),
        'save-me': (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE,
                    (object,)), }

    def on_close(self, *args):
        pass

    def __init__(self, app, files=[]):
        Gtk.ApplicationWindow.__init__(self, application=app)
        self.app = app
        self.set_icon_from_file(comun.ICON)
        self.connect('destroy', self.on_close)

        self.get_root_window().set_cursor(WAIT_CURSOR)

        '''
        max_action = Gio.SimpleAction.new_stateful(
            "maximize", None, GLib.Variant.new_boolean(False))
        max_action.connect("change-state", self.on_maximize_toggle)
        self.add_action(max_action)
        '''

        self.notification = Notify.Notification.new('', '', '')

        self.init_headerbar()

        mainbox = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 5)
        self.add(mainbox)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_policy(Gtk.PolicyType.AUTOMATIC,
                                  Gtk.PolicyType.AUTOMATIC)
        scrolledwindow.set_shadow_type(Gtk.ShadowType.ETCHED_OUT)
        scrolledwindow.set_visible(True)
        scrolledwindow.set_property('min-content-width', 200)
        mainbox.pack_start(scrolledwindow, False, False, 0)

        sidebar = Gtk.ListBox()
        sidebar.connect('row-activated', self.on_row_activated)
        scrolledwindow.add(sidebar)

        option1 = SideWidget(_('Custom dock'),
                             'preferences-ubuntu-panel-symbolic')
        sidebar.add(option1)
        option2 = SideWidget(_('Custom desktop'),
                             'preferences-desktop-display')
        sidebar.add(option2)
        option3 = SideWidget(_('Privacy'),
                             'preferences-system-privacy-symbolic')
        sidebar.add(option3)
        option4 = SideWidget(_('Repositories'),
                             'folder-remote-symbolic')
        sidebar.add(option4)
        option5 = SideWidget(_('Applications'),
                             'software-store-symbolic')
        sidebar.add(option5)

        self.stack = Gtk.Stack()
        sw = Gtk.ScrolledWindow(child=self.stack)
        mainbox.pack_start(sw, True, True, 0)

        self.tweakDock = TweakDock()
        self.stack.add_named(self.tweakDock, 'tweakDock')
        option1.set_stack('tweakDock')

        self.tweakDesktop = TweakDesktop()
        self.stack.add_named(self.tweakDesktop, 'tweakDesktop')
        option2.set_stack('tweakDesktop')

        self.tweakPrivacy = TweakPrivacy()
        self.stack.add_named(self.tweakPrivacy, 'tweakPrivacy')
        option3.set_stack('tweakPrivacy')

        self.tweakRepositories = TweakRepositories()
        self.stack.add_named(self.tweakRepositories, 'tweakRepositories')
        option4.set_stack('tweakRepositories')

        self.tweakPackages = TweakPackages()
        self.stack.add_named(self.tweakPackages, 'tweakPackages')
        option5.set_stack('tweakPackages')

        self.get_root_window().set_cursor(DEFAULT_CURSOR)

        self.load_css()

        self.set_default_size(800, 700)
        monitor = Gdk.Display.get_primary_monitor(Gdk.Display.get_default())
        scale = monitor.get_scale_factor()
        width = monitor.get_geometry().width / scale
        height = monitor.get_geometry().height / scale
        self.move((width - 500)/2, (height - 600)/2)

        self.show_all()

    def on_row_activated(self, lb, sidewidget):
        self.stack.set_visible_child_name(sidewidget.get_stack())
    
    def on_apply_clicked(self, *args):
        print('clicked')
        # self.tweakDock.set_selected()
        # self.tweakDesktop.set_selected()
        # self.tweakPrivacy.set_selected()
        ppas = self.tweakRepositories.set_selected()
        apps = self.tweakPackages.set_selected()
        installer = Installer(ppas, apps)
        installer.run()

    def init_headerbar(self):
        self.control = {}
        self.menu_selected = 'suscriptions'
        #
        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.props.title = comun.APPNAME
        self.set_titlebar(hb)

        self.apply_controls = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 5)
        hb.pack_start(self.apply_controls)

        self.control['apply'] = Gtk.Button()
        self.control['apply'].connect('clicked', self.on_apply_clicked)
        self.control['apply'].set_tooltip_text(_('Apply changes'))
        self.control['apply'].add(Gtk.Image.new_from_gicon(Gio.ThemedIcon(
            name='preferences-system-symbolic'), Gtk.IconSize.BUTTON))
        self.apply_controls.pack_start(self.control['apply'],
                                       False, False, 0)

        help_model = Gio.Menu()

        help_section1_model = Gio.Menu()
        help_section1_model.append(_('Homepage'), 'app.goto_homepage')
        help_section1 = Gio.MenuItem.new_section(None, help_section1_model)
        help_model.append_item(help_section1)

        help_section2_model = Gio.Menu()
        help_section2_model.append(_('Code'), 'app.goto_code')
        help_section2_model.append(_('Issues'), 'app.goto_bug')
        help_section2 = Gio.MenuItem.new_section(None, help_section2_model)
        help_model.append_item(help_section2)

        help_section3_model = Gio.Menu()
        help_section3_model.append(_('Twitter'), 'app.goto_twitter')
        help_section3_model.append(_('Facebook'), 'app.goto_facebook')
        help_section3 = Gio.MenuItem.new_section(None, help_section3_model)
        help_model.append_item(help_section3)

        help_section4_model = Gio.Menu()
        help_section4_model.append(_('Donations'), 'app.goto_donate')
        help_section4 = Gio.MenuItem.new_section(None, help_section4_model)
        help_model.append_item(help_section4)

        help_section5_model = Gio.Menu()
        help_section5_model.append(_('About'), 'app.about')
        help_section5 = Gio.MenuItem.new_section(None, help_section5_model)
        help_model.append_item(help_section5)

        help_section6_model = Gio.Menu()
        help_section6_model.append(_('Quit'), 'app.quit')
        help_section6 = Gio.MenuItem.new_section(None, help_section6_model)
        help_model.append_item(help_section6)

        self.control['help'] = Gtk.MenuButton()
        self.control['help'].set_tooltip_text(_('Help'))
        self.control['help'].set_menu_model(help_model)
        self.control['help'].add(Gtk.Image.new_from_gicon(Gio.ThemedIcon(
            name='open-menu-symbolic'), Gtk.IconSize.BUTTON))
        hb.pack_end(self.control['help'])

    def on_toggled(self, widget, arg):
        if widget.get_active() is True:
            if arg == self.menu_selected:
                if self.menu[arg].get_active() is False:
                    self.menu[arg].set_active(True)
            else:
                old = self.menu_selected
                self.menu_selected = arg
                self.menu[old].set_active(False)
        else:
            if self.menu_selected == arg:
                widget.set_active(True)

    def load_css(self):
        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(CSS.encode())
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_USER)
