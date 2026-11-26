pkgname = "transmission-gtk-qtify"
pkgver = "3.00"
pkgrel = 0
build_style = "gnu_configure"
configure_args = [
    "--with-gtk",
    "--disable-cli",
    "--disable-daemon",
    "--disable-mac",
]
# the release has a configure
configure_gen = []
hostmakedepends = ["gettext-devel", "intltool", "pkgconf"]
makedepends = [
    "curl-devel",
    "gtk-made-qt-devel",
    "libevent-devel",
    "openssl3-devel",
    "zlib-ng-compat-devel",
]
provides = ["transmission-gtk=3.00"]
pkgdesc = "Transmission, the BitTorrent client (GTK interface), on Qt"
license = "GPL-2.0-or-later"
url = "https://transmissionbt.com"
# Debian's copy of the release
source = f"https://deb.debian.org/debian/pool/main/t/transmission/transmission_{pkgver}.orig.tar.xz"
sha256 = "9144652fe742f7f7dd6657716e378da60b751aaeda8bef8344b3eefc4db255f2"
# what gtk-made-qt-env sets: GTK from GTK made Qt, linked statically;
# 2020 GTK code passes some objects with the wrong pointer type
tool_flags = {
    "CFLAGS": ["-Wno-error=incompatible-pointer-types"],
    "LDFLAGS": ["-L/usr/lib/gtk-made-qt"],
}
env = {"PKG_CONFIG_PATH": "/usr/lib/gtk-made-qt/pkgconfig"}
# the static library is not LTO
options = ["!lto"]


# the GTK client and its translations (built out of tree, in make_dir);
# the utilities and the web
# interface are transmission's own package
def install(self):
    self.make.install(wrksrc=f"{self.make_dir}/gtk")
    self.make.install(wrksrc=f"{self.make_dir}/po")


def check(self):
    self.do(
        "sh",
        "-c",
        f"./{self.make_dir}/gtk/transmission-gtk --version 2>&1 | grep -q 'transmission-gtk 3.00'",
    )
    # the main window, headless, on a scratch profile
    home = self.chroot_cwd / "check-home"
    self.mkdir("check-home/transmission", parents=True)
    (self.cwd / "check-home/transmission/settings.json").write_text(
        '{ "user-has-given-informed-consent": true }\n'
    )
    self.do(
        f"./{self.make_dir}/gtk/transmission-gtk",
        env={
            "XDG_CONFIG_HOME": str(home),
            "QT_QPA_PLATFORM": "offscreen",
            "GTKQT_AUTOQUIT": "1500",
        },
    )
