'''
jwmsession.rcgen
    
    Generate default jwmrc
    In the spirit of JWM I'm not going to implement loads 
    of custom options that I am not going to use. You can 
    set the generate-jwmrc option to False to stop this 
    behaviour.


Copyright 2014 joshiggins

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


values = ['menufile',
          'tray-y',
          'tray-height',
          'tray-autohide',
          'clockformat',
          'windowfont',
          'trayfont',
          'menufont']

template_path = "@sysconfdir@/jwm/template.jwmrc"

class ConfGenerator():
    
    def __init__(self, SettingsWorkerInstance):
        self._service = SettingsWorkerInstance._service
        self._template = open(template_path, "r").read()
        for val in values:
            self._replace(val)
        
    def _replace(self, val):
        newvalue = self._service.get('desktop.jwm.configuration', val, "string")
        self._template.replace('%' + val + '%', newvalue)
        
    def to_file(self, handle):
        handle.write(self._template)