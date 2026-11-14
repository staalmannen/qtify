pkgname = "motif-on-qt"
pkgver = "0.1_git202611141521"
pkgrel = 0
_commit = "54dacc657de15e55f94274c4d454a4f9b69e6225"
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
sha256 = "e0906ec6f5844b63b1cb6689daf9b4533fb447595aa1e0ba8af2aa806661d00b"
# the static archive must not hold LTO bitcode; the tests need the examples
options = ["!lto", "!check"]


def post_install(self):
    self.uninstall("usr/share/doc")
    # the vendored X11 and Xt headers carry their MIT notices themselves
    self.install_license("LICENSE.LGPL")
