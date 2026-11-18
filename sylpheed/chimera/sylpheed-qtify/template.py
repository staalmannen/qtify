pkgname = "sylpheed-qtify"
pkgver = "3.7.0"
pkgrel = 0
build_style = "gnu_configure"
configure_args = [
    "--disable-gtkspell",
    "--disable-gpgme",
    "--disable-compface",
    "--disable-rpath",
]
# its shipped configure is used as it is
configure_gen = []
hostmakedepends = ["gettext-devel", "pkgconf"]
makedepends = ["gtk-made-qt-devel", "openssl3-devel"]
provides = ["sylpheed=3.7.0"]
pkgdesc = "Sylpheed, the GTK 2 mail client, on Qt"
license = "GPL-2.0-or-later AND LGPL-2.1-or-later"
url = "https://sylpheed.sraoss.jp"
# Debian's copy of the release tarball
source = f"https://deb.debian.org/debian/pool/main/s/sylpheed/sylpheed_{pkgver}.orig.tar.bz2"
sha256 = "3e6ac156fa1f7c7b3a4e8a5b077488c77b49374318575bb9e32ae13b3655cbe7"
# what gtk-made-qt-env --shared sets: GTK from GTK made Qt's shared
# library, as the plugin library calls GTK too
# clang 16 and GCC 14 make libsylph's pointer type mismatches errors
tool_flags = {
    "CFLAGS": [
        "-Wno-error=incompatible-pointer-types",
        "-Wno-error=incompatible-function-pointer-types",
    ],
    "LDFLAGS": ["-L/usr/lib/gtk-made-qt/shared"],
}
env = {"PKG_CONFIG_PATH": "/usr/lib/gtk-made-qt/shared/pkgconfig"}
# the program installs its icon to /usr/share/pixmaps itself
options = ["!lto", "!lintpixmaps"]


def pre_configure(self):
    # where libc has no gettext of its own (musl) glib's gettext macro picks
    # .mo catalogs, which po/ installs to /usr/lib/locale; the program reads
    # them from /usr/share/locale
    mk = self.cwd / "po/Makefile.in.in"
    mk.write_text(
        mk.read_text().replace(
            "localedir = $(libdir)/locale", "localedir = $(datadir)/locale"
        )
    )


# starts headless in an empty home (the first run dialog) and quits
def check(self):
    self.mkdir("test-home")
    self.do(
        f"./{self.make_dir}/src/sylpheed",
        env={
            "HOME": str(self.chroot_cwd / "test-home"),
            "LANG": "C.UTF-8",
            "QT_QPA_PLATFORM": "offscreen",
            "GTKQT_AUTOQUIT": "2000",
        },
    )


def post_install(self):
    self.uninstall("usr/lib/*.la", glob=True)


@subpackage("sylpheed-qtify-devel")
def _(self):
    return self.default_devel()
