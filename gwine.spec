%define name gwine
%define version 0.10.3
%define release %mkrel 1

Summary: A Gnome application to manage your wine cellar
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://download.gna.org/gwine/%{name}-%{version}.tar.bz2
License: GPL
Group: Databases
Url: http://home.gna.org/gwine/index
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch: noarch
BuildRequires:	ImageMagick
BuildRequires: scrollkeeper
Requires(post): scrollkeeper
Requires(post): shared-mime-info
Requires(postun): scrollkeeper
Requires(postun): shared-mime-info

%define _requires_exceptions 'perl(Gwine::.*)'

%description
Gwine is a Gnome application to manage your wine cellar.

%prep
%setup -q

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make
make test

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT PREFIX=%{_prefix} XDG_DATA_DIRS=$RPM_BUILD_ROOT%{_datadir}

install -d $RPM_BUILD_ROOT%{_menudir}
cat << EOF > $RPM_BUILD_ROOT%{_menudir}/%{name}
?package(%{name}): \
 command="%{_bindir}/%{name}" \
 needs="x11" \
 section="More Applications/Databases" \
 title="Gwine" \
 icon="%{name}.png" \
 longtitle="Manage your wine cellar"
EOF
mkdir -p $RPM_BUILD_ROOT%{_liconsdir} $RPM_BUILD_ROOT%{_iconsdir} $RPM_BUILD_ROOT%{_miconsdir}
convert -geometry 48x48 pixmaps/%{name}.png $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png
convert -geometry 32x32 pixmaps/%{name}.png $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
convert -geometry 16x16 pixmaps/%{name}.png $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png

%find_lang %name

rm -rf $RPM_BUILD_ROOT%{_var}/lib/scrollkeeper
rm -rf $RPM_BUILD_ROOT%{_datadir}/mime
rm -f $RPM_BUILD_ROOT%{_datadir}/applications/mimeinfo.cache

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_menus
if [ -x %{_bindir}/scrollkeeper-update ]; then %{_bindir}/scrollkeeper-update -q || true ; fi
%{_bindir}/update-mime-database %{_datadir}/mime >/dev/null

%postun
%clean_menus
if [ -x %{_bindir}/scrollkeeper-update ]; then %{_bindir}/scrollkeeper-update -q || true ; fi
%{_bindir}/update-mime-database %{_datadir}/mime >/dev/null

%files -f %name.lang
%defattr(-,root,root)
%{_bindir}/%{name}
%{perl_vendorlib}/*
%{_mandir}/*/*
%{_datadir}/%{name}
%{_datadir}/omf/%{name}
%{_datadir}/gnome/help/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
%{_menudir}/%{name}
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
