# RPM spec for Fedora and openSUSE.
# Build: rpmbuild -ba --undefine=_disable_source_fetch asunder-qtify.spec

Name:           asunder-qtify
Version:        3.0.1
Release:        1%{?dist}
Summary:        Asunder, the GTK 2 CD ripper and encoder, built on Qt with GTK made Qt
License:        GPL-2.0-or-later
URL:            http://littlesvr.ca/asunder/
# Debian's copy of the release (+ds: without the generated configure)
Source0:        https://deb.debian.org/debian/pool/main/a/asunder/asunder_%{version}+ds.orig.tar.xz

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  intltool
BuildRequires:  gettext
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(libcddb)
BuildRequires:  gtk-made-qt-devel
Requires:       cdparanoia
Provides:       asunder = %{version}-%{release}
Conflicts:      asunder

%description
Asunder rips audio CDs and encodes them to WAV, MP3, Ogg Vorbis, Opus,
FLAC and more, with CDDB lookup. This package builds its unmodified GTK 2
source against GTK made Qt: it runs as a Qt application without GTK 2.
The encoders are found at run time (lame, oggenc, flac, opusenc ...).

%prep
%autosetup -n asunder-%{version}

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
%find_lang asunder

%check
mkdir -p test-home/.config
HOME=$PWD/test-home QT_QPA_PLATFORM=offscreen GTKQT_AUTOQUIT=1500 ./src/asunder

%files -f asunder.lang
%license COPYING
%doc AUTHORS ChangeLog NEWS README
%{_bindir}/asunder
%{_datadir}/applications/asunder.desktop
%{_datadir}/pixmaps/asunder.*

%changelog
* Fri Nov 13 2026 staalmannen <https://github.com/staalmannen/qtify> - 3.0.1-1
- Asunder 3.0.1 built against GTK made Qt
