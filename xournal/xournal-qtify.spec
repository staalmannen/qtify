# RPM spec for Fedora and openSUSE.
# Build: rpmbuild -ba --undefine=_disable_source_fetch xournal-qtify.spec

%global artver 2.3.21
%global canvasver 2.30.3

Name:           xournal-qtify
Version:        0.4.8.2016
Release:        1%{?dist}
Summary:        Xournal, the GTK 2 note taker and PDF annotator, built on Qt with GTK made Qt
License:        GPL-2.0-or-later AND LGPL-2.0-or-later
URL:            https://xournal.sourceforge.net/
# Debian's copy of the Xournal release; libart and libgnomecanvas (for
# GTK 2, long gone from distributions) are built into the program
Source0:        https://deb.debian.org/debian/pool/main/x/xournal/xournal_%{version}.orig.tar.gz
Source1:        https://download.gnome.org/sources/libart_lgpl/2.3/libart_lgpl-%{artver}.tar.bz2
Source2:        https://download.gnome.org/sources/libgnomecanvas/2.30/libgnomecanvas-%{canvasver}.tar.bz2

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig
# libgnomecanvas's configure checks for intltool
BuildRequires:  intltool
BuildRequires:  pkgconfig(poppler-glib)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  gtk-made-qt-devel
Provides:       xournal = %{version}-%{release}
Conflicts:      xournal

%description
Xournal is an application for notetaking, sketching and keeping a journal
with a stylus or the mouse; it also annotates PDF files. This package
builds its unmodified GTK 2 source, with the libart and libgnomecanvas
libraries it draws with, against GTK made Qt: it runs as a Qt
application without GTK.

%prep
%setup -q -n xournal-%{version} -a 1 -a 2

%build
deps=$PWD/deps
# libart and libgnomecanvas: static, only for this build;
# gtk-made-qt-env puts its own -L in front of LDFLAGS
export LDFLAGS="%{?build_ldflags}"
(cd libart_lgpl-%{artver} &&
 ./configure --prefix=$deps --disable-shared --enable-static --with-pic &&
 %make_build && make install)
(cd libgnomecanvas-%{canvasver} &&
 PKG_CONFIG_PATH=$deps/lib/pkgconfig gtk-made-qt-env ./configure --prefix=$deps \
   --disable-nls --disable-shared --enable-static --with-pic &&
 %make_build && make install)
# the static library needs its private dependencies (gail, pangoft2)
sed -i 's/^Requires.private:/Requires:/' $deps/lib/pkgconfig/libgnomecanvas-2.0.pc
eval "$(gtk-made-qt-env)"
# GCC 14 makes ttsubset's implicit read/write/close declarations errors;
# I_det in xo-shapes.c is a GNU89 inline function
export CFLAGS="%{optflags} -Wno-error=implicit-function-declaration -fgnu89-inline"
export PKG_CONFIG_PATH="$PKG_CONFIG_PATH:$deps/lib/pkgconfig"
%configure
%make_build

%install
%make_install
# what upstream's desktop-install adds (without the KDE 3 mimelnk file)
install -Dm644 xournal.desktop %{buildroot}%{_datadir}/applications/xournal.desktop
install -Dm644 xournal.xml %{buildroot}%{_datadir}/mime/packages/xournal.xml
install -Dm644 pixmaps/xournal.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/xournal.svg
install -Dm644 pixmaps/xoj.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/mimetypes/application-x-xoj.svg
%find_lang xournal

%check
# starts headless with a new journal and quits
mkdir -p test-home
HOME=$PWD/test-home QT_QPA_PLATFORM=offscreen GTKQT_AUTOQUIT=2000 ./src/xournal

%files -f xournal.lang
%license COPYING
%doc AUTHORS ChangeLog README
%{_bindir}/xournal
%{_datadir}/xournal/
%{_datadir}/applications/xournal.desktop
%{_datadir}/mime/packages/xournal.xml
%{_datadir}/icons/hicolor/scalable/apps/xournal.svg
%{_datadir}/icons/hicolor/scalable/mimetypes/application-x-xoj.svg

%changelog
* Thu Nov 19 2026 staalmannen <staal1978@gmail.com> - 0.4.8.2016-1
- Xournal 0.4.8.2016 built against GTK made Qt, with libart 2.3.21 and libgnomecanvas 2.30.3
