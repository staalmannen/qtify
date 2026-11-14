# RPM spec for Fedora and openSUSE.
# Build: rpmbuild -ba --undefine=_disable_source_fetch gtk-made-qt.spec
%global commit 9d436125e6f070f06036e7a7397f2a8a46d665d9
%global shortcommit %(echo %{commit} | cut -c1-7)
%global snapdate 20261113
# The static archive must not hold LTO objects: programs link it with
# whatever compiler they use.
%global _lto_cflags %{nil}

Name:           gtk-made-qt
Version:        0.2.0+git%{snapdate}.%{shortcommit}
Release:        1%{?dist}
Summary:        The GTK 1.2/2/3/4 C API on Qt 6
License:        LGPL-2.1-or-later WITH static-linking-exception AND MIT
URL:            https://github.com/staalmannen/gtk-made-qt
Source0:        %{url}/archive/%{commit}/%{name}-%{commit}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  pkgconfig
BuildRequires:  cmake(Qt6Widgets)
BuildRequires:  cmake(Qt6PrintSupport)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(pangocairo)

%description
GTK made Qt implements the GTK C API on Qt, so GTK programs compile
unmodified as plain C and run as Qt applications, without GTK.

This package has the shared library, used by programs whose plugins call
GTK themselves (XMMS, for example). Most programs link the static library
from %{name}-devel and do not need it.

%package devel
Summary:        Development files for GTK made Qt (headers, static library, gtk-config)
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       cmake(Qt6Widgets)
Requires:       cmake(Qt6PrintSupport)
Requires:       pkgconfig(glib-2.0)
Requires:       pkgconfig(cairo)
Requires:       pkgconfig(pango)
Requires:       pkgconfig(pangocairo)
Requires:       pkgconfig

%description devel
Headers, the static library, pkg-config files for gtk+-2.0, gtk+-3.0, gtk4
and gtk+ (1.2), gtk-config and the gtk-made-qt-env wrapper: run a
program's build under gtk-made-qt-env to build it against GTK made Qt.

%prep
%autosetup -n %{name}-%{commit}

%build
cmake -B build -S . \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_C_FLAGS_RELEASE="%{optflags}" \
    -DCMAKE_CXX_FLAGS_RELEASE="%{optflags}" \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DCMAKE_INSTALL_LIBDIR=%{_lib} \
    -DGTKQT_BUILD_EXAMPLES=OFF \
    -DGTKQT_BUILD_TESTS=OFF
cmake --build build %{?_smp_mflags}

%install
DESTDIR=%{buildroot} cmake --install build
rm -rf %{buildroot}%{_datadir}/doc/%{name}

%files
%license COPYING
%{_libdir}/libgtk-made-qt.so.0*

%files devel
%doc README.md
%{_bindir}/gtk-made-qt-env
%{_includedir}/gtk-made-qt/
%{_libdir}/gtk-made-qt/
%{_libdir}/pkgconfig/*.pc

%changelog
* Fri Nov 13 2026 staalmannen <https://github.com/staalmannen/qtify> - 0.2.0+git20261113.9d43612-1
- Snapshot of gtk-made-qt at 9d43612 (Asunder support)

* Thu Nov 12 2026 staalmannen <https://github.com/staalmannen/qtify> - 0.2.0+git20261112.ff8aba1-1
- Snapshot of gtk-made-qt at ff8aba1
