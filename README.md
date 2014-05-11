# jwmsession

jwmsession is a kind of session manager written for (but in no way endorsed by) JWM, with the aim of making a more comfortable desktop environment but keeping the speed and simplicity of a window manager.

It depends on some core Gnome technologies like GLib, DBus and GSettings(DConf), but since we will more than likely have a Gnome application installed this dependency is acceptable.

Requires
--------

- Python >=3.2
- GLib
- DBus
- Appropriate Python bindings
- JWM

Installing
----------

```
./configure --prefix=/usr --sysconfdir=/etc
make
make DESTDIR=/ install
```

Setup
-----

1. jwmsession includes some gschemas and you should compile them with `glib-compile-schemas /usr/share/glib-2.0/schemas/`
2. A .desktop file is placed in /usr/share/xsessions so that you can pick jwmsession from your login manager
3. Use `jwmenugen` to generate a fancy XDG-based menu file for JWM, complete with icons.
4. jwmsession will generate it's own template .jwmrc on every login. Set the `desktop.jwm.session.generate-jwmrc` key to `false` to stop this behaviour. The template file used to generate this is located in `/etc/jwm/template.jwmrc`.
5. All other desktop settings (themes, icons, fonts, wallpaper etc etc) can be managed using `gsettings` or `dconf-editor`.
