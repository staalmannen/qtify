pkgname = "motif-on-qt"
pkgver = "0.1_git202611141549"
pkgrel = 0
_commit = "80f683941783107f408ba88d3aa2f6946d0dbb60"
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
sha256 = "2444af897cfcab71350b8fa539e4263fcf9a74bfb01b6f1229dd02a4c01df1b1"
# the static archive must not hold LTO bitcode; the tests need the examples
options = ["!lto", "!check"]


def post_install(self):
    self.uninstall("usr/share/doc")
    # the vendored X11 and Xt headers carry their MIT notices themselves
    self.install_license("LICENSE.LGPL")
