pkgname = "galculator-qtify"
pkgver = "2.1.4"
pkgrel = 0
build_style = "gnu_configure"
# autoreconf runs in pre_configure, before configure is adjusted
configure_gen = []
hostmakedepends = [
    "automake",
    "flex",
    "gettext-devel",
    "intltool",
    "libtool",
    "pkgconf",
]
makedepends = ["gtk-made-qt-devel"]
provides = ["galculator=2.1.4"]
pkgdesc = "Galculator, the GTK scientific calculator, on Qt"
license = "GPL-2.0-or-later"
url = "http://galculator.mnim.org"
# Debian's copy of the release (without the generated configure)
source = f"https://deb.debian.org/debian/pool/main/g/galculator/galculator_{pkgver}.orig.tar.gz"
sha256 = "dcbdb48ddf8a3f68b9aa5902f880f174fd269de2b7410988148d05871012e142"
# what gtk-made-qt-env sets: GTK from GTK made Qt, linked statically;
# gnu17 and -fcommon: 2016 C (Debian patches the source for the same)
tool_flags = {
    "CFLAGS": ["-std=gnu17", "-fcommon"],
    "LDFLAGS": ["-L/usr/lib/gtk-made-qt"],
}
env = {"PKG_CONFIG_PATH": "/usr/lib/gtk-made-qt/pkgconfig"}
# the static library is not LTO; the program loads its icon from
# /usr/share/pixmaps itself
options = ["!lto", "!lintpixmaps"]


def pre_configure(self):
    self.mkdir("m4", parents=True)
    self.do("intltoolize", "--force")
    self.do("autoreconf", "-fi")
    # glib's gettext macro puts the catalogs (and the program's LOCALEDIR)
    # in /usr/lib/locale where libc has no gettext of its own (musl)
    conf = self.cwd / "configure"
    text = conf.read_text()
    text = text.replace("DATADIRNAME=lib", "DATADIRNAME=share")
    text = text.replace('"${libdir}/locale"', '"${datadir}/locale"')
    conf.write_text(text)


# starts the toolkit; the window needs the installed interface files
def check(self):
    self.do(
        "sh",
        "-c",
        f"./{self.make_dir}/src/galculator -v | grep -q 'galculator v2'",
        env={"QT_QPA_PLATFORM": "offscreen"},
    )
