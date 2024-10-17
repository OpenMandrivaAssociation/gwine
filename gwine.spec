%define name gwine
%define version 0.10.3
%define release 10

Summary:	A Gnome application to manage your wine cellar
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	http://download.gna.org/gwine/%{name}-%{version}.tar.bz2
License:	GPLv2+
Group:		Databases
Url:		https://home.gna.org/gwine/index
BuildArch:	noarch
BuildRequires:	imagemagick
BuildRequires:	scrollkeeper desktop-file-utils 
BuildRequires:	perl-Gtk2-GladeXML perl-Gnome2-GConf perl-Gnome2 perl-Locale-gettext
buildrequires:	perl-devel
buildrequires:	shared-mime-info
Requires:	perl-Gtk2-GladeXML perl-Gnome2-GConf perl-Gnome2 perl-Locale-gettext
Requires(post): scrollkeeper
Requires(post): shared-mime-info
Requires(postun): scrollkeeper
Requires(postun): shared-mime-info 

%define __noautoreq 'perl\\(Gwine::.*\\)'

%description
Gwine is a Gnome application to manage your wine cellar.

%prep
%setup -q

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make
make test

%install
make install DESTDIR=%{buildroot} PREFIX=%{_prefix} XDG_DATA_DIRS=%{buildroot}%{_datadir}

perl -pi -e 's,%{name}.png,%{name},g' %{buildroot}%{_datadir}/applications/*

rm -f %{buildroot}%{_datadir}/applications/mimeinfo.cache

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --remove-category="Accessories" \
  --add-category="Database;Office" \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

mkdir -p %{buildroot}%{_liconsdir} %{buildroot}%{_iconsdir} %{buildroot}%{_miconsdir}
convert -geometry 48x48 pixmaps/%{name}.png %{buildroot}%{_liconsdir}/%{name}.png
convert -geometry 32x32 pixmaps/%{name}.png %{buildroot}%{_iconsdir}/%{name}.png
convert -geometry 16x16 pixmaps/%{name}.png %{buildroot}%{_miconsdir}/%{name}.png

%find_lang %name

rm -rf %{buildroot}%{_localestatedir}/lib/scrollkeeper
rm -rf %{buildroot}%{_datadir}/mime

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



%changelog
* Sun Apr 17 2011 Funda Wang <fwang@mandriva.org> 0.10.3-8mdv2011.0
+ Revision: 654195
- rebuild for updated spec-helper

* Sun Dec 05 2010 Oden Eriksson <oeriksson@mandriva.com> 0.10.3-7mdv2011.0
+ Revision: 611052
- rebuild

* Thu Dec 31 2009 Jérôme Brenier <incubusss@mandriva.org> 0.10.3-6mdv2010.1
+ Revision: 484299
- drop manual move of omf files, they already are where they should be
- fix license tag
- $RPM_BUILD_ROOT -> %%{buildroot}

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - rebuild
    - kill re-definition of %%buildroot on Pixel's request

  + Oden Eriksson <oeriksson@mandriva.com>
    - lowercase ImageMagick

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Sun Sep 09 2007 Emmanuel Andry <eandry@mandriva.org> 0.10.3-2mdv2008.0
+ Revision: 83680
- xdg menu
- drop old menu
- fix buildrequires
- fix requires
- use mimetypes and scrollkeeper macros
- Import gwine



* Mon Jan 16 2006 Olivier Blin <oblin@mandriva.com> 0.10.3-1mdk
- initial release
