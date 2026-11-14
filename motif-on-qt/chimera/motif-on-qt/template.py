pkgname = "motif-on-qt"
pkgver = "0.1_git202611140548"
pkgrel = 0
_commit = "421a6489817d78aee3d8f5776026d3bb785f09f6"
build_style = "cmake"
configure_args = ["-DMQ_BUILD_EXAMPLES=OFF"]
hostmakedepends = ["cmake", "ninja", "pkgconf"]
makedepends = ["qt6-qtbase-devel"]
# only a static library and headers, so one package: build against it with
# makedepends = ["motif-on-qt"]
depends = ["pkgconf", "qt6-qtbase-devel"]
pkgdesc = "Motif, Xt and Xlib C APIs on Qt 6"
license = "LGPL-2.1-or-later AND MIT"
url = "https://github.com/staalmannen/qtmotifextension"
source = f"{url}/archive/{_commit}.tar.gz"
sha256 = "3227b580bb9e0a9ebfdd81e7c75d23f6fb6930ddab40f1cfa788fbdc1c916b87"
# the static archive must not hold LTO bitcode; the tests need the examples
options = ["!lto", "!check"]


def post_install(self):
    self.uninstall("usr/share/doc")
    # the vendored X11 and Xt headers carry their MIT notices themselves
    self.install_license("LICENSE.LGPL")
