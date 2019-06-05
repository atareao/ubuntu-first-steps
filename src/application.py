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
    gi.require_version('Gio', '2.0')
    gi.require_version('GLib', '2.0')
    gi.require_version('GdkPixbuf', '2.0')
except Exception as e:
    print(e)
    exit(1)
from gi.repository import Gtk
from gi.repository import Gio
from gi.repository import GLib
from gi.repository import GdkPixbuf

from comun import _
import comun
from mainwindow import MainWindow
import webbrowser


class Application(Gtk.Application):
    """start-here application object."""
    instance = None
    IS_DEVEL = True

    def __init__(self):
        Gtk.Application.__init__(self,
                                 application_id="es.atareao.start-here",
                                 flags=Gio.ApplicationFlags.FLAGS_NONE)
        GLib.set_application_name(_("start-here"))
        GLib.set_prgname("start-here")
        self.alive = True

        self._menu = Gio.Menu()

    @staticmethod
    def get_default():
        if Application.instance is None:
            Application.instance = Application()
        return Application.instance

    def do_startup(self):
        """Startup the application."""
        Gtk.Application.do_startup(self)
        self.__setup_actions()

    def __setup_actions(self):
        self.__add_action(
                'goto_homepage',
                callback=lambda x, y: webbrowser.open(
                    'http://www.atareao.es/'))
        self.__add_action(
            'goto_twitter',
            callback=lambda x, y: webbrowser.open(
                'http://twitter.com/atareao'))
        self.__add_action(
            'goto_github',
            callback=lambda x, y: webbrowser.open(
                'https://github.com/atareao'))
        self.__add_action(
            'goto_code',
            callback=lambda x, y: webbrowser.open(
                'https://github.com/atareao/start-here'))
        self.__add_action(
            'goto_bug',
            callback=lambda x, y: webbrowser.open(
                'https://github.com/atareao/start-here/issues'))
        self.__add_action(
            'goto_sugestion',
            callback=lambda x, y: webbrowser.open(
                'https://github.com/atareao/start-here/issues'))
        self.__add_action(
            'goto_donate',
            callback=lambda x, y: webbrowser.open(
                'https://www.atareao.es/donar/'))
        self.__add_action(
            'about',
            callback=self.on_about_activate)
        self.__add_action(
            'quit',
            callback=self.__on_quit)

        # Keyboard shortcuts. This includes actions defined in window.py.in
        self.set_accels_for_action("app.shortcuts", ["<Ctrl>question"])
        self.set_accels_for_action("app.quit", ["<Ctrl>Q"])
        self.set_accels_for_action("app.settings", ["<Ctrl>comma"])
        self.set_accels_for_action("win.add-account", ["<Ctrl>N"])
        self.set_accels_for_action("win.toggle-searchbar", ["<Ctrl>F"])

    def do_activate(self, *_):
        """On activate signal override."""
        window = MainWindow(self)
        self.add_window(window)
        window.show_all()
        window.present()

    def action_clicked(self, action, variant):
        print(action, variant)
        if variant:
            action.set_state(variant)

    def __add_action(self, name, callback=None, var_type=None,
                     value=None):
        if var_type is None:
            action = Gio.SimpleAction.new(name, None)
        else:
            action = Gio.SimpleAction.new_stateful(
                name,
                GLib.VariantType.new(var_type),
                GLib.Variant(var_type, value)
            )
        if callback is None:
            callback = self.action_clicked
        action.connect('activate', callback)
        self.add_action(action)

    def __on_quit(self, *_):
        self.get_active_window().close()
        self.quit()

    def on_about_activate(self, widget, optional):
        ad = Gtk.AboutDialog(comun.APPNAME, self.get_active_window())
        ad.set_name(comun.APPNAME)
        ad.set_version(comun.VERSION)
        ad.set_copyright('Copyrignt (c) 2019\nLorenzo Carbonell')
        ad.set_comments(_('An audio player for YouTube'))
        ad.set_license('''
This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.
''')
        ad.set_website('http://www.atareao.es')
        ad.set_website_label('http://www.atareao.es')
        ad.set_authors([
            'Lorenzo Carbonell <lorenzo.carbonell.cerezo@gmail.com>'])
        ad.set_documenters([
            'Lorenzo Carbonell <lorenzo.carbonell.cerezo@gmail.com>'])
        ad.set_translator_credits('\
Lorenzo Carbonell <lorenzo.carbonell.cerezo@gmail.com>\n')
        ad.set_program_name(comun.APPNAME)
        ad.set_logo(GdkPixbuf.Pixbuf.new_from_file(comun.ICON))
        ad.run()
        ad.destroy()