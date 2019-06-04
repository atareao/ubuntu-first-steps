#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# start-here is a program that helps you to tweak Ubuntu,
# after install a new version of Ubuntu.
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

import os
import sys
import gi
try:
    gi.require_version('Gtk', '3.0')
    gi.require_version('Handy', '0.0')
except Exception as e:
    print(e)
    exit(-1)
from gi.repository import Gtk
from gi.repository import Handy

if __name__ == '__main__':
    mdir = os.path.dirname(os.path.abspath(__file__))
    if mdir.startswith('/opt/extras.ubuntu.com/start-here'):
        sys.path.insert(
            1, '/opt/extras.ubuntu.com/start-here/share/start-here')
    else:
        sys.path.insert(1, os.path.normpath(os.path.join(mdir, '../src')))
    from application import Application
    try:
        Handy.init(None)
        app = Application.get_default()
        exit_status = app.run(None)
        sys.exit(exit_status)
    except KeyboardInterrupt:
        exit()