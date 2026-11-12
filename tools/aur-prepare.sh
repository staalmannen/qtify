#!/bin/bash
# Prepare a qtify package for the AUR (run on Arch):
#   tools/aur-prepare.sh <package dir> [<directory for AUR checkouts>]
# Clones ssh://aur@aur.archlinux.org/<pkgname>.git (an empty repository is
# fine for a new package), copies the PKGBUILD and the local files it lists,
# writes .SRCINFO with makepkg and stages the changes. Nothing is committed or
# pushed: review, then  git commit  and  git push  in the checkout.
set -euo pipefail
pkgdir=$(cd "${1:?usage: $0 <package dir> [aur dir]}" && pwd)
aurdir=${2:-aur}
mkdir -p "$aurdir"; aurdir=$(cd "$aurdir" && pwd)
pkgname=$(cd "$pkgdir" && source ./PKGBUILD && echo "$pkgname")
co="$aurdir/$pkgname"
if [ -d "$co/.git" ]; then
  git -C "$co" pull --ff-only
else
  git clone "ssh://aur@aur.archlinux.org/$pkgname.git" "$co"
fi
cp "$pkgdir/PKGBUILD" "$co/"
# local sources: entries without a URL
for s in $(cd "$pkgdir" && source ./PKGBUILD && printf '%s\n' "${source[@]}"); do
  case "$s" in *://*) ;; *) cp "$pkgdir/${s#*::}" "$co/" ;; esac
done
(cd "$co" && makepkg --printsrcinfo > .SRCINFO && git add -A && git status --short)
echo "review $co, then: git -C $co commit -m '...' && git -C $co push"
