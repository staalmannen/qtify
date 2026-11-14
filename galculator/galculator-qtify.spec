# RPM spec for Fedora and openSUSE.
# Build: rpmbuild -ba --undefine=_disable_source_fetch galculator-qtify.spec

Name:           galculator-qtify
Version:        2.1.4
Release:        1%{?dist}
Summary:        Galculator, the GTK scientific calculator, built on Qt with GTK made Qt
License:        GPL-2.0-or-later
URL:            http://galculator.mnim.org/
# Debian's copy of the release (without the generated configure)
Source0:        https://deb.debian.org/debian/pool/main/g/galculator/galculator_%{version}.orig.tar.gz

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  intltool
BuildRequires:  gettext
BuildRequires:  flex
BuildRequires:  pkgconfig
BuildRequires:  gtk-made-qt-devel
Provides:       galculator = %{version}-%{release}
Conflicts:      galculator

%description
Galculator is a scientific calculator with algebraic, RPN and formula
modes, number bases, user constants and functions. This package builds its
unmodified GTK source against GTK made Qt: it runs as a Qt application
without GTK.

%prep
%autosetup -n galculator-%{version}

%build
mkdir -p m4
intltoolize --force
autoreconf -fi
# gnu17 and -fcommon: 2016 C (Debian patches the source for the same);
# gtk-made-qt-env puts its own -L in front of LDFLAGS
export CFLAGS="%{optflags} -std=gnu17 -fcommon" LDFLAGS="%{?build_ldflags}"
eval "$(gtk-made-qt-env)"
%configure
%make_build

%install
%make_install
%find_lang galculator

%check
# starts the toolkit; the window needs the installed interface files
QT_QPA_PLATFORM=offscreen ./src/galculator -v | grep -q 'galculator v2'


%files -f galculator.lang
%license COPYING
%doc AUTHORS ChangeLog NEWS README THANKS
%{_bindir}/galculator
%{_datadir}/applications/galculator.desktop
%{_datadir}/appdata/galculator.appdata.xml
%{_datadir}/galculator/
%{_datadir}/icons/hicolor/*/apps/galculator.*
%{_datadir}/pixmaps/galculator.xpm
%{_mandir}/man1/galculator.1*

%changelog
* Sat Nov 14 2026 staalmannen <staal1978@gmail.com> - 2.1.4-1
- Galculator 2.1.4 built against GTK made Qt
