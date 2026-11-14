pkgname = "motif-on-qt"
pkgver = "0.1_git20261114"
pkgrel = 0
_commit = "491b66c0cfa740d5ec5a623c66d90f2d3b1e969c"
build_style = "cmake"
configure_args = ["-DMQ_BUILD_EXAMPLES=OFF"]
hostmakedepends = ["cmake", "ninja", "pkgconf"]
makedepends = ["qt6-qtbase-devel"]
pkgdesc = "Motif, Xt and Xlib C APIs on Qt 6"
license = "LGPL-2.1-or-later AND MIT"
url = "https://github.com/staalmannen/qtmotifextension"
source = f"{url}/archive/{_commit}.tar.gz"
sha256 = "0b343f54514fd4ed141ab64e8f8f55ac2734fe72b18d2718cfc87b15f57600dd"
# the static archive must not hold LTO bitcode; the tests need the examples.
# Only a static library and headers, so one package: build against it with
# makedepends = ["motif-on-qt"]
depends = ["pkgconf", "qt6-qtbase-devel"]
options = ["!lto", "!check"]


def post_install(self):
    self.uninstall("usr/share/doc")
