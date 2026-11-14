pkgname = "ddd-qtify"
pkgver = "3.4.1"
pkgrel = 0
build_style = "gnu_configure"
# no Xft: it would pull in the system's libX11 (fonts come from Qt)
configure_env = {"ac_cv_lib_Xft_XftFontOpen": "no"}
# the release has a generated configure; keep it
configure_gen = []
hostmakedepends = ["bison", "flex", "pkgconf"]
makedepends = ["motif-on-qt", "ncurses-devel"]
depends = ["gdb"]
provides = ["ddd=3.4.1"]
pkgdesc = "DDD, the GNU Data Display Debugger, on Qt"
license = "GPL-3.0-or-later"
url = "https://www.gnu.org/software/ddd"
# Debian's copy of the release
source = (
    f"https://deb.debian.org/debian/pool/main/d/ddd/ddd_{pkgver}.orig.tar.gz"
)
sha256 = "b87517a6c3f9611566347e283a2cf931fa369919b553536a2235e63402f4ee89"
# what motif-on-qt-env sets: Motif, Athena, Xt and Xlib from Motif on Qt
tool_flags = {
    "CFLAGS": ["-I/usr/include/motif-on-qt"],
    "CXXFLAGS": ["-I/usr/include/motif-on-qt"],
    "LDFLAGS": ["-L/usr/lib/motif-on-qt"],
}
env = {"PKG_CONFIG_PATH": "/usr/lib/motif-on-qt/pkgconfig"}
# DDD adds the INT_MIN sentinels of an empty graph's region (signed
# overflow at start-up, upstream; the trap would stop it with real Motif too)
hardening = ["!int"]
# the static library is not LTO
options = ["!lto"]


# reads the command line through Xrm and prints the version, without a
# debugger
def check(self):
    self.mkdir("test-home")
    self.do(
        "sh",
        "-c",
        f"./{self.make_dir}/ddd/ddd --version | grep -q 'GNU DDD 3.4'",
        env={
            "HOME": str(self.chroot_cwd / "test-home"),
            "QT_QPA_PLATFORM": "offscreen",
        },
    )
