# RPM spec for Fedora and openSUSE.
# Build: rpmbuild -ba --undefine=_disable_source_fetch ddd-qtify.spec

Name:           ddd-qtify
Version:        3.4.1
Release:        1%{?dist}
Summary:        DDD, the GNU Data Display Debugger, built on Qt with Motif on Qt
License:        GPL-3.0-or-later
URL:            https://www.gnu.org/software/ddd/
# Debian's copy of the release
Source0:        https://deb.debian.org/debian/pool/main/d/ddd/ddd_%{version}.orig.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  flex
BuildRequires:  bison
BuildRequires:  ncurses-devel
BuildRequires:  motif-on-qt-devel
Requires:       gdb
Provides:       ddd = %{version}-%{release}
Conflicts:      ddd

%description
DDD, the GNU Data Display Debugger, is a graphical front end for gdb and
other command-line debuggers, with a source window, a debugger console and
a graph of data displays. This package builds its unmodified Motif and
Athena source against Motif on Qt: it runs as a Qt application without
libXm, libXaw, libXt or libX11.

%prep
%autosetup -n ddd-%{version}

%build
# no Xft: it would pull in the system's libX11 (fonts come from Qt);
# motif-on-qt-env puts its own -L in front of LDFLAGS
export LDFLAGS="%{?build_ldflags}" ac_cv_lib_Xft_XftFontOpen=no
eval "$(motif-on-qt-env)"
%configure
%make_build

%install
%make_install

%check
mkdir -p home
HOME=$PWD/home QT_QPA_PLATFORM=offscreen ./ddd/ddd --version | grep -q 'GNU DDD 3.4'

%files
%license doc/COPYING
%doc doc/AUTHORS README
%{_bindir}/ddd
%{_datadir}/ddd-%{version}/
%{_datadir}/applications/ddd.desktop
%{_mandir}/man1/ddd.1*

%changelog
* Sat Nov 14 2026 staalmannen <staal1978@gmail.com> - 3.4.1-1
- DDD 3.4.1 built against Motif on Qt
