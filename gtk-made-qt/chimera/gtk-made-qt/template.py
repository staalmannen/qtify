pkgname = "gtk-made-qt"
pkgver = "0.2.0_git202611191754"
pkgrel = 0
_commit = "edaf628594afacadc6f64e52314d4df45ebf6811"
build_style = "cmake"
configure_args = ["-DGTKQT_BUILD_EXAMPLES=OFF", "-DGTKQT_BUILD_TESTS=OFF"]
hostmakedepends = ["cmake", "ninja", "pkgconf"]
# libucontext: musl has no swapcontext (used by gdk_threads_enter)
# at-spi2-core-devel has ATK: libgailutil and gail.pc are built with it
makedepends = [
    "at-spi2-core-devel",
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
sha256 = "d779eb819c1cdc439607a30f50592f3145b12f50835c0a9459b74234036a6d8f"
# the static archive must not hold LTO bitcode; the tests need the examples
options = ["!lto", "!check"]


def post_install(self):
    self.uninstall("usr/share/doc")


@subpackage("gtk-made-qt-devel")
def _(self):
    self.depends += [
        "at-spi2-core-devel",
        "cairo-devel",
        "glib-devel",
        "libucontext-devel",
        "pango-devel",
        "pkgconf",
        "qt6-qtbase-devel",
    ]
    # the library is only static: the archive stays in -devel
    self.options = ["!splitstatic"]
    # the static library, linker scripts, pkg-config files and gtk-config
    return self.default_devel(
        extra=["usr/bin/gtk-made-qt-env", "usr/lib/gtk-made-qt"]
    )
