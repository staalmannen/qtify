# RPM spec for Fedora and openSUSE.
# Build: rpmbuild -ba --undefine=_disable_source_fetch transmission-gtk-qtify.spec

Name:           transmission-gtk-qtify
Version:        3.00
Release:        1%{?dist}
Summary:        Transmission, the BitTorrent client (GTK interface), built on Qt with GTK made Qt
License:        GPL-2.0-or-later
URL:            https://transmissionbt.com/
# Debian's copy of the release
Source0:        https://deb.debian.org/debian/pool/main/t/transmission/transmission_%{version}.orig.tar.xz

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  intltool
BuildRequires:  gettext
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(libevent)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  gtk-made-qt-devel
Provides:       transmission-gtk = %{version}-%{release}
Conflicts:      transmission-gtk
# the application icons, transmission-remote, the daemon, the web interface
Recommends:     transmission-common

%description
Transmission is a BitTorrent client. This package builds its unmodified
GTK interface against GTK made Qt: it runs as a Qt application without GTK.

%prep
%autosetup -n transmission-%{version}

%build
# 2020 GTK code passes some objects with the wrong pointer type, which
# GCC 14 rejects by default; gtk-made-qt-env puts its own -L in front of LDFLAGS
export CFLAGS="%{optflags} -Wno-error=incompatible-pointer-types" LDFLAGS="%{?build_ldflags}"
eval "$(gtk-made-qt-env)"
%configure --with-gtk --disable-cli --disable-daemon --disable-mac
%make_build

%install
# the GTK client and its translations; the icons are transmission-common's
make -C gtk DESTDIR=%{buildroot} install
make -C po DESTDIR=%{buildroot} install
rm %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/transmission.svg
rm %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/transmission-devel.svg
rm %{buildroot}%{_datadir}/icons/hicolor/symbolic/apps/transmission-symbolic.svg
%find_lang transmission-gtk

%check
./gtk/transmission-gtk --version 2>&1 | grep -q 'transmission-gtk 3.00'
# the main window, headless, on a scratch profile
mkdir -p check-home/transmission
echo '{ "user-has-given-informed-consent": true }' > check-home/transmission/settings.json
XDG_CONFIG_HOME=$PWD/check-home QT_QPA_PLATFORM=offscreen GTKQT_AUTOQUIT=1500 ./gtk/transmission-gtk

%files -f transmission-gtk.lang
%license COPYING
%doc AUTHORS NEWS.md README.md
%{_bindir}/transmission-gtk
%{_datadir}/applications/transmission-gtk.desktop
%{_datadir}/appdata/transmission-gtk.appdata.xml
%{_datadir}/pixmaps/transmission.png
%{_mandir}/man1/transmission-gtk.1*

%changelog
* Thu Nov 26 2026 staalmannen <staal1978@gmail.com> - 3.00-1
- Transmission 3.00 (GTK interface) built against GTK made Qt
