pkgname = "leafpad-qtify"
pkgver = "0.8.19"
pkgrel = 0
_commit = "3b1a2c2a1fad10f7f03e9b240bb6fa425aed5417"
build_style = "gnu_configure"
# autoreconf runs in pre_configure, before configure is adjusted
configure_gen = []
hostmakedepends = [
    "automake",
    "gettext-devel",
    "intltool",
    "pkgconf",
]
makedepends = ["gtk-made-qt-devel"]
provides = ["leafpad=0.8.19"]
pkgdesc = "Leafpad, the GTK 2 text editor, on Qt"
license = "GPL-2.0-or-later"
url = "https://github.com/tarot231/leafpad"
source = f"{url}/archive/{_commit}.tar.gz"
sha256 = "a57774ef72694758fe61e8a9cc151c394d3a2a3c5c9cf3ff3c2d874bb1926115"
# what gtk-made-qt-env sets: gtk+-2.0 from GTK made Qt, linked statically
tool_flags = {"LDFLAGS": ["-L/usr/lib/gtk-made-qt"]}
env = {"PKG_CONFIG_PATH": "/usr/lib/gtk-made-qt/pkgconfig"}
# the static library is not LTO; the program loads its icon from
# /usr/share/pixmaps itself
options = ["!lto", "!lintpixmaps"]


def pre_configure(self):
    self.do("intltoolize", "--force")
    self.do("autoreconf", "-fi")
    # glib's gettext macro puts the catalogs (and the program's LOCALEDIR)
    # in /usr/lib/locale where libc has no gettext of its own (musl)
    conf = self.cwd / "configure"
    text = conf.read_text()
    text = text.replace("DATADIRNAME=lib", "DATADIRNAME=share")
    text = text.replace('"${libdir}/locale"', '"${datadir}/locale"')
    conf.write_text(text)


def check(self):
    self.do(
        f"./{self.make_dir}/src/leafpad",
        env={"QT_QPA_PLATFORM": "offscreen", "GTKQT_AUTOQUIT": "1000"},
    )
