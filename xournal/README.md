Xournal 0.4.8.2016, the GTK 2 note taker and PDF annotator, built from its
unmodified source against gtk-made-qt: it runs as a Qt application without
GTK.

Notes on the recipes:

- Three sources: Debian's copy of the Xournal release (the same file in
  Ubuntu), and libart 2.3.21 and libgnomecanvas 2.30.3 from GNOME, also
  unmodified. Xournal's page is a GnomeCanvas; libgnomecanvas for GTK 2
  (and libart in some distributions) is no longer packaged, and a system
  copy built for real GTK would pull GTK in. Both are built static into a
  scratch prefix inside the build and linked into the program; nothing of
  them is installed.
- libgnomecanvas uses libgailutil and ATK for its accessibility objects:
  gtk-made-qt edaf628 or newer, built with ATK (its recipes depend on it),
  has them.
- The static libgnomecanvas needs its private dependencies (gail,
  pangoft2) when Xournal links it: its scratch `.pc` file gets them as
  `Requires` (`pkg-config --static` would drag in the private
  dependencies of every system library as well).
- `-Wno-error=implicit-function-declaration`: GCC 14 and clang 16 reject
  ttsubset's calls of `read`/`write`/`close` without `<unistd.h>` (glibc
  pulls it in indirectly, musl does not). `-fgnu89-inline`: `I_det` in
  xo-shapes.c is a plain `inline` function, which links only where the
  compiler inlines it (not at Alpine's `-Os`).
- libgnomecanvas's configure checks for intltool, even without NLS.
- PDF backgrounds come from poppler-glib.
- The check starts Xournal headless with a new journal and quits.
- The desktop file, MIME type and icons are installed as upstream's
  `make desktop-install` does, without its KDE 3 `mimelnk` file.

Built, installed and run on Ubuntu 24.04, Alpine edge and Chimera.
Tested (installed): drawing with pens of several colours, the text tool
(a text view on the canvas, sized to its text), rectangle selection,
copy and paste through the clipboard, undo, saving a journal, exporting
to PDF, opening a PDF to annotate, compared with Ubuntu's xournal on
real GTK 2.
