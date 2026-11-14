NEdit 5.7, the classic Motif programmer's editor, built from the release
tarball against motif-on-qt: it runs as a Qt application without libXm,
libXt or libX11.

Notes on the recipes:

- NEdit's makefiles set `CFLAGS` and `LIBS` themselves, so the paths that
  `motif-on-qt-env` provides are passed on the `make linux` command line.
- `-std=gnu17`: NEdit declares unprototyped function pointers, which C23
  (GCC 15's default) reads as taking no arguments.
- The man pages are generated from the POD sources with `pod2man` (the
  tarball has no ready-made ones).
- The client `nc` is installed as `nedit-nc` (as Debian and Fedora do):
  `nc` is netcat. NEdit's server mode talks through X properties, which do
  not cross processes without an X server, so `nedit-nc` cannot reach a
  running NEdit yet.
