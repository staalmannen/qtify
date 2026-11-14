# RPM spec for Fedora and openSUSE.
# Build: rpmbuild -ba --undefine=_disable_source_fetch leafpad-qtify.spec
%global commit 3b1a2c2a1fad10f7f03e9b240bb6fa425aed5417

Name:           leafpad-qtify
Version:        0.8.19
Release:        1%{?dist}
Summary:        Leafpad (the GTK 2 text editor) built on Qt with GTK made Qt
License:        GPL-2.0-or-later
URL:            https://github.com/tarot231/leafpad
Source0:        %{url}/archive/%{commit}/leafpad-%{commit}.tar.gz

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  intltool
BuildRequires:  gettext
BuildRequires:  pkgconfig
BuildRequires:  gtk-made-qt-devel
Provides:       leafpad = %{version}-%{release}
Conflicts:      leafpad

%description
Leafpad is a simple, fast text editor. This package builds its unmodified
GTK 2 source against GTK made Qt: it runs as a Qt application without
GTK 2.

%prep
%autosetup -n leafpad-%{commit}

%build
intltoolize --force
autoreconf -fi
# gtk-made-qt-env puts its own -L in front of LDFLAGS
export LDFLAGS="%{?build_ldflags}"
eval "$(gtk-made-qt-env)"
%configure
%make_build

%install
%make_install
%find_lang leafpad

%check
QT_QPA_PLATFORM=offscreen GTKQT_AUTOQUIT=1000 ./src/leafpad

%files -f leafpad.lang
%license COPYING
%doc AUTHORS NEWS README
%{_bindir}/leafpad
%{_datadir}/applications/leafpad.desktop
%{_datadir}/icons/hicolor/*/apps/leafpad.*
%{_datadir}/pixmaps/leafpad.*
%{_mandir}/man1/leafpad.1*

%changelog
* Thu Nov 12 2026 staalmannen <staal1978@gmail.com> - 0.8.19-1
- Leafpad 0.8.19 (tarot231/leafpad 3b1a2c2) built against GTK made Qt
