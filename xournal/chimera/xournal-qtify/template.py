pkgname = "xournal-qtify"
pkgver = "0.4.8.2016"
pkgrel = 0
_artver = "2.3.21"
_canvasver = "2.30.3"
build_style = "gnu_configure"
# the shipped configure scripts are used as they are
configure_gen = []
# libgnomecanvas's configure checks for intltool
hostmakedepends = ["intltool", "pkgconf"]
makedepends = ["gtk-made-qt-devel", "poppler-devel", "zlib-ng-compat-devel"]
provides = ["xournal=0.4.8.2016"]
pkgdesc = "Xournal, the GTK 2 note taker and PDF annotator, on Qt"
license = "GPL-2.0-or-later AND LGPL-2.0-or-later"
url = "https://xournal.sourceforge.net"
# Debian's copy of the Xournal release; libart and libgnomecanvas (for
# GTK 2, long gone from distributions) are built into the program
source = [
    f"https://deb.debian.org/debian/pool/main/x/xournal/xournal_{pkgver}.orig.tar.gz",
    f"https://download.gnome.org/sources/libart_lgpl/2.3/libart_lgpl-{_artver}.tar.bz2",
    f"https://download.gnome.org/sources/libgnomecanvas/2.30/libgnomecanvas-{_canvasver}.tar.bz2",
]
source_paths = [".", "libart", "libgnomecanvas"]
sha256 = [
    "1d6b2609b1e3b2873332710e4b9fa6db676b3c3983fc46cb717bf4d1955c754e",
    "fdc11e74c10fc9ffe4188537e2b370c0abacca7d89021d4d303afdf7fd7476fa",
    "859b78e08489fce4d5c15c676fec1cd79782f115f516e8ad8bed6abcb8dedd40",
]
# what gtk-made-qt-env sets: gtk+-2.0 from GTK made Qt, linked statically
# clang 16 makes ttsubset's implicit read/write/close declarations errors;
# I_det in xo-shapes.c is a GNU89 inline function
tool_flags = {
    "CFLAGS": ["-Wno-error=implicit-function-declaration", "-fgnu89-inline"],
    "LDFLAGS": ["-L/usr/lib/gtk-made-qt"],
}
env = {"PKG_CONFIG_PATH": "/usr/lib/gtk-made-qt/pkgconfig"}
# the static libraries are not LTO
options = ["!lto"]


# libart and libgnomecanvas: static, only for this build; Xournal finds
# libgnomecanvas there
def pre_configure(self):
    from cbuild.util import gnu_configure

    # libart and libgnomecanvas are configured here, before the configure
    # step refreshes config.sub (which does not know musl)
    gnu_configure.replace_guess(self)
    # where libc has no gettext of its own (musl) glib's gettext macro puts
    # the catalogs (and the program's locale directory) in /usr/lib/locale
    conf = self.cwd / "configure"
    conf.write_text(
        conf.read_text().replace("DATADIRNAME=lib", "DATADIRNAME=share")
    )
    mk = self.cwd / "po/Makefile.in.in"
    mk.write_text(
        mk.read_text().replace(
            "localedir = $(libdir)/locale", "localedir = $(datadir)/locale"
        )
    )
    deps = str(self.chroot_cwd / "deps")
    host = [f"--host={self.profile.triplet}"] if self.profile.triplet else []
    for d, extra in (("libart", []), ("libgnomecanvas", ["--disable-nls"])):
        self.do(
            "./configure",
            f"--prefix={deps}",
            "--disable-shared",
            "--enable-static",
            "--with-pic",
            *host,
            *extra,
            wrksrc=d,
            env={
                "PKG_CONFIG_PATH": f"/usr/lib/gtk-made-qt/pkgconfig:{deps}/lib/pkgconfig"
            },
        )
        self.do("make", f"-j{self.make_jobs}", wrksrc=d)
        self.do("make", "install", wrksrc=d)
    # the static library needs its private dependencies (gail, pangoft2)
    pc = self.cwd / "deps/lib/pkgconfig/libgnomecanvas-2.0.pc"
    pc.write_text(pc.read_text().replace("Requires.private:", "Requires:"))
    self.configure_env = {
        "PKG_CONFIG_PATH": f"/usr/lib/gtk-made-qt/pkgconfig:{deps}/lib/pkgconfig",
    }


# starts headless with a new journal and quits
def check(self):
    self.mkdir("test-home")
    self.do(
        f"./{self.make_dir}/src/xournal",
        env={
            "HOME": str(self.chroot_cwd / "test-home"),
            "QT_QPA_PLATFORM": "offscreen",
            "GTKQT_AUTOQUIT": "2000",
        },
    )


# what upstream's desktop-install adds (without the KDE 3 mimelnk file)
def post_install(self):
    self.install_file("xournal.desktop", "usr/share/applications")
    self.install_file("xournal.xml", "usr/share/mime/packages")
    self.install_file(
        "pixmaps/xournal.svg", "usr/share/icons/hicolor/scalable/apps"
    )
    self.install_file(
        "pixmaps/xoj.svg",
        "usr/share/icons/hicolor/scalable/mimetypes",
        name="application-x-xoj.svg",
    )
