# RPM spec for Fedora and openSUSE.
# Build: rpmbuild -ba --undefine=_disable_source_fetch motif-on-qt.spec
%global commit 54dacc657de15e55f94274c4d454a4f9b69e6225
%global shortcommit %(echo %{commit} | cut -c1-7)
%global snapdate 202611141521
# The static archive must not hold LTO objects: programs link it with
# whatever compiler they use.
%global _lto_cflags %{nil}
# only a static library: nothing to extract debug info from
%global debug_package %{nil}

Name:           motif-on-qt
Version:        0.1+git%{snapdate}.%{shortcommit}
Release:        1%{?dist}
Summary:        The Motif, Athena, Xt and Xlib C APIs on Qt 6
License:        LGPL-2.1-or-later AND MIT
URL:            https://github.com/staalmannen/motif-on-qt
Source0:        %{url}/archive/%{commit}/motif-on-qt-%{commit}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  pkgconfig
BuildRequires:  cmake(Qt6Widgets)

%description
Motif on Qt implements the Xt/Motif C API, and the part of Xlib Motif
programs use, on Qt 6: Motif programs compile unmodified and run as Qt
applications, without X11 or libXm. The Athena widgets (libXaw), Xmu and
the Xpm API are included, so Athena programs and programs that mix Motif
with Athena widgets build too.

%package devel
Summary:        Headers, static library and build wrapper for Motif on Qt
Requires:       cmake(Qt6Widgets)
Requires:       pkgconfig

%description devel
Headers, the static library, linker scripts and pkg-config files for
-lXm -lXt -lX11, and the motif-on-qt-env wrapper: run a program's build
under motif-on-qt-env to build it against Motif on Qt.

%prep
%autosetup -n motif-on-qt-%{commit}

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
* Sat Nov 14 2026 staalmannen <staal1978@gmail.com> - 0.1+git202611141521.54dacc6-1
- Snapshot of motif-on-qt at 54dacc6 (Athena widgets, Xmu and Xpm; DDD support)

* Sat Nov 14 2026 staalmannen <staal1978@gmail.com> - 0.1+git202611140924.cfff583-1
- Snapshot of motif-on-qt at cfff583 (the repository is now motif-on-qt)

* Sat Nov 14 2026 staalmannen <staal1978@gmail.com> - 0.1+git202611140548.421a648-1
- Snapshot of motif-on-qt at 421a648 (headers compile as C++17 with clang; links with libc++)

* Sat Nov 14 2026 staalmannen <staal1978@gmail.com> - 0.1+git20261114.491b66c-1
- Snapshot of motif-on-qt at 491b66c (builds on musl and Qt 6.11; no build directory in the tree)

* Fri Nov 13 2026 staalmannen <staal1978@gmail.com> - 0.1+git20261113.249a95f-1
- Snapshot of motif-on-qt at 249a95f
