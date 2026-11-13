pkgname = "nedit-qtify"
pkgver = "5.7"
pkgrel = 0
hostmakedepends = ["motif-on-qt", "perl"]
makedepends = ["motif-on-qt"]
provides = ["nedit=5.7"]
pkgdesc = "NEdit, the classic Motif programmer's editor, on Qt"
license = "GPL-2.0-or-later"
url = "https://sourceforge.net/projects/nedit"
source = f"$(SOURCEFORGE_SITE)/nedit/nedit-source/nedit-{pkgver}-src.tar.gz"
sha256 = "add9ac79ff973528ad36c86858238bac4f59896c27dbf285cbe6a4d425fca17a"
# motif-on-qt-env points at the build machine's library
options = ["!cross"]


# NEdit's makefiles set CFLAGS and LIBS themselves: the paths of Motif on
# Qt go on the command line. gnu17: NEdit's code is not C23.
def build(self):
    cflags = self.get_cflags(shell=True)
    ldflags = self.get_ldflags(shell=True)
    self.do(
        "make",
        "linux",
        f"CC={self.get_tool('CC')}",
        f"CFLAGS={cflags} -std=gnu17 -I/usr/include/motif-on-qt -DUSE_DIRENT -DUSE_LPR_PRINT_CMD",
        f"LIBS={ldflags} -L/usr/lib/motif-on-qt -lXm -lXt -lX11 -lm",
    )
    for name, pod in (("nedit", "nedit.pod"), ("nedit-nc", "nc.pod")):
        self.do(
            "sh",
            "-c",
            f"pod2man --section=1 --center=NEdit --release='NEdit {pkgver}' "
            f"--name={name} doc/{pod} > {name}.1",
        )


def check(self):
    self.do(
        "./source/nedit",
        env={
            "HOME": str(self.chroot_cwd / "test-home"),
            "QT_QPA_PLATFORM": "offscreen",
            "MOTIFQT_AUTOQUIT": "1500",
        },
    )


# no install target; nc is netcat's name: NEdit's client is nedit-nc
def install(self):
    self.install_bin("source/nedit")
    self.install_bin("source/nc", name="nedit-nc")
    self.install_man("nedit.1")
    self.install_man("nedit-nc.1")
    self.install_file(self.files_path / "nedit.desktop", "usr/share/applications")
