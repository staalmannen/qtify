Galculator 2.1.4, the GTK scientific calculator, built from its unmodified
source against gtk-made-qt: it runs as a Qt application without GTK.

Notes on the recipes:

- The source is Debian's copy of the release (the same file in Ubuntu),
  which has no generated `configure`: the recipes run `intltoolize` and
  `autoreconf` (after creating the `m4/` directory intltoolize writes to).
- Built for GTK 3, Galculator's default (`--disable-gtk3` builds the GTK 2
  version, which works as well).
- `-std=gnu17 -fcommon`: code of 2016 that GCC 10+ and C23 reject; Debian
  patches the source for the same two problems.
- The check runs `galculator -v` (starts the toolkit): the window needs the
  interface files in /usr/share/galculator, which exist only once installed.
- Needs gtk-made-qt 5ebef1c or newer (builder accelerators, GTK's toggle
  button order, every keysym name).

Tested (installed): typing and clicking calculations, the scientific and paper modes,
the preferences dialog (font and color buttons), with both GTK versions.
