pkgname = "xpdf-qtify"
_debver = "3.04+git20260802"
pkgver = "3.04_git20260802"
pkgrel = 0
build_style = "gnu_configure"
configure_args = ["--sysconfdir=/etc"]
hostmakedepends = ["automake", "pkgconf"]
makedepends = ["motif-on-qt", "poppler-devel"]
provides = ["xpdf=3.04"]
pkgdesc = "Xpdf 3, the Motif PDF viewer (Poppler based), on Qt"
license = "GPL-2.0-only OR GPL-3.0-only"
url = "https://tracker.debian.org/pkg/xpdf"
source = (
    f"https://deb.debian.org/debian/pool/main/x/xpdf/xpdf_{_debver}.orig.tar.xz"
)
sha256 = "3d08a47306ac7515736cb256d63ea2f0cbaeafa4f05961fcd6cf38e3dbea83e6"
tool_flags = {
    "CFLAGS": ["-I/usr/include/motif-on-qt"],
    # poppler 25 headers use C++20 (std::span, string::ends_with)
    "CXXFLAGS": ["-I/usr/include/motif-on-qt", "-std=gnu++20"],
    "LDFLAGS": ["-L/usr/lib/motif-on-qt"],
}
# the static library is not LTO
# what motif-on-qt-env sets: Motif, Xt and Xlib from Motif on Qt
env = {"PKG_CONFIG_PATH": "/usr/lib/motif-on-qt/pkgconfig"}
options = ["!lto"]


def check(self):
    # -v prints the version and exits with status 99 (xpdf's convention)
    self.do(
        "sh",
        "-c",
        f"./{self.make_dir}/xpdf/xpdf -v 2>&1 | grep -q 'version 3'",
        env={"QT_QPA_PLATFORM": "offscreen"},
    )
