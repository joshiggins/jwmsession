'''
h5desktop.session
    
    Session Manager


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


import subprocess
import dbus.service


import jwmsession.settings
import jwmsession.autostart


class SessionService(dbus.service.Object):

    def __init__(self, SessionClassInstance, loop):
        bus_name = dbus.service.BusName('org.jwm', bus=dbus.SessionBus())
        dbus.service.Object.__init__(self, bus_name, '/org/jwm/Session')
        self.session = SessionClassInstance
        self.loop = loop

    @dbus.service.method('org.jwm.Session')
    def logout(self):
        self.session._jwm.kill()
        self.loop.quit()


class Session():

    def __init__(self, loop):
        self.session = "JWM"
        # Settings
        self.service = SessionService(self, loop)

    def default(self):
        self.settings_manager()
        self.jwm()
        self.autostart()

    def settings_manager(self):
        # Start the settings manager
        self.SettingsService = jwmsession.settings.SettingsService()

    def autostart(self):
        # Run the xdg autostart
        if self.SettingsService.get_boolean("ignore-xdg-autostart") is not True:
            jwmsession.autostart.autostart(['JWM'])

    def jwm(self):
        # start JWM!
        # keep hold of it so we can kill it on logout
        self._jwm = subprocess.Popen("jwm", shell=True)
