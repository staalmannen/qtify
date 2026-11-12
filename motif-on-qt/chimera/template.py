pkgname = "motif-on-qt"
pkgver = "0.1_git20261112"
pkgrel = 0
_commit = "bc5b3ed65994b163cdf97638520f5f1afb6007ea"
build_style = "cmake"
configure_args = ["-DMQ_BUILD_EXAMPLES=OFF"]
hostmakedepends = ["cmake", "ninja", "pkgconf"]
makedepends = ["qt6-qtbase-devel"]
pkgdesc = "Motif, Xt and Xlib C APIs on Qt 6"
license = "LGPL-2.1-or-later AND MIT"
url = "https://github.com/staalmannen/qtmotifextension"
source = f"{url}/archive/{_commit}.tar.gz"
sha256 = "966959020c3673d6cd92feb14ca82eaefa3f6959b65b192d8973c08f0ae19623"
# the static archive must not hold LTO bitcode; the tests need the examples.
# Only a static library and headers, so one package: build against it with
# makedepends = ["motif-on-qt"]
depends = ["pkgconf", "qt6-qtbase-devel"]
options = ["!lto", "!check"]


def post_install(self):
    self.uninstall("usr/share/doc")
