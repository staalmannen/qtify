# RPM spec for Fedora and openSUSE.
# Build: rpmbuild -ba --undefine=_disable_source_fetch grace-qtify.spec

Name:           grace-qtify
Version:        5.1.25
Release:        1%{?dist}
Summary:        Grace (xmgrace), the Motif 2D plotting tool, built on Qt with Motif on Qt
License:        GPL-2.0-or-later
URL:            https://plasma-gate.weizmann.ac.il/Grace/
# Debian's copy of the release; Grace's bundled Xbae and T1lib are used
Source0:        https://deb.debian.org/debian/pool/main/g/grace/grace_%{version}.orig.tar.gz

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  motif-on-qt-devel
Provides:       grace = %{version}-%{release}
Conflicts:      grace

%description
Grace is a WYSIWYG 2D plotting tool: line, scatter and bar plots, curve
fitting, transforms and publication quality output (PostScript, SVG, PNG
and more). This package builds its unmodified Motif source, with the Xbae
matrix widget it bundles, against Motif on Qt: it runs as a Qt
application without X11 or libXm.

%prep
%autosetup -n grace-%{version}

%build
# X headers and libraries are Motif on Qt's (configure would look for the
# system's X11); the first -I / -L of motif-on-qt-env are its own
eval "$(motif-on-qt-env)"
xinc=${CPPFLAGS%% *}; xlib=${LDFLAGS%% *}
# GCC 14 makes the implicit declarations of 2000-era code errors (and
# hardened builds T1lib's printf (model)); C23
# (GCC 15) reads its unprototyped functions as taking no arguments
export CFLAGS="%{optflags} -std=gnu17 -Wno-error=implicit-function-declaration -Wno-error=incompatible-pointer-types -Wno-error=int-conversion -Wno-error=implicit-int -Wno-error=format-security"
./configure --prefix=%{_prefix} --enable-grace-home=%{_datadir}/grace \
    --with-bundled-xbae --with-bundled-t1lib \
    --disable-pdfdrv --disable-netcdf --without-fftw --disable-xmhtml \
    --x-includes="${xinc#-I}" --x-libraries="${xlib#-L}"
%make_build

%install
make DESTDIR=%{buildroot} install
# FHS places, as Debian has them: programs in /usr/bin, the grace_np
# library and header in /usr/lib and /usr/include
g=%{buildroot}%{_datadir}/grace
install -d %{buildroot}%{_bindir} %{buildroot}%{_libdir} %{buildroot}%{_includedir} %{buildroot}%{_mandir}/man1
mv $g/bin/xmgrace $g/bin/convcal $g/bin/fdf2fit %{buildroot}%{_bindir}/
ln -s xmgrace %{buildroot}%{_bindir}/gracebat
ln -s xmgrace %{buildroot}%{_bindir}/grace
rm $g/bin/gracebat && rmdir $g/bin
mv $g/lib/libgrace_np.a %{buildroot}%{_libdir}/ && rmdir $g/lib
mv $g/include/grace_np.h %{buildroot}%{_includedir}/ && rmdir $g/include
for m in grace xmgrace gracebat convcal; do install -m644 doc/$m.1 %{buildroot}%{_mandir}/man1/; done

%check
# starts the toolkit and prints the build: Motif, Xbae, T1lib
QT_QPA_PLATFORM=offscreen GRACE_HOME=$PWD ./src/xmgrace -version | grep -q 'Motif Version'

%files
%license COPYRIGHT LICENSE
%doc README CHANGES
%{_bindir}/xmgrace
%{_bindir}/gracebat
%{_bindir}/grace
%{_bindir}/convcal
%{_bindir}/fdf2fit
%{_libdir}/libgrace_np.a
%{_includedir}/grace_np.h
%{_datadir}/grace/
%{_mandir}/man1/*.1*

%changelog
* Wed Nov 25 2026 staalmannen <staal1978@gmail.com> - 5.1.25-1
- Grace 5.1.25 built against Motif on Qt, with its bundled Xbae and T1lib
