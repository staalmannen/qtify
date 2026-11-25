pkgname = "grace-qtify"
pkgver = "5.1.25"
pkgrel = 0
build_style = "gnu_configure"
# X headers and libraries are Motif on Qt's (configure would look for the
# system's X11); Grace's bundled Xbae and T1lib are used
configure_args = [
    "--enable-grace-home=/usr/share/grace",
    "--with-bundled-xbae",
    "--with-bundled-t1lib",
    "--disable-pdfdrv",
    "--disable-netcdf",
    "--without-fftw",
    "--disable-xmhtml",
    "--x-includes=/usr/include/motif-on-qt",
    "--x-libraries=/usr/lib/motif-on-qt",
]
# the release has a generated configure; keep it
configure_gen = []
# its Makefiles build in the source tree only
make_dir = "."
hostmakedepends = ["pkgconf"]
makedepends = [
    "libjpeg-turbo-devel",
    "libpng-devel",
    "motif-on-qt",
    "zlib-ng-compat-devel",
]
provides = ["grace=5.1.25"]
pkgdesc = "Grace (xmgrace), the Motif 2D plotting tool, on Qt"
license = "GPL-2.0-or-later"
url = "https://plasma-gate.weizmann.ac.il/Grace"
# Debian's copy of the release
source = f"https://deb.debian.org/debian/pool/main/g/grace/grace_{pkgver}.orig.tar.gz"
sha256 = "751ab9917ed0f6232073c193aba74046037e185d73b77bab0f5af3e3ff1da2ac"
# what motif-on-qt-env sets: Motif, Xt and Xlib from Motif on Qt; clang 16
# makes the implicit declarations of 2000-era code errors (and hardened
# builds T1lib's printf (model)), and C23 reads its unprototyped functions
# as taking no arguments
tool_flags = {
    "CFLAGS": [
        "-I/usr/include/motif-on-qt",
        "-std=gnu17",
        "-Wno-error=implicit-function-declaration",
        "-Wno-error=incompatible-pointer-types",
        "-Wno-error=incompatible-function-pointer-types",
        "-Wno-error=int-conversion",
        "-Wno-error=implicit-int",
        "-Wno-error=format-security",
    ],
    "LDFLAGS": ["-L/usr/lib/motif-on-qt"],
}
env = {"PKG_CONFIG_PATH": "/usr/lib/motif-on-qt/pkgconfig"}
# the static library is not LTO
options = ["!lto"]


# starts the toolkit and prints the build: Motif, Xbae, T1lib
def check(self):
    self.do(
        "sh",
        "-c",
        "./src/xmgrace -version | grep -q 'Motif Version'",
        env={
            "QT_QPA_PLATFORM": "offscreen",
            "GRACE_HOME": str(self.chroot_cwd),
        },
    )


# FHS places, as Debian has them: programs in /usr/bin (no ELF files in
# /usr/share), the grace_np library and header in /usr/lib and /usr/include
def post_install(self):
    g = "usr/share/grace"
    self.install_dir("usr/bin")
    for b in ["xmgrace", "convcal", "fdf2fit"]:
        self.mv(self.destdir / g / "bin" / b, self.destdir / "usr/bin")
    self.install_link("usr/bin/gracebat", "xmgrace")
    self.install_link("usr/bin/grace", "xmgrace")
    self.uninstall(f"{g}/bin")
    self.install_dir("usr/lib")
    self.mv(self.destdir / g / "lib/libgrace_np.a", self.destdir / "usr/lib")
    self.uninstall(f"{g}/lib")
    self.install_dir("usr/include")
    self.mv(
        self.destdir / g / "include/grace_np.h", self.destdir / "usr/include"
    )
    self.uninstall(f"{g}/include")
    for m in ["grace", "xmgrace", "gracebat", "convcal"]:
        self.install_man(f"doc/{m}.1")
