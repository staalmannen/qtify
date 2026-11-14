pkgname = "motif-on-qt"
pkgver = "0.1_git202611140924"
pkgrel = 0
_commit = "cfff583cbe09cf5f231b2716b36caa9c8e40d332"
build_style = "cmake"
configure_args = ["-DMQ_BUILD_EXAMPLES=OFF"]
hostmakedepends = ["cmake", "ninja", "pkgconf"]
makedepends = ["qt6-qtbase-devel"]
# only a static library and headers, so one package: build against it with
# makedepends = ["motif-on-qt"]
depends = ["pkgconf", "qt6-qtbase-devel"]
pkgdesc = "Motif, Xt and Xlib C APIs on Qt 6"
license = "LGPL-2.1-or-later AND MIT"
url = "https://github.com/staalmannen/motif-on-qt"
source = f"{url}/archive/{_commit}.tar.gz"
sha256 = "b03dafa3b65f703b52a0ba4b4841169fbabd62ceac16da927faf26a3492c3e7e"
# the static archive must not hold LTO bitcode; the tests need the examples
options = ["!lto", "!check"]


def post_install(self):
    self.uninstall("usr/share/doc")
    # the vendored X11 and Xt headers carry their MIT notices themselves
    self.install_license("LICENSE.LGPL")
