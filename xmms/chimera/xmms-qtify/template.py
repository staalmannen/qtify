pkgname = "xmms-qtify"
pkgver = "1.2.11"
pkgrel = 0
_commit = "5847897230da018d93cd9833695f944ece96587b"
hostmakedepends = ["gtk-made-qt-devel", "pkgconf"]
makedepends = [
    "alsa-lib-devel",
    "gtk-made-qt-devel",
    "libogg-devel",
    "libvorbis-devel",
]
provides = ["xmms=1.2.11"]
pkgdesc = "XMMS, the GTK 1.2 audio player, on Qt"
license = "GPL-2.0-or-later"
url = "https://github.com/deepfire/xmms"
source = f"{url}/archive/{_commit}.tar.gz"
sha256 = "3963f5e2c0c9b55598dff2e0e86a4b02cae952c46a82f43a62421b22b32d05d1"
# gnu17: GTK 1 era C (unprototyped callbacks, its own bool) is not C23
tool_flags = {"CFLAGS": ["-std=gnu17"]}
# no LTO: the 2007 configure's function checks give false positives with
# it; gtk-made-qt-env points at the build machine's library
options = ["!lto", "!cross"]


def post_extract(self):
    # its 2007 config.sub does not know musl
    from cbuild.util import gnu_configure

    gnu_configure.replace_guess(self)
    # the getopt.c copies include <string.h> only on glibc
    for f in ["wmxmms/getopt.c", "xmms/getopt.c"]:
        p = self.cwd / f
        src = p.read_bytes()
        p.write_bytes(
            src.replace(b"<stdio.h>\n", b"<stdio.h>\n#include <string.h>\n", 1)
        )
    # time stamps as in the release tarball, so make does not rerun automake 1.x
    self.do(
        "sh",
        "-c",
        "find . -exec touch -h -t 200101010000 {} + && "
        "touch -t 200101010001 aclocal.m4 && "
        "touch -t 200101010002 configure "
        "$(find . -name Makefile.in -o -name '*.h.in')",
    )


# the 2007 configure rejects options newer configure scripts take, so it is
# run by hand, under gtk-made-qt-env (the shared library: plugins call GTK)
def configure(self):
    self.do(
        "gtk-made-qt-env",
        "--shared",
        "./configure",
        f"--build={self.profile.triplet}",
        f"--host={self.profile.triplet}",
        "--prefix=/usr",
        "--sysconfdir=/etc",
        "--mandir=/usr/share/man",
        "--disable-esd",
        "--disable-opengl",
        "--disable-mikmod",
        "--disable-nls",
        "ac_cv_lib_SM_SmcOpenConnection=no",
    )


def build(self):
    self.do("gtk-made-qt-env", "--shared", "make", f"-j{self.make_jobs}")


def check(self):
    # starts, shows its windows and quits
    self.do(
        "./xmms/xmms",
        env={
            "HOME": str(self.chroot_cwd / "test-home"),
            "QT_QPA_PLATFORM": "offscreen",
            "GTKQT_AUTOQUIT": "1500",
        },
    )


def install(self):
    self.do("make", f"DESTDIR={self.chroot_destdir}", "install")
    self.uninstall("usr/lib/*.la", glob=True)
    self.uninstall("usr/lib/xmms/*/*.la", glob=True)
    self.uninstall("usr/lib/libxmms.a")
    self.install_file(
        self.files_path / "xmms.desktop", "usr/share/applications"
    )
