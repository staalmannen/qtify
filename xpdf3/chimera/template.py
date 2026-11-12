pkgname = "xpdf-qtify"
_debver = "3.04+git20240202"
pkgver = "3.04_git20240202"
pkgrel = 0
build_style = "gnu_configure"
configure_args = ["--sysconfdir=/etc"]
hostmakedepends = ["automake", "pkgconf"]
makedepends = ["motif-on-qt", "poppler-devel"]
provides = ["xpdf=3.04"]
pkgdesc = "Xpdf 3, the Motif PDF viewer (Poppler based), on Qt"
license = "GPL-2.0-only OR GPL-3.0-only"
url = "https://tracker.debian.org/pkg/xpdf"
source = f"https://deb.debian.org/debian/pool/main/x/xpdf/xpdf_{_debver}.orig.tar.xz"
sha256 = "3a020caedde7e75997373e6eb2076c81e25586d8422cd161d6d17203c51f76ae"
# what motif-on-qt-env sets: Motif, Xt and Xlib from Motif on Qt
env = {"PKG_CONFIG_PATH": "/usr/lib/motif-on-qt/pkgconfig"}
tool_flags = {
    "CFLAGS": ["-I/usr/include/motif-on-qt"],
    "CXXFLAGS": ["-I/usr/include/motif-on-qt"],
    "LDFLAGS": ["-L/usr/lib/motif-on-qt"],
}
# the static library is not LTO
options = ["!lto"]


def check(self):
    # -v prints the version and exits with status 99 (xpdf's convention)
    self.do(
        "sh",
        "-c",
        "./xpdf/xpdf -v 2>&1 | grep -q 'xpdf version 3'",
        env={"QT_QPA_PLATFORM": "offscreen"},
    )
