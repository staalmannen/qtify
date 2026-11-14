#!/usr/bin/env python3
"""Move a library's pinned snapshot to another commit in every recipe.

usage: tools/repin.py <package dir> <git clone> <commit> [<changelog note>]

  tools/repin.py gtk-made-qt ~/src/gtk-made-qt ee24bf3 "Qt 6.11 build fix"

Updates APKBUILD (_commit, pkgver, sha512sums), chimera/template.py
(_commit, pkgver, sha256), the .spec (commit, snapdate, %changelog),
debian/changelog and debian/qtify-source. The checksums are those of
GitHub's archive of the commit, which `git archive | gzip -n` reproduces.
The snapshot date is the commit's date. The PKGBUILD follows the default
branch and is not touched.
"""
import datetime, glob, hashlib, os, re, subprocess, sys

if len(sys.argv) < 4:
    sys.exit(__doc__)
pkgdir, clone, rev = sys.argv[1:4]
note = sys.argv[4] if len(sys.argv) > 4 else ""

commit = subprocess.check_output(["git", "-C", clone, "rev-parse", rev + "^{commit}"], text=True).strip()
short = commit[:7]
stamp = int(subprocess.check_output(["git", "-C", clone, "show", "-s", "--format=%ct", commit], text=True))
date = datetime.datetime.fromtimestamp(stamp, datetime.timezone.utc)
snap = date.strftime("%Y%m%d")

# the repository name GitHub uses as the archive's top directory
src = open(os.path.join(pkgdir, "debian", "qtify-source")).read()
repo = re.search(r"github\.com/[^/]+/([^/]+)/archive/", src).group(1)
tar = subprocess.check_output(["git", "-C", clone, "archive", "--format=tar", "--prefix=%s-%s/" % (repo, commit), commit])
data = subprocess.run(["gzip", "-cn"], input=tar, stdout=subprocess.PIPE, check=True).stdout
sha256 = hashlib.sha256(data).hexdigest()
sha512 = hashlib.sha512(data).hexdigest()


def update(path, subs):
    with open(path) as f:
        s = f.read()
    for pattern, repl in subs:
        s, n = re.subn(pattern, repl, s, count=1, flags=re.M)
        if not n:
            sys.exit("%s: no match for %s" % (path, pattern))
    with open(path, "w") as f:
        f.write(s)


update(os.path.join(pkgdir, "APKBUILD"), [
    (r"^_commit=\w+", "_commit=" + commit),
    (r"^pkgver=(\d[\w.]*?)_git\d+", r"pkgver=\g<1>_git" + snap),
    (r"^[0-9a-f]{128}  (\S+)-[0-9a-f]{40}\.tar\.gz", r"%s  \g<1>-%s.tar.gz" % (sha512, commit)),
])
update(os.path.join(pkgdir, "chimera", "template.py"), [
    (r'^_commit = "\w+"', '_commit = "%s"' % commit),
    (r'^pkgver = "(\d[\w.]*?)_git\d+"', r'pkgver = "\g<1>_git%s"' % snap),
    (r'^sha256 = "[0-9a-f]+"', 'sha256 = "%s"' % sha256),
])
spec = glob.glob(os.path.join(pkgdir, "*.spec"))[0]
with open(spec) as f:
    s = f.read()
version = re.search(r"^Version:\s*(\S+?)\+git", s, re.M).group(1)
name = re.search(r"^Name:\s*(\S+)", s, re.M).group(1)
entry = "* %s staalmannen <https://github.com/staalmannen/qtify> - %s+git%s.%s-1\n- Snapshot of %s at %s%s\n\n" % (
    date.strftime("%a %b %d %Y"), version, snap, short, name, short, (" (" + note + ")") if note else "")
update(spec, [
    (r"^%global commit \w+", "%global commit " + commit),
    (r"^%global snapdate \d+", "%global snapdate " + snap),
    (r"^%changelog\n", "%changelog\n" + entry),
])
update(os.path.join(pkgdir, "debian", "qtify-source"), [
    (r"/archive/\w+\.tar\.gz", "/archive/%s.tar.gz" % commit),
    (r"^SOURCE_SHA256=\w+", "SOURCE_SHA256=" + sha256),
])
cl = os.path.join(pkgdir, "debian", "changelog")
with open(cl) as f:
    old = f.read()
src_name = old.split(" ", 1)[0]
url = re.search(r"https://github\.com/\S+?/archive/", src).group(0)[: -len("/archive/")]
text = "Snapshot of %s at %s%s." % (url, short, (" (" + note + ")") if note else "")
lines, line = [], "  *"
for word in text.split():
    if len(line) + 1 + len(word) > 76:
        lines.append(line)
        line = "   "
    line += " " + word
lines.append(line)
with open(cl, "w") as f:
    f.write("%s (%s+git%s.%s-1) unstable; urgency=medium\n\n%s\n\n -- staalmannen <https://github.com/staalmannen/qtify>  %s\n\n" % (
        src_name, version, snap, short, "\n".join(lines), date.strftime("%a, %d %b %Y %H:%M:%S +0000")) + old)
print("%s: %s (%s, sha256 %s)" % (pkgdir, commit, snap, sha256))
