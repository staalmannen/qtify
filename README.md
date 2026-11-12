# qtify
## (pronounced cute-ify)
A repository of package management files (for example PKGBUILD for Arch, APKGBUILD for Alpine or Chimera, ...) for rebuilding legacy GTK and Motif applications with Qt.

## Core dependencies
**GTK applications** are built using [gtk-made-qt](https://github.com/staalmannen/gtk-made-qt), which require GLib and Cairo in addition to the normal Qt dependencies.
**Motif applications** are built with [qtmotifextension](https://github.com/staalmannen/qtmotifextension), where all X11 dependencies have been replaced with an API built on top of Qt. A Motif application should thus be more portable (to Wayland, OSX, Windows, ...) when being rebuilt using Qt.




