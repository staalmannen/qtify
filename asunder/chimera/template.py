pkgname = "asunder-qtify"
pkgver = "3.0.1"
pkgrel = 0
build_style = "gnu_configure"
hostmakedepends = [
    "automake",
    "gettext-devel",
    "intltool",
    "pkgconf",
]
makedepends = ["gtk-made-qt-devel", "libcddb-devel"]
depends = ["cdparanoia"]
checkdepends = ["cdparanoia"]
provides = ["asunder=3.0.1"]
pkgdesc = "Asunder, the GTK 2 CD ripper and encoder, on Qt"
license = "GPL-2.0-or-later"
url = "http://littlesvr.ca/asunder"
# Debian's copy of the release (+ds: without the generated configure)
source = f"https://deb.debian.org/debian/pool/main/a/asunder/asunder_{pkgver}+ds.orig.tar.xz"
sha256 = "b2237b9adb6587fb6fe311d79e3e733bcecc1a630295c61e2f4a0aed302775b9"
# what gtk-made-qt-env sets: gtk+-2.0 from GTK made Qt, linked statically
env = {"PKG_CONFIG_PATH": "/usr/lib/gtk-made-qt/pkgconfig"}
tool_flags = {"LDFLAGS": ["-L/usr/lib/gtk-made-qt"]}
# the static library is not LTO
options = ["!lto"]


def pre_configure(self):
    self.do("intltoolize", "--force")


def check(self):
    self.mkdir("test-home/.config", parents=True)
    self.do(
        "./src/asunder",
        env={
            "HOME": str(self.chroot_cwd / "test-home"),
            "QT_QPA_PLATFORM": "offscreen",
            "GTKQT_AUTOQUIT": "1500",
        },
    )
