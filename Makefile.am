EXTRA_DIST = etc \
	usr

SUBDIRS = src

install-data-hook:
	mkdir -p $(DESTDIR)$(sysconfdir)/xdg/menus
	cp -r $(srcdir)/etc/* $(DESTDIR)$(sysconfdir)
	cp -r $(srcdir)/usr $(DESTDIR)
