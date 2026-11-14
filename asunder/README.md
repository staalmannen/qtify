Asunder 3.0.1, the GTK 2 CD ripper and encoder, built from its unmodified
source against gtk-made-qt: it runs as a Qt application without GTK 2.

Notes on the recipes:

- The source is Debian's copy of the release (`asunder_3.0.1+ds.orig.tar.xz`,
  the same file in Ubuntu): it is the release without the generated
  `configure`, so every recipe runs `intltoolize` and `autoreconf` (as
  Debian does). littlesvr.ca, the upstream site, often refuses
  connections.
- Needs gtk-made-qt 9d43612 or newer: Asunder's threads update the window
  between `gdk_threads_enter()` and `gdk_threads_leave()`, and those
  sections must run on Qt's GUI thread. On musl (Alpine, Chimera)
  gtk-made-qt uses libucontext for that.
- `cdparanoia` is needed at run time (Asunder refuses to start without it);
  the encoders (lame, oggenc, flac, opusenc, wavpack ...) are optional and
  found in `PATH`.
- The check starts Asunder headless; with no drive it reports
  `Couldn't open /dev/cdrom` and quits. Asunder saves its settings with a
  non-recursive mkdir, so the test home gets a `.config` first.

Tested: the main window, the four preferences pages (folder button,
check-button frame labels), saving the settings, and the disc-polling
thread, also under valgrind. Ripping a real CD has not been tried yet (no
drive in the build machine).
