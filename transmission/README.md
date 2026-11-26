Transmission 3.00, the BitTorrent client's GTK 3 interface, built from its
unmodified source against gtk-made-qt: it runs as a Qt application without
GTK.

Notes on the recipes:

- The source is Debian's copy of the release (the same file in Ubuntu).
  3.00 is the last release whose GTK interface is C; 4.x moved to C++ and
  gtkmm.
- Only the GTK client is built (`--disable-cli --disable-daemon`) and
  installed (from `gtk/` and `po/`): transmission-remote, the daemon and
  the web interface come from the distribution's own Transmission
  packages. On Debian / Ubuntu and Fedora the application icons are
  transmission-common's (recommended); the other recipes install them.
- `-Wno-error=incompatible-pointer-types`: the GTK code passes a few objects
  with the wrong pointer type (the real GTK headers give the same
  warnings), which GCC 14 makes an error.
- Needs gtk-made-qt 39b63c3 or newer (tree models through the interface,
  filter and sort models, cell renderer classes, the icon theme, tooltips).
- The check starts the client headless on a scratch profile and quits.

Tested (GTK made Qt, headless, compared with the same program on real
GTK 3 under Xvfb): adding torrents (the options dialog with its file tree),
the torrent list with its own cell renderer, the filter bar, the
properties dialog (information, files, trackers, options), preferences,
selection and the actions' sensitivity.
