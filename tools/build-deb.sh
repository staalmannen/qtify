#!/bin/sh
# Build a qtify package for Debian / Ubuntu:
#   tools/build-deb.sh <package dir> [<work dir>]
# Downloads the source named in <package>/debian/qtify-source, checks its
# SHA-256, adds the debian/ directory and runs dpkg-buildpackage. Extra
# sources are component tarballs: SOURCE_COMPONENTS="a b" with
# SOURCE_URL_a / SOURCE_SHA256_a ..., unpacked into the directories a, b
# (they become <source>_<version>.orig-a.tar.* for dpkg-source). The .deb
# files end up in the work dir (default: ./build-deb). Install the build
# dependencies first: apt build-dep <package dir>/  (or mk-build-deps).
set -eu
pkgdir=$(cd "${1:?usage: $0 <package dir> [work dir]}" && pwd)
work=${2:-build-deb}
mkdir -p "$work"; work=$(cd "$work" && pwd)
SOURCE_URL= SOURCE_SHA256= SOURCE_COMPONENTS=
. "$pkgdir/debian/qtify-source"
src=$(dpkg-parsechangelog -l "$pkgdir/debian/changelog" -S Source)
ver=$(dpkg-parsechangelog -l "$pkgdir/debian/changelog" -S Version)
upver=${ver#*:}; upver=${upver%-*}
case "$SOURCE_URL" in
  *.tar.xz) ext=xz ;; *.tar.bz2) ext=bz2 ;; *) ext=gz ;;
esac
fetch() {  # fetch <url> <file> <sha256>
  [ -f "$2" ] || curl -fL -o "$2" "$1"
  if [ -n "$3" ]; then
    echo "$3  $2" | sha256sum -c -
  else
    echo "warning: no checksum for $1 in $pkgdir/debian/qtify-source; got $(sha256sum "$2" | cut -d' ' -f1)" >&2
  fi
}
tarext() {
  case "$1" in *.tar.xz) echo xz ;; *.tar.bz2) echo bz2 ;; *) echo gz ;; esac
}
orig="$work/${src}_${upver}.orig.tar.$ext"
fetch "$SOURCE_URL" "$orig" "$SOURCE_SHA256"
tree="$work/$src-$upver"
rm -rf "$tree"; mkdir -p "$tree"
tar -xf "$orig" -C "$tree" --strip-components=1
for c in $SOURCE_COMPONENTS; do
  eval "curl_url=\$SOURCE_URL_$c sum=\$SOURCE_SHA256_$c"
  corig="$work/${src}_${upver}.orig-$c.tar.$(tarext "$curl_url")"
  fetch "$curl_url" "$corig" "$sum"
  mkdir -p "$tree/$c"
  tar -xf "$corig" -C "$tree/$c" --strip-components=1
done
cp -r "$pkgdir/debian" "$tree/"
for f in "$pkgdir"/*.desktop; do [ -f "$f" ] && cp "$f" "$tree/debian/"; done
rm -f "$tree/debian/qtify-source"
cd "$tree"
dpkg-buildpackage -us -uc ${DPKG_BUILDPACKAGE_OPTS:-}
ls -1 "$work"/*.deb
