'''
jwmsession.menugen
    
    Generate JWM menu, kind of like Debian's menu,
    but with icons

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


import xdg.Menu
import xdg.IconTheme


class MenuGenerator:
    
    def __init__(self, definition, icontheme):
        self._definition = definition
        self._icontheme = icontheme
        
    def _write(self):
        lines = []
        lines.append("<JWM>")
        xdgmenu = xdg.Menu.parse(self._definition)
        for entry in xdgmenu.getEntries():
            if isinstance(entry, xdg.Menu.Menu) and entry.Show is True:
                try:
                    menu_icon_path = xdg.IconTheme.getIconPath(entry.getIcon(), 24, self._icontheme)
                    lines.append('    <Menu icon="' + menu_icon_path + '" label="' + entry.getName() + '">')
                except:
                    lines.append('    <Menu label="' + entry.getName() + '">')
                for entry2 in entry.getEntries():
                    try:
                        name = entry2.DesktopEntry.getName()
                        icon_name = entry2.DesktopEntry.getIcon()
                        texec = entry2.DesktopEntry.getExec().split("%")[0]
                        try:
                            icon_path = xdg.IconTheme.getIconPath(icon_name, 24, self._icontheme)
                            lines.append('        <Program label="' + name + '" icon="' + icon_path + '" confirm="false">' + texec + "</Program>")
                        except:
                            lines.append('        <Program label="' + name + '" confirm="false">' + texec + "</Program>")
                    except:
                        pass
                lines.append('    </Menu>')
        lines.append("</JWM>")
        return lines
    
    def to_file(self, handle):
        for line in self._write():
            handle.write(line + "\n")

    def to_screen(self):
        for line in self._write():
            print(line)
            

if __name__ == "__main__":
    import sys
    mg = MenuGenerator(None, sys.argv[2])
    f = open(sys.argv[1], 'wt', encoding='utf-8')
    mg.to_file(f)
    f.close()