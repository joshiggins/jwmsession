'''
h5desktop.settings
    
    Settings manager


Copyright 2014 Joshua Higgins

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
import subprocess
import dbus.service


import jwmsession.dconf
import jwmsession.rcgen


class SettingsService(dbus.service.Object):
    
    def __init__(self, ETCDIR, logger):
        self.ETCDIR = ETCDIR
        bus_name = dbus.service.BusName('org.jwm', bus=dbus.SessionBus())
        dbus.service.Object.__init__(self, bus_name, '/org/jwm/Settings')
        self.logger = logger
        # Initiate a settings manager
        self.sworker = SettingsWorker(self)

    @dbus.service.method('org.jwm.Settings')
    def reloadSettings(self):
        self.sworker.reload_settings()
        
    @dbus.service.method('org.jwm.Settings',
                         in_signature='sss',
                         out_signature='v')
    def get(self, schema, value, rtype):
        s = jwmsession.dconf.SettingsWatcher(schema)
        if rtype == "string":
            return s.get_string(value)
        elif rtype == "bool":
            return s.get_boolean(value)
        elif rtype == "int":
            return s.get_int(value)
        elif rtype == "variant":
            return s.get_variant(value)


class SettingsWorker:

    def __init__(self, service):
        self._service = service
        self.logger = self._service.logger
        self.desktopsettings = jwmsession.dconf.SettingsWatcher("desktop.jwm.appearance")
        # Attach watchers
        self.attach_watchers()

    def _backup_file(self, path):
        if os.path.exists(path):
            try:
                old = open(path, "r").read()
                bak = open(path + ".bak", "w")
                bak.write(old)
                bak.close()
            except Exception as e:
                self.logger.log_error("Could not backup " + path + ": " + str(e))
                return False
        return True

    def attach_watchers(self):
        self.desktopsettings.connect("background-path", self.set_wallpaper)
        self.desktopsettings.connect("font", self.set_gtk)
        self.desktopsettings.connect("font-dpi", self.set_xrdb)
        self.desktopsettings.connect("gtk-theme", self.set_gtk)
        self.desktopsettings.connect("icon-theme", self.set_gtk)
        self.desktopsettings.connect("xft-antialias", self.set_xrdb)
        self.desktopsettings.connect("xft-hinting", self.set_xrdb)
        self.desktopsettings.connect("xft-hintstyle", self.set_xrdb)
        self.desktopsettings.connect("xft-rgba", self.set_xrdb)

    def reload_settings(self):
        """Reloads the desktop settings from dconf and writes config files"""
        self.update_jwmrc()
        self.set_xrdb()
        self.set_gtk()
        self.set_wallpaper()
        
    def set_wallpaper(self):
        # ping pcmanfm if using it as desktop manager
        if self._service.get('desktop.jwm.session', 'desktop-manager', "string") == "pcmanfm --desktop":
            self.logger.log_debug("setting wallpaper with pcmanfm")
            cmd = "pcmanfm --set-wallpaper=" + self.desktopsettings.get_string("background-path")
            subprocess.Popen(cmd, shell=True).wait()
        else:
            # set it using feh, but if the session has already been started
            # the wallpaper specified in jwmrc will be ignore temporarily, until
            # the config file is rewritten next login
            self.logger.log_debug("setting wallpaper with feh")
            cmd = "feh --bg-scale " + self.desktopsettings.get_string("background-path")
            subprocess.Popen(cmd, shell=True).wait()
    
    def update_jwmrc(self):
        # write jwmrc if we are allowed
        if self._service.get('desktop.jwm.session', 'generate-jwmrc', "bool"):
            self.logger.log_debug("writing jwmrc")
            gc = jwmsession.rcgen.ConfGenerator(self)
            if self._backup_file(os.path.expanduser("~/.jwmrc")):
                f = open(os.path.expanduser("~/.jwmrc"), "w")
                gc.to_file(f)
                f.close()
        else:
            self.logger.log_debug("not writing jwmrc")

    def set_xrdb(self, event=None, data=None):
        try:
            self.logger.log_debug("writing .Xresources")
            if self._backup_file(os.path.expanduser("~/.Xresources")):
                f = open(os.path.expanduser("~/.Xresources"), "w")
                f.write("Xft.dpi: " + str(self.desktopsettings.get_int("font-dpi")) + "\n")
                f.write("Xft.antialias: " + self.desktopsettings.get_string("xft-antialias") + "\n")
                f.write("Xft.hinting: " + self.desktopsettings.get_string("xft-hinting") + "\n")
                f.write("Xft.rgba: " + self.desktopsettings.get_string("xft-rgba") + "\n")
                f.write("Xft.hintstyle: " + self.desktopsettings.get_string("xft-hintstyle") + "\n")
                f.close
            self.logger.log_debug("merging with xrdb")
            xrdbcmd = 'xrdb -merge ' + os.path.expanduser("~/.Xresources")
            subprocess.Popen(xrdbcmd, shell=True).wait()
        except Exception as e:
            self.logger.log_error("could not set xrdb " + str(e))

    def set_gtk(self, event=None, data=None):
        self.set_gtk3()
        self.set_gtk2()

    def set_gtk3(self, event=None, data=None):
        # Create GTK3 config directory if it doesn't exist
        if not os.path.exists(os.path.expanduser("~/.config/gtk-3.0/")):
            self.logger.log_debug("creating gtk3 config directory")
            os.makedirs(os.path.expanduser("~/.config/gtk-3.0/"))
        try:
            self.logger.log_debug("writing gtk3 settings.ini")
            if self._backup_file(os.path.expanduser("~/.config/gtk-3.0/settings.ini")):
                f = open(os.path.expanduser("~/.config/gtk-3.0/settings.ini"), "w")
                f.write("[Settings]" + "\n")
                f.write("gtk-theme-name = " + self.desktopsettings.get_string("gtk-theme") + "\n")
                f.write("gtk-icon-theme-name = " + self.desktopsettings.get_string("icon-theme") + "\n")
                f.write("gtk-font-name = " + self.desktopsettings.get_string("font") + "\n")
                f.close
        except Exception as e:
            self.logger.log_error("could not write gtk3 settings.ini" + str(e))

    def set_gtk2(self, event=None, data=None):
        try:
            self.logger.log_debug("writing gtk2 .gtkrc-2.0")
            if self._backup_file(os.path.expanduser("~/.gtkrc-2.0")):
                f = open(os.path.expanduser("~/.gtkrc-2.0"), "w")
                f.write("gtk-theme-name = \"" + self.desktopsettings.get_string("gtk-theme") + "\"\n")
                f.write("gtk-icon-theme-name = \"" + self.desktopsettings.get_string("icon-theme") + "\"\n")
                f.write("gtk-font-name = \"" + self.desktopsettings.get_string("font") + "\"\n")
                f.close
        except Exception as e:
            self.logger.log_debug("could not write gtk2 .gtkrc-2.0 " + str(e))
