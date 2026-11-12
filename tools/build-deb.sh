#!/bin/sh
# Build a qtify package for Debian / Ubuntu:
#   tools/build-deb.sh <package dir> [<work dir>]
# Downloads the source named in <package>/debian/qtify-source, checks its
# SHA-256, adds the debian/ directory and runs dpkg-buildpackage. The .deb
# files end up in the work dir (default: ./build-deb). Install the build
# dependencies first: apt build-dep <package dir>/  (or mk-build-deps).
set -eu
pkgdir=$(cd "${1:?usage: $0 <package dir> [work dir]}" && pwd)
work=${2:-build-deb}
mkdir -p "$work"; work=$(cd "$work" && pwd)
SOURCE_URL= SOURCE_SHA256=
. "$pkgdir/debian/qtify-source"
src=$(dpkg-parsechangelog -l "$pkgdir/debian/changelog" -S Source)
ver=$(dpkg-parsechangelog -l "$pkgdir/debian/changelog" -S Version)
upver=${ver#*:}; upver=${upver%-*}
case "$SOURCE_URL" in
  *.tar.xz) ext=xz ;; *.tar.bz2) ext=bz2 ;; *) ext=gz ;;
esac
orig="$work/${src}_${upver}.orig.tar.$ext"
[ -f "$orig" ] || curl -fL -o "$orig" "$SOURCE_URL"
if [ -n "$SOURCE_SHA256" ]; then
  echo "$SOURCE_SHA256  $orig" | sha256sum -c -
else
  echo "warning: no SOURCE_SHA256 in $pkgdir/debian/qtify-source; got $(sha256sum "$orig" | cut -d' ' -f1)" >&2
fi
tree="$work/$src-$upver"
rm -rf "$tree"; mkdir -p "$tree"
tar -xf "$orig" -C "$tree" --strip-components=1
cp -r "$pkgdir/debian" "$tree/"
for f in "$pkgdir"/*.desktop; do [ -f "$f" ] && cp "$f" "$tree/debian/"; done
rm -f "$tree/debian/qtify-source"
cd "$tree"
dpkg-buildpackage -us -uc ${DPKG_BUILDPACKAGE_OPTS:-}
ls -1 "$work"/*.deb
