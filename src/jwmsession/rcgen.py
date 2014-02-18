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

values = ['menufile',
          'tray-y',
          'tray-height',
          'tray-autohide',
          'clockformat',
          'windowfont',
          'trayfont',
          'menufont']

template = """
<?xml version="1.0"?>
<JWM>
   <RootMenu height="25" onroot="0">
      <Include>%menufile%</Include>
      <Separator/>
      <Exit label="Logout" confirm="false" icon="quit.png"/>
   </RootMenu>
   <Group>
      <Class>Pidgin</Class>
      <Option>sticky</Option>
   </Group>
   <!-- Additional tray attributes: autohide, width, border, layer, layout -->
   <Tray  x="0" y="%tray-y%" height="%tray-height%" autohide="%tray-autohide%" border="false">
      <TrayButton label="Apps" border="false">root:0</TrayButton>
      <TaskList maxwidth="175" border="false"/>
      <Dock/>
      <Clock format="%clockformat%"></Clock>
   </Tray>
   <!-- Visual Styles -->
   <WindowStyle>
    <Font>%windowfont%</Font>
    <Width>6</Width>
    <Height>28</Height>
    <Active>
       <Text>#000000</Text>
       <Title>#D0D0D0</Title>
       <Outline>#333333</Outline>
    </Active>
    <Inactive>
       <Text>#7f7f7f</Text>
       <Title>#D0D0D0</Title>
       <Outline>#ffffff</Outline>
    </Inactive>
   </WindowStyle>
   <TaskListStyle>
        <Font>%trayfont%</Font>
        <ActiveForeground>#ffffff</ActiveForeground>
        <ActiveBackground>#2e2e2e</ActiveBackground>
        <Background>#333333</Background>
        <Foreground>#7f7f7f</Foreground>
    </TaskListStyle>
    <!-- TRAY PROPERTIES -->
    <TrayStyle>
        <Font>%trayfont%</Font>
        <Foreground>#ffffff</Foreground>
        <Background>#333333</Background>
    </TrayStyle>
    <!-- PAGER PROPERTIES -->
    <PagerStyle>
        <Outline>grey</Outline>
        <Foreground>#7f7f7f</Foreground>
        <Background>#333333</Background>
        <ActiveForeground>#333333</ActiveForeground>
        <ActiveBackground>#2e2e2e</ActiveBackground>
    </PagerStyle>
       <PopupStyle>
        <Font>%trayfont%</Font>
        <Outline>#7f7f7f</Outline>
        <Foreground>#ffffff</Foreground>
        <Background>#333333</Background>
    </PopupStyle>
    <MenuStyle>
        <Font>%menufont%</Font>
        <Foreground>#ffffff</Foreground>
        <Background>#333333</Background>
        <ActiveForeground>#ffffff</ActiveForeground>
        <ActiveBackground>#7f7f7f</ActiveBackground>
    </MenuStyle>
   <IconPath>
      /usr/share/icons/wm-icons/32x32-gant
   </IconPath>
   <!-- Virtual Desktops -->
   <!-- Desktop tags can be contained within Desktops for desktop names. -->
   <Desktops width="1" height="1">
      <Background type="image">%wallpaper%</Background>
   </Desktops>
   <!-- Double click speed (in milliseconds) -->
   <DoubleClickSpeed>400</DoubleClickSpeed>
   <!-- Double click delta (in pixels) -->
   <DoubleClickDelta>2</DoubleClickDelta>
   <!-- The focus model (sloppy or click) -->
   <FocusModel>click</FocusModel>
   <!-- The snap mode (none, screen, or border) -->
   <SnapMode distance="10">border</SnapMode>
   <!-- The move mode (outline or opaque) -->
   <MoveMode coordinates="window">opaque</MoveMode>
   <!-- The resize mode (outline or opaque) -->
   <ResizeMode coordinates="window">opaque</ResizeMode>
   <!-- Key bindings -->
   <Key key="Up">up</Key>
   <Key key="Down">down</Key>
   <Key key="Right">right</Key>
   <Key key="Left">left</Key>
   <Key key="h">left</Key>
   <Key key="j">down</Key>
   <Key key="k">up</Key>
   <Key key="l">right</Key>
   <Key key="Return">select</Key>
   <Key key="Escape">escape</Key>
   <Key mask="A" key="Tab">next</Key>
   <Key mask="A" key="F4">close</Key>
   <Key mask="A" key="#">desktop#</Key>
   <Key mask="A" key="F1">root:1</Key>
   <Key mask="A" key="F2">window</Key>
   <Key mask="A" key="F10">maximize</Key>
   <Key mask="A" key="Right">rdesktop</Key>
   <Key mask="A" key="Left">ldesktop</Key>
   <Key mask="A" key="Up">udesktop</Key>
   <Key mask="A" key="Down">ddesktop</Key>
</JWM>
"""

class ConfGenerator():
    
    def __init__(self, SettingsWorkerInstance):
        self._service = SettingsWorkerInstance._service
        self._template = template
        for val in values:
            self._replace(val)
        
    def _replace(self, val):
        newvalue = self._service.get('desktop.jwm.configuration', val, "string")
        self._template.replace('%' + val + '%', newvalue)