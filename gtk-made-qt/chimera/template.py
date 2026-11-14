pkgname = "gtk-made-qt"
pkgver = "0.2.0_git20261114"
pkgrel = 0
_commit = "ee24bf3c1058a6d56e1a61bda9a7a9379d38610b"
build_style = "cmake"
configure_args = ["-DGTKQT_BUILD_EXAMPLES=OFF", "-DGTKQT_BUILD_TESTS=OFF"]
hostmakedepends = ["cmake", "ninja", "pkgconf"]
# libucontext: musl has no swapcontext (used by gdk_threads_enter)
makedepends = [
    "cairo-devel",
    "glib-devel",
    "libucontext-devel",
    "pango-devel",
    "qt6-qtbase-devel",
]
pkgdesc = "GTK 1.2/2/3/4 C API on Qt 6"
license = "LGPL-2.1-or-later"
url = "https://github.com/staalmannen/gtk-made-qt"
source = f"{url}/archive/{_commit}.tar.gz"
sha256 = "f5ee0323b7a01fd22132a4a59faa342eecb7bf4e860d74b8ce98a6abeb7a09ed"
# the static archive must not hold LTO bitcode; the tests need the examples
options = ["!lto", "!check"]


def post_install(self):
    self.uninstall("usr/share/doc")


@subpackage("gtk-made-qt-devel")
def _(self):
    self.depends += [
        "cairo-devel",
        "glib-devel",
        "libucontext-devel",
        "pango-devel",
        "pkgconf",
        "qt6-qtbase-devel",
    ]
    # the static library, linker scripts, pkg-config files and gtk-config
    return self.default_devel(
        extra=["usr/bin/gtk-made-qt-env", "usr/lib/gtk-made-qt"]
    )
