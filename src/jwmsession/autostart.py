'''
jwmsession.autostart
    
    XDG Autostart
    
    Based on xdg-autostart by Dana Jansens
    Released under the terms of the GNU GPL v3

Copyright 2012 joshiggins

This file is part of the KX Platform Suite.

KX Platform is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published
by the Free Software Foundation, either version 3 of the License,
or (at your option) any later version.

KX Platform is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with KX Platform. If not, see http://www.gnu.org/licenses/.
'''


import os
import glob
from xdg import BaseDirectory
from xdg.DesktopEntry import DesktopEntry
from xdg.Exceptions import ParsingError


def autostart(environments):
    # get the autostart directories
    autodirs = BaseDirectory.load_config_paths("autostart")
    # find all the autostart files
    files = []
    for mdir in autodirs:
        for path in glob.glob(os.path.join(mdir, '*.desktop')):
            try:
                autofile = AutostartFile(path)
            except ParsingError:
                print("Invalid .desktop file: " + path)
            else:
                if not autofile in files:
                    files.append(autofile)
    # run them
    for autofile in files:
        autofile.run(environments)

class AutostartFile:
    def __init__(self, path):
        self.path = path
        self.filename = os.path.basename(path)
        self.dirname = os.path.dirname(path)
        self.de = DesktopEntry(path)

    def __eq__(self, other):
        return self.filename == other.filename

    def __str__(self):
        return self.path + " : " + self.de.getName()

    def _isexecfile(self, path):
        return os.access(path, os.X_OK)

    def _findFile(self, path, search, match_func):
        # check empty path
        if not path: return None
        # check absolute path
        if path[0] == '/':
            if match_func(path): return path
            else: return None
        else:
            # check relative path
            for dirname in search.split(os.pathsep):
                if dirname != "":
                    candidate = os.path.join(dirname, path)
                    if (match_func(candidate)): return candidate

    def _alert(self, mstr, info=False):
        if info:
            print("\t " + mstr)
        else:
            print("\t*" + mstr)

    def _showInEnvironment(self, envs, verbose=False):
        default = not self.de.getOnlyShowIn()
        noshow = False
        force = False
        for i in self.de.getOnlyShowIn():
            if i in envs: force = True
        for i in self.de.getNotShowIn():
            if i in envs: noshow = True

        if verbose:
            if not default and not force:
                s = ""
                for i in self.de.getOnlyShowIn():
                    if s: s += ", "
                    s += i
                self._alert("Excluded by: OnlyShowIn (" + s + ")")
            if default and noshow and not force:
                s = ""
                for i in self.de.getNotShowIn():
                    if s: s += ", "
                    s += i
                self._alert("Excluded by: NotShowIn (" + s + ")")
        return (default and not noshow) or force

    def _shouldRun(self, envs, verbose=False):
        if not self.de.getExec():
            if verbose: self._alert("Excluded by: Missing Exec field")
            return False
        if self.de.getHidden():
            if verbose: self._alert("Excluded by: Hidden")
            return False
        if self.de.getTryExec():
            if not self._findFile(self.de.getTryExec(), os.getenv("PATH"),
                                  self._isexecfile):
                if verbose: self._alert("Excluded by: TryExec (" +
                                        self.de.getTryExec() + ")")
                return False
        if not self._showInEnvironment(envs, verbose):
            return False
        return True

    def display(self, envs):
        if self._shouldRun(envs):
            print("[*] " + self.de.getName())
        else:
            print("[ ] " + self.de.getName())
        self._alert("File: " + self.path, info=True)
        if self.de.getExec():
            self._alert("Executes: " + self.de.getExec(), info=True)
        self._shouldRun(envs, True)
        print

    def run(self, envs):
        here = os.getcwd()
        if self.de.getPath():
            os.chdir(self.de.getPath())
        if self._shouldRun(envs):
            args = ["/bin/sh", "-c", "exec " + self.de.getExec()]
            os.spawnv(os.P_NOWAIT, args[0], args);
        os.chdir(here)
