pkgname = "motif-on-qt"
pkgver = "0.1_git202611142017"
pkgrel = 0
_commit = "4b231cb3b6cdb3ff168d138f854e9c25e07f3644"
build_style = "cmake"
configure_args = ["-DMQ_BUILD_EXAMPLES=OFF"]
hostmakedepends = ["cmake", "ninja", "pkgconf"]
makedepends = ["qt6-qtbase-devel"]
# only a static library and headers, so one package: build against it with
# makedepends = ["motif-on-qt"]
depends = ["pkgconf", "qt6-qtbase-devel"]
pkgdesc = "Motif, Athena, Xt and Xlib C APIs on Qt 6"
license = "LGPL-2.1-or-later AND MIT"
url = "https://github.com/staalmannen/motif-on-qt"
source = f"{url}/archive/{_commit}.tar.gz"
sha256 = "0fff4910b3bff3a02c9b1f06c19fc2231acfbb6f5abfde5a857d8909367f2b60"
# the static archive must not hold LTO bitcode; the tests need the examples
options = ["!lto", "!check"]


def post_install(self):
    self.uninstall("usr/share/doc")
    # the vendored X11 and Xt headers carry their MIT notices themselves
    self.install_license("LICENSE.LGPL")
