pkgname = "asunder-qtify"
pkgver = "3.0.1"
pkgrel = 0
build_style = "gnu_configure"
# autoreconf runs in pre_configure, before configure is adjusted
configure_gen = []
# in the source tree: its install hook does "cd syslogng"
make_dir = "."
hostmakedepends = [
    "automake",
    "gettext-devel",
    "intltool",
    "pkgconf",
]
makedepends = ["gtk-made-qt-devel", "libcddb-devel"]
checkdepends = ["cdparanoia"]
depends = ["cdparanoia"]
provides = ["asunder=3.0.1"]
pkgdesc = "Asunder, the GTK 2 CD ripper and encoder, on Qt"
license = "GPL-2.0-or-later"
url = "http://littlesvr.ca/asunder"
# Debian's copy of the release (+ds: without the generated configure)
source = f"https://deb.debian.org/debian/pool/main/a/asunder/asunder_{pkgver}+ds.orig.tar.xz"
sha256 = "b2237b9adb6587fb6fe311d79e3e733bcecc1a630295c61e2f4a0aed302775b9"
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
    self.mkdir("test-home/.config", parents=True)
    self.do(
        f"./{self.make_dir}/src/asunder",
        env={
            "HOME": str(self.chroot_cwd / "test-home"),
            "QT_QPA_PLATFORM": "offscreen",
            "GTKQT_AUTOQUIT": "1500",
        },
    )
