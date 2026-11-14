# RPM spec for Fedora and openSUSE.
# Build: rpmbuild -ba --undefine=_disable_source_fetch xpdf-qtify.spec
%global debver 3.04+git20260802

Name:           xpdf-qtify
Version:        3.04.git20260802
Release:        1%{?dist}
Summary:        xpdf 3 (the Motif PDF viewer, Poppler based) built on Qt with Motif on Qt
License:        GPL-2.0-only OR GPL-3.0-only
URL:            https://tracker.debian.org/pkg/xpdf
Source0:        https://deb.debian.org/debian/pool/main/x/xpdf/xpdf_%{debver}.orig.tar.xz

BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  pkgconfig
BuildRequires:  motif-on-qt-devel
BuildRequires:  pkgconfig(poppler)
Provides:       xpdf = %{version}-%{release}
Conflicts:      xpdf

%description
xpdf 3.04 as Debian maintains it (xpopple: the xpdf viewer on Poppler),
built from its unmodified Motif source against Motif on Qt: it runs as a
Qt application without libXm, libXt or libX11.

%prep
%autosetup -n xpdf-%{debver}

%build
autoreconf -fi
# motif-on-qt-env puts its own -I and -L in front of these
export CPPFLAGS="" LDFLAGS="%{?build_ldflags}"
# poppler 25 headers use C++20 (std::span, string::ends_with)
export CXXFLAGS="%{optflags} -std=gnu++20"
eval "$(motif-on-qt-env)"
%configure
%make_build

%install
%make_install

%check
# -v prints the version and exits with status 99 (xpdf's convention)
QT_QPA_PLATFORM=offscreen ./xpdf/xpdf -v 2>&1 | grep -q 'version 3'

%files
%license COPYING COPYING3
%doc README
%{_bindir}/xpdf
%{_mandir}/man1/xpdf.1*
%{_mandir}/man5/xpdfrc.5*

%changelog
* Sat Nov 14 2026 staalmannen <staal1978@gmail.com> - 3.04.git20260802-1
- Debian's xpdf snapshot of 2026-08-02: builds with poppler 25 (C++20)

* Thu Nov 12 2026 staalmannen <staal1978@gmail.com> - 3.04.git20240202-1
- xpdf 3.04+git20240202 (Debian's orig tarball) built against Motif on Qt
