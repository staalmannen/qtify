# qtify
## (pronounced cute-ify)
A repository of package management files (for example PKGBUILD for Arch, APKBUILD for Alpine, cports templates for Chimera, ...) for rebuilding legacy GTK and Motif applications with Qt.

## Core dependencies
**GTK applications** are built using [gtk-made-qt](https://github.com/staalmannen/gtk-made-qt), which require GLib and Cairo in addition to the normal Qt dependencies.
**Motif applications** are built with [motif-on-qt](https://github.com/staalmannen/qtmotifextension), where all X11 dependencies have been replaced with an API built on top of Qt. A Motif application should thus be more portable (to Wayland, OSX, Windows, ...) when being rebuilt using Qt.

## Packages and formats

| Package | Built from | Arch | Alpine | Chimera | Fedora / openSUSE | Debian / Ubuntu |
| --- | --- | --- | --- | --- | --- | --- |
| [gtk-made-qt](gtk-made-qt) | git master (Arch), snapshot ff8aba1 (others) | `PKGBUILD` | `APKBUILD` | `chimera/` | `gtk-made-qt.spec` | `debian/` |
| [motif-on-qt](motif-on-qt) | git master (Arch), snapshot bc5b3ed (others) | `PKGBUILD` | `APKBUILD` | `chimera/` | `motif-on-qt.spec` | `debian/` |
| [leafpad](leafpad) (GTK 2) | 0.8.19 | `PKGBUILD` | `APKBUILD` | `chimera/` | `leafpad-qtify.spec` | `debian/` |
| [xmms](xmms) (GTK 1.2) | 1.2.11 | `PKGBUILD` | `APKBUILD` | `chimera/` | `xmms-qtify.spec` | `debian/` |
| [xpdf3](xpdf3) (Motif) | 3.04+git20240202 | `PKGBUILD` | `APKBUILD` | `chimera/` | `xpdf-qtify.spec` | `debian/` |
| [asunder](asunder) (GTK 2) | 3.0.1 | `PKGBUILD` | | | | |
| [nedit](nedit) (Motif) | 5.7 | `PKGBUILD` | | | | |

Applications are named `<program>-qtify` and provide / conflict with the
original package. The libraries come in two parts where the distribution
splits them: the shared library (`libgtk-made-qt.so.0`, only used by programs
with plugins such as XMMS) and the development package with headers, the
static library and the `gtk-made-qt-env` / `motif-on-qt-env` build wrappers.

### What was tested

- **Debian / Ubuntu**: every package built with `tools/build-deb.sh` on
  Ubuntu 24.04, installed, and run (XMMS plays through its disk writer
  plugin, finds its plugins in the system directory).
- **Fedora / openSUSE**: every spec built with `rpmbuild` (lib64 layout) on
  Ubuntu; not yet inside Fedora or openSUSE, so the dependency names
  (`cmake(Qt6Widgets)`, `pkgconfig(...)`, which both distributions provide)
  are unchecked.
- **Arch**: the PKGBUILDs' functions run as makepkg does, with Arch's
  default flags and GCC 14; not yet with makepkg on Arch itself.
- **Alpine**: the APKBUILDs' functions run as abuild does, with the musl
  target triple; not yet inside Alpine (musl, Alpine's package names).
- **Chimera**: written for cports, not yet built with cbuild.
- XMMS and both libraries also build with GCC 14 and clang 18 (C code of
  2007 meets their new default errors; see the notes in the recipes).
- asunder and nedit: PKGBUILDs only, not built yet.

## Building

### Arch
```sh
cd xmms && makepkg -si
```
Build `gtk-made-qt` / `motif-on-qt` first (they are `-git` packages that
follow the default branch). To publish to the AUR (each package is its own
AUR git repository):
```sh
tools/aur-prepare.sh xmms ~/aur      # clones, copies, writes .SRCINFO, stages
```
then review, commit and push in `~/aur/xmms-qtify`.

### Alpine
```sh
cd xmms && abuild -r
```

### Chimera (cports)
A cports template lives in a directory named after the package, and every
subpackage needs a symlink to it:
```sh
ln -s ~/qtify/gtk-made-qt/chimera ~/cports/user/gtk-made-qt
ln -s gtk-made-qt ~/cports/user/gtk-made-qt-devel
ln -s ~/qtify/xmms/chimera ~/cports/user/xmms-qtify
cd ~/cports && ./cbuild pkg user/xmms-qtify
```
(`motif-on-qt`, `leafpad-qtify` and `xpdf-qtify` the same way; motif-on-qt
has no subpackage.)

### Fedora / openSUSE
```sh
cd xmms
rpmbuild -ba --define "_sourcedir $PWD" --undefine=_disable_source_fetch xmms-qtify.spec
```
`--undefine=_disable_source_fetch` lets rpmbuild download Source0 (or use
`spectool -g`). Install the build dependencies first: on Fedora
`sudo dnf builddep xmms-qtify.spec`, on openSUSE
`sudo zypper install $(rpmspec -q --buildrequires xmms-qtify.spec)`.

### Debian / Ubuntu
```sh
sudo apt build-dep ./gtk-made-qt      # or mk-build-deps -i gtk-made-qt/debian/control
tools/build-deb.sh gtk-made-qt
sudo apt install ./build-deb/libgtk-made-qt0_*.deb ./build-deb/gtk-made-qt-dev_*.deb
tools/build-deb.sh xmms
```
`tools/build-deb.sh` downloads the source named in `debian/qtify-source`,
checks its SHA-256, adds `debian/` and runs `dpkg-buildpackage` (it also
leaves a source package for a PPA or OBS).

## Updating a snapshot

The library recipes outside Arch pin a commit. To move them to a newer one,
change the commit, version and checksum in each file:
`APKBUILD` (`_commit`, `pkgver`, `sha512sums`), `chimera/template.py`
(`_commit`, `pkgver`, `sha256`), the `.spec` (`commit`, `snapdate`),
`debian/changelog` and `debian/qtify-source`. GitHub's archive of a commit is
reproducible: `git archive --format=tar --prefix=<repo>-<commit>/ <commit> |
gzip -n` gives the same bytes, so checksums can be computed from a clone.
