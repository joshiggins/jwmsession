bin_SCRIPTS = startjwm \
	jwmenugen
CLEANFILES = $(bin_SCRIPTS)
EXTRA_DIST = startjwm.in \
	jwmenugen.in

do_substitution = sed -e 's,[@]pythondir[@],$(pythondir),g'
do_subprefdir = sed -e 's,[@]prefixdir[@],$(PREFIX),g'
do_subconfdir = sed -e 's,[@]sysconfdir[@],$(sysconfdir),g'

startjwm: startjwm.in Makefile
	$(do_substitution) < $(srcdir)/startjwm.in > startjwm.2
	$(do_subconfdir) < $(srcdir)/startjwm.2 > startjwm
	chmod +x startjwm
	
jwmenugen: jwmenugen.in Makefile
	$(do_substitution) < $(srcdir)/jwmenugen.in > jwmenugen.2
	$(do_subconfdir) < $(srcdir)/jwmenugen.2 > jwmenugen
	rm $(srcdir)/jwmenugen.2
	chmod +x jwmenugen

SUBDIRS = jwmsession
