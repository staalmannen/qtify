# RPM spec for Fedora and openSUSE.
# Build: rpmbuild -ba --undefine=_disable_source_fetch xmms-qtify.spec
%global commit 5847897230da018d93cd9833695f944ece96587b
# No LTO: the 2007 configure's function checks give false positives with
# it (it finds BSD's srandomdev on Linux).
%global _lto_cflags %{nil}
# plugins resolve xmms_* symbols from the player
%undefine _strict_symbol_defs_build

Name:           xmms-qtify
Version:        1.2.11
Release:        1%{?dist}
Summary:        XMMS, the GTK 1.2 audio player, built on Qt with GTK made Qt
License:        GPL-2.0-or-later
URL:            https://github.com/deepfire/xmms
Source0:        %{url}/archive/%{commit}/xmms-%{commit}.tar.gz
Source1:        xmms.desktop

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig
BuildRequires:  gtk-made-qt-devel
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(vorbis)
BuildRequires:  pkgconfig(ogg)
Provides:       xmms = %{version}-%{release}
Conflicts:      xmms

%description
The X MultiMedia System, the classic skinned audio player, built from its
unmodified GTK 1.2 source against GTK made Qt: it runs as a Qt application
(X11 or Wayland) without GTK 1.2 or libX11.

Includes the ALSA, OSS and disk writer output plugins; MP3, Ogg Vorbis,
WAV, CD audio and tone generator input; effect and visualization plugins.

%prep
%autosetup -n xmms-%{commit}
# time stamps as in a release tarball, so make does not rerun automake 1.x
find . -exec touch -h -d '2001-01-01 00:00' {} +
touch -d '2001-01-01 00:01' aclocal.m4
touch -d '2001-01-01 00:02' configure $(find . -name Makefile.in -o -name '*.h.in')

%build
# gtk-made-qt-env puts its own -L in front of LDFLAGS; the 2007 configure
# rejects some of the options %%configure passes, so it is called directly
# gnu17: GTK 1 era C (unprototyped callbacks, its own bool) is not C23;
# no tree vectorizer: GCC 14.2 crashes on the ALSA plugin with -ffast-math
export CFLAGS="%{optflags} -std=gnu17 -fno-tree-vectorize"
export LDFLAGS="%{?build_ldflags}"
eval "$(gtk-made-qt-env --shared)"
./configure --build=%{_build} --host=%{_host} --prefix=%{_prefix} \
    --libdir=%{_libdir} --mandir=%{_mandir} --sysconfdir=%{_sysconfdir} \
    --disable-dependency-tracking --disable-esd --disable-opengl \
    --disable-mikmod --disable-nls ac_cv_lib_SM_SmcOpenConnection=no
%make_build

%install
%make_install
find %{buildroot} -name '*.la' -delete
rm -f %{buildroot}%{_libdir}/libxmms.a
install -Dm644 %{SOURCE1} %{buildroot}%{_datadir}/applications/xmms.desktop

%check
# starts, shows its windows and quits
HOME=$PWD/test-home QT_QPA_PLATFORM=offscreen GTKQT_AUTOQUIT=1500 ./xmms/xmms

%files
%license COPYING
%doc AUTHORS NEWS README
%{_bindir}/xmms
%{_bindir}/wmxmms
%{_bindir}/xmms-config
%{_libdir}/libxmms.so*
%{_libdir}/xmms/
%{_includedir}/xmms/
%{_datadir}/aclocal/xmms.m4
%{_datadir}/xmms/
%{_mandir}/man1/*.1*
%{_datadir}/applications/xmms.desktop

%changelog
* Thu Nov 12 2026 staalmannen <staal1978@gmail.com> - 1.2.11-1
- XMMS 1.2.11 (deepfire/xmms 5847897) built against GTK made Qt
