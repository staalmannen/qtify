# RPM spec for Fedora and openSUSE.
# Build: rpmbuild -ba --undefine=_disable_source_fetch motif-on-qt.spec
%global commit 421a6489817d78aee3d8f5776026d3bb785f09f6
%global shortcommit %(echo %{commit} | cut -c1-7)
%global snapdate 202611140548
# The static archive must not hold LTO objects: programs link it with
# whatever compiler they use.
%global _lto_cflags %{nil}
# only a static library: nothing to extract debug info from
%global debug_package %{nil}

Name:           motif-on-qt
Version:        0.1+git%{snapdate}.%{shortcommit}
Release:        1%{?dist}
Summary:        The Motif, Xt and Xlib C APIs on Qt 6
License:        LGPL-2.1-or-later AND MIT
URL:            https://github.com/staalmannen/qtmotifextension
Source0:        %{url}/archive/%{commit}/qtmotifextension-%{commit}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  pkgconfig
BuildRequires:  cmake(Qt6Widgets)

%description
Motif on Qt implements the Xt/Motif C API, and the part of Xlib Motif
programs use, on Qt 6: Motif programs compile unmodified and run as Qt
applications, without X11 or libXm.

%package devel
Summary:        Headers, static library and build wrapper for Motif on Qt
Requires:       cmake(Qt6Widgets)
Requires:       pkgconfig

%description devel
Headers, the static library, linker scripts and pkg-config files for
-lXm -lXt -lX11, and the motif-on-qt-env wrapper: run a program's build
under motif-on-qt-env to build it against Motif on Qt.

%prep
%autosetup -n qtmotifextension-%{commit}

%build
cmake -B build -S . \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_C_FLAGS_RELEASE="%{optflags}" \
    -DCMAKE_CXX_FLAGS_RELEASE="%{optflags}" \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DCMAKE_INSTALL_LIBDIR=%{_lib} \
    -DMQ_BUILD_EXAMPLES=OFF
cmake --build build %{?_smp_mflags}

%install
DESTDIR=%{buildroot} cmake --install build
rm -rf %{buildroot}%{_datadir}/doc/%{name}

%files devel
%license LICENSE.LGPL
%doc README.md
%{_bindir}/motif-on-qt-env
%{_includedir}/motif-on-qt/
%{_libdir}/motif-on-qt/
%{_libdir}/pkgconfig/motif-on-qt.pc

%changelog
* Sat Nov 14 2026 staalmannen <https://github.com/staalmannen/qtify> - 0.1+git202611140548.421a648-1
- Snapshot of motif-on-qt at 421a648 (headers compile as C++17 with clang; links with libc++)

* Sat Nov 14 2026 staalmannen <https://github.com/staalmannen/qtify> - 0.1+git20261114.491b66c-1
- Snapshot of motif-on-qt at 491b66c (builds on musl and Qt 6.11; no build directory in the tree)

* Fri Nov 13 2026 staalmannen <https://github.com/staalmannen/qtify> - 0.1+git20261113.249a95f-1
- Snapshot of qtmotifextension at 249a95f
