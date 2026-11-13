pkgname = "motif-on-qt"
pkgver = "0.1_git20261113"
pkgrel = 0
_commit = "249a95f10befb10f7c6b6b76587949dbd1abaa16"
build_style = "cmake"
configure_args = ["-DMQ_BUILD_EXAMPLES=OFF"]
hostmakedepends = ["cmake", "ninja", "pkgconf"]
makedepends = ["qt6-qtbase-devel"]
pkgdesc = "Motif, Xt and Xlib C APIs on Qt 6"
license = "LGPL-2.1-or-later AND MIT"
url = "https://github.com/staalmannen/qtmotifextension"
source = f"{url}/archive/{_commit}.tar.gz"
sha256 = "000aeaeb69da52b9551288902e30140b8871d1f0b98bc8f22314a7a6608d063e"
# the static archive must not hold LTO bitcode; the tests need the examples.
# Only a static library and headers, so one package: build against it with
# makedepends = ["motif-on-qt"]
depends = ["pkgconf", "qt6-qtbase-devel"]
options = ["!lto", "!check"]


def post_install(self):
    self.uninstall("usr/share/doc")
