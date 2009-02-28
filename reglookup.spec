Summary:	small utility for querying NT/2K/XP/2K3/Vista registries
Summary(pl.UTF-8):	proste narzędzie do odpytywania rejestrów NT/2K/XP/2K3/Vista
Name:		reglookup
Version:	0.10.0
Release:	1
License:	GPL v3
Group:		Applications
Source0:	http://projects.sentinelchicken.org/data/downloads/%{name}-%{version}.tar.gz
# Source0-md5:	67112df2798fc2d9539f2557ef38eb3d
URL:		http://projects.sentinelchicken.org/reglookup/
Patch0:		%{name}-DESTDIR.patch
Patch1:		%{name}-parallel-make.patch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
RegLookup is an small command line utility for reading and querying
Windows NT-based registries. RegLookup is released under the GNU GPL,
and is implemented in ANSI C. Original source was borrowed from the
program editreg, written by Richard Sharpe. It has since been
rewritten to use the regfio library, written by Gerald Carter.

Currently the program allows one to read an entire registry and output
it in a (mostly) standardized, quoted format. It also provides
features for filtering of results based on registry path and data
type.

%description -l pl.UTF-8
RegLookup to proste narzędzie do odczytywania i odpytywania rejestrów
systemów Windows serii NT. RegLookup jest udostępniony na zasadach
licencji GNU GPL i zaimplementowany w ANSI C. Źródła oparte są na
programie editreg, napisanym przez Richarda Sharpe. Od tamtej pory
program został przepisany z wykorzystaniem biblioteki regfio,
napisanej przez Geralda Cartera.

Obecnie program pozwala na odczyt rejestru i wypisania go w
ustandaryzowanym formacie. Możliwe jest także filtrowanie wyników na
podstawie ścieżek rejestru czy typów danych.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__make} \
	CC="%{__cc}" \
	OPTS="%{rpmcflags}" \
	INC="-I%{_includedir}" \
	LIB="-L%{_libdir} -lm"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	PREFIX=%{_prefix} \
	MAN_PREFIX="%{_mandir}" \
	DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT%{_mandir}/man1/\*
mv $RPM_BUILD_ROOT%{_docdir}/%{name}/man/man1/* $RPM_BUILD_ROOT%{_mandir}/man1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/reglookup*.1*
