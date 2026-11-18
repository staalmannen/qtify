pkgname = "motif-on-qt"
pkgver = "0.1_git202611180246"
pkgrel = 0
_commit = "24c2cc238df7bf6d3d660425fa06dc8ac0f65fdb"
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
sha256 = "ca034eee6b512619b01b9b11c5bcb6c995bcc7c087685233b945a3fb51298711"
# the static archive must not hold LTO bitcode; the tests need the examples
options = ["!lto", "!check"]


def post_install(self):
    self.uninstall("usr/share/doc")
    # the vendored X11 and Xt headers carry their MIT notices themselves
    self.install_license("LICENSE.LGPL")
