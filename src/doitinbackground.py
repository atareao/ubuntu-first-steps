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
    gi.require_version('GLib', '2.0')
except Exception as e:
    print(e)
    exit(1)
from gi.repository import GObject
from gi.repository import GLib
from threading import Thread
import subprocess
import os
import shlex
import time


class DoItInBackground(GObject.GObject, Thread):
    __gsignals__ = {
        'started': (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, (int, )),
        'ended': (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, (bool,)),
        'done_one': (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE,
                     (str,)),
        'stopped': (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, ()),
    }

    def __init__(self, printer, commands):
        GObject.GObject.__init__(self)
        Thread.__init__(self)
        self.printer = printer
        self.commands = commands
        self.stopit = False
        self.ok = True
        self.daemon = True

    def emit(self, *args):
        GLib.idle_add(GObject.GObject.emit, self, *args)

    def execute(self, command):
        self.printer.feed(('$ %s\n\r' % (command)).encode())
        env = os.environ.copy()
        answer = ''
        try:
            po = subprocess.Popen(shlex.split(command),
                                  shell=False,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  universal_newlines=True,
                                  env=env)
            for stdout_line in iter(po.stdout.readline, ''):
                answer += stdout_line
                stdout_line = stdout_line.replace('\n', '\n\r')
                self.printer.feed(stdout_line.encode())
            return_code = po.wait()
            if command.startswith('add-apt-repository') and\
                    answer.find('OK') == -1:
                        self.ok = False
            if return_code:
                output = 'Error: %s\n\r' % (return_code)
                output = output + po.stderr.read().replace('\n', '\n\r') +\
                    '\n\r'
                self.printer.feed(output.encode())
                self.ok = False
        except OSError as e:
            print('Execution failed:', e)
            self.ok = False

    def stop(self, *args):
        self.stopit = True

    def run(self):
        self.emit('started', len(self.commands))
        for index, command in enumerate(self.commands):
            if self.stopit is True:
                self.emit('stopped')
                return
            self.execute(command)
            time.sleep(1)
            self.emit('done_one', command)
        self.emit('ended', self.ok)
