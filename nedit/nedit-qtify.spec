# RPM spec for Fedora and openSUSE.
# Build: rpmbuild -ba --define "_sourcedir $PWD" --undefine=_disable_source_fetch nedit-qtify.spec

Name:           nedit-qtify
Version:        5.7
Release:        1%{?dist}
Summary:        NEdit, the classic Motif programmer's editor, built on Qt with Motif on Qt
License:        GPL-2.0-or-later
URL:            https://sourceforge.net/projects/nedit/
Source0:        https://downloads.sourceforge.net/project/nedit/nedit-source/nedit-%{version}-src.tar.gz
Source1:        nedit.desktop

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  motif-on-qt-devel
BuildRequires:  /usr/bin/pod2man
Provides:       nedit = %{version}-%{release}
Conflicts:      nedit

%description
NEdit 5.7 built from its unmodified Motif source against Motif on Qt: it
runs as a Qt application (X11 or Wayland) without libXm, libXt or libX11.
Syntax highlighting, tabs, macros, shell commands and the nedit-nc client
are included.

%prep
%autosetup -n nedit-%{version}

%build
# NEdit's makefiles set CFLAGS and LIBS themselves: the paths from
# motif-on-qt-env go on the command line. gnu17: NEdit's code is not C23.
export CPPFLAGS="" LDFLAGS="%{?build_ldflags}"
eval "$(motif-on-qt-env)"
make linux CFLAGS="%{optflags} -std=gnu17 $CPPFLAGS -DUSE_DIRENT -DUSE_LPR_PRINT_CMD" \
    LIBS="$LDFLAGS -lXm -lXt -lX11 -lm"
pod2man --section=1 --center=NEdit --release="NEdit %{version}" doc/nedit.pod > nedit.1
pod2man --section=1 --center=NEdit --release="NEdit %{version}" --name=nedit-nc doc/nc.pod > nedit-nc.1

%install
# no install target; nc is netcat's name: NEdit's client is nedit-nc
install -Dm755 source/nedit %{buildroot}%{_bindir}/nedit
install -Dm755 source/nc %{buildroot}%{_bindir}/nedit-nc
install -Dm644 nedit.1 %{buildroot}%{_mandir}/man1/nedit.1
install -Dm644 nedit-nc.1 %{buildroot}%{_mandir}/man1/nedit-nc.1
install -Dm644 %{SOURCE1} %{buildroot}%{_datadir}/applications/nedit.desktop

%check
HOME=$PWD/test-home QT_QPA_PLATFORM=offscreen MOTIFQT_AUTOQUIT=1500 ./source/nedit

%files
%license COPYRIGHT
%doc README ReleaseNotes
%{_bindir}/nedit
%{_bindir}/nedit-nc
%{_mandir}/man1/nedit.1*
%{_mandir}/man1/nedit-nc.1*
%{_datadir}/applications/nedit.desktop

%changelog
* Fri Nov 13 2026 staalmannen <staal1978@gmail.com> - 5.7-1
- NEdit 5.7 built against Motif on Qt
