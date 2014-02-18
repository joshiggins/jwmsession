'''
jwmsession.dconf
    
    DConf settings watcher
    ...because we are more than likely going to have
    other Gnome apps installed!


Copyright 2012 Joshua Higgins

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


import gi
gi.require_version('Gdk', '3.0')
from gi.repository import Gio  # @UnresolvedImport


class SettingsWatcher:

    def __init__(self, schema):
        # Create a new Settings
        self.settings = Gio.Settings.new(schema)

    def connect(self, setting, callback):
        """Attach callback for setting change"""
        self.settings.connect("changed::" + setting, callback)

    def get_boolean(self, setting):
        return self.settings.get_boolean(setting)

    def get_string(self, setting):
        return self.settings.get_string(setting)

    def get_int(self, setting):
        return self.settings.get_int(setting)
    
    def get_variant(self, setting):
        return self.settings.get_value(setting)
