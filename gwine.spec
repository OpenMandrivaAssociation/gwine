%define name gwine
%define version 0.10.3
%define release %mkrel 4

Summary:	A Gnome application to manage your wine cellar
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	http://download.gna.org/gwine/%{name}-%{version}.tar.bz2
License:	GPL
Group:		Databases
Url:		http://home.gna.org/gwine/index
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch:	noarch
BuildRequires:	ImageMagick
BuildRequires:	scrollkeeper desktop-file-utils 
BuildRequires:	perl-Gtk2-GladeXML perl-Gnome2-GConf perl-Gnome2 perl-Locale-gettext
Requires:	perl-Gtk2-GladeXML perl-Gnome2-GConf perl-Gnome2 perl-Locale-gettext
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

perl -pi -e 's,%{name}.png,%{name},g' %{buildroot}%{_datadir}/applications/*

rm -f $RPM_BUILD_ROOT%{_datadir}/applications/mimeinfo.cache

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --remove-category="Accessories" \
  --add-category="Database;Office" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*

mkdir -p $RPM_BUILD_ROOT%{_liconsdir} $RPM_BUILD_ROOT%{_iconsdir} $RPM_BUILD_ROOT%{_miconsdir}
convert -geometry 48x48 pixmaps/%{name}.png $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png
convert -geometry 32x32 pixmaps/%{name}.png $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
convert -geometry 16x16 pixmaps/%{name}.png $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png

%find_lang %name

rm -rf $RPM_BUILD_ROOT%{_localestatedir}/lib/scrollkeeper
rm -rf $RPM_BUILD_ROOT%{_datadir}/mime

#manually move omf files, they've a strange default location
mkdir -p $RPM_BUILD_ROOT%{_datadir}/omf/%{name}
mv $RPM_BUILD_ROOT/gwine/* $RPM_BUILD_ROOT%{_datadir}/omf/%{name}/

%clean
rm -rf $RPM_BUILD_ROOT

%if %mdkversion < 200900
%post
%update_menus
%update_scrollkeeper
%update_desktop_database
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%clean_scrollkeeper
%clean_desktop_database
%endif

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
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_miconsdir}/%{name}.png

