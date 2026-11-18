# RPM spec for Fedora and openSUSE.
# Build: rpmbuild -ba --undefine=_disable_source_fetch sylpheed-qtify.spec

Name:           sylpheed-qtify
Version:        3.7.0
Release:        1%{?dist}
Summary:        Sylpheed, the GTK 2 mail client, built on Qt with GTK made Qt
License:        GPL-2.0-or-later AND LGPL-2.1-or-later
URL:            https://sylpheed.sraoss.jp/
# Debian's copy of the release tarball
Source0:        https://deb.debian.org/debian/pool/main/s/sylpheed/sylpheed_%{version}.orig.tar.bz2

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  gettext
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(openssl)
BuildRequires:  gtk-made-qt-devel
Provides:       sylpheed = %{version}-%{release}
Conflicts:      sylpheed

%description
Sylpheed is a lightweight, fast e-mail client with an MH mailbox, POP3,
IMAP4 and SMTP (over TLS), filtering, junk mail control and an address
book. This package builds its unmodified GTK 2 source against GTK made Qt:
it runs as a Qt application without GTK.

%package devel
Summary:        Headers for Sylpheed plugins
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers and libraries for building Sylpheed plugins.

%prep
%autosetup -n sylpheed-%{version}

%build
# the shared toolkit: the plugin library calls GTK too;
# gtk-made-qt-env puts its own -L in front of LDFLAGS
# GCC 14 makes libsylph's pointer type mismatches (execute_async) errors
export CFLAGS="%{optflags} -Wno-error=incompatible-pointer-types" LDFLAGS="%{?build_ldflags}"
eval "$(gtk-made-qt-env --shared)"
%configure --disable-gtkspell --disable-gpgme --disable-compface --disable-rpath
%make_build

%install
%make_install
find %{buildroot} -name '*.la' -delete
%find_lang sylpheed

%check
# starts headless in an empty home (the first run dialog) and quits
mkdir -p test-home
HOME=$PWD/test-home LANG=C.UTF-8 QT_QPA_PLATFORM=offscreen GTKQT_AUTOQUIT=2000 ./src/sylpheed

%files -f sylpheed.lang
%license COPYING COPYING.LIB LICENSE
%doc AUTHORS NEWS README
%{_bindir}/sylpheed
%{_libdir}/libsylph-0.so.1*
%{_libdir}/libsylpheed-plugin-0.so.1*
%{_datadir}/applications/sylpheed.desktop
%{_datadir}/pixmaps/sylpheed.png
%{_datadir}/sylpheed/

%files devel
%{_includedir}/sylpheed/
%{_libdir}/libsylph-0.so
%{_libdir}/libsylpheed-plugin-0.so

%changelog
* Wed Nov 18 2026 staalmannen <staal1978@gmail.com> - 3.7.0-1
- Sylpheed 3.7.0 built against GTK made Qt
