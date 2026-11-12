pkgname = "gtk-made-qt"
pkgver = "0.2.0_git20261112"
pkgrel = 0
_commit = "ff8aba1520c15b381ae7c4b3155697d69be05fd9"
build_style = "cmake"
configure_args = ["-DGTKQT_BUILD_EXAMPLES=OFF", "-DGTKQT_BUILD_TESTS=OFF"]
hostmakedepends = ["cmake", "ninja", "pkgconf"]
makedepends = ["cairo-devel", "glib-devel", "pango-devel", "qt6-qtbase-devel"]
pkgdesc = "GTK 1.2/2/3/4 C API on Qt 6"
license = "LGPL-2.1-or-later"
url = "https://github.com/staalmannen/gtk-made-qt"
source = f"{url}/archive/{_commit}.tar.gz"
sha256 = "aa29e1cbf29f695d673fd80756492dc6fedd7ac8d5b7cbcd9f2d92170e9958cd"
# the static archive must not hold LTO bitcode; the tests need the examples
options = ["!lto", "!check"]


def post_install(self):
    self.uninstall("usr/share/doc")


@subpackage("gtk-made-qt-devel")
def _(self):
    self.depends += [
        "cairo-devel",
        "glib-devel",
        "pango-devel",
        "pkgconf",
        "qt6-qtbase-devel",
    ]
    # the static library, linker scripts, pkg-config files and gtk-config
    return self.default_devel(
        extra=["usr/bin/gtk-made-qt-env", "usr/lib/gtk-made-qt"]
    )
