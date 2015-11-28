Summary:	small utility for querying NT/2K/XP/2K3/Vista registries
Summary(pl.UTF-8):	proste narzędzie do odpytywania rejestrów NT/2K/XP/2K3/Vista
Name:		reglookup
Version:	1.0.1
Release:	2
License:	GPL v3
Group:		Applications
Source0:	http://projects.sentinelchicken.org/data/downloads/%{name}-src-%{version}.tar.gz
# Source0-md5:	c451c2dba904db8ae5b0531ca303e322
Patch0:		%{name}-paths.patch
Patch1:		%{name}-soname.patch
URL:		http://projects.sentinelchicken.org/reglookup/
BuildRequires:	rpmbuild(macros) >= 1.385
BuildRequires:	scons
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

%package libs
Summary:	reglookup shared library
Summary(pl.UTF-8):	współdzielona biblioteka reglookup
Group:		Libraries

%description libs
reglookup shared library.

%description libs -l pl.UTF-8
współdzielona biblioteka reglookup.

%package devel
Summary:	Header files for reglookup library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki reglookup
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for reglookup library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki reglookup.

%package static
Summary:	Static reglookup library
Summary(pl.UTF-8):	Statyczna biblioteka reglookup
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static reglookup library.

%description static -l pl.UTF-8
Statyczna biblioteka reglookup.

%package -n python-pyregfi
Summary:	Python bindings for regfi library
Summary(pl.UTF-8):	Dowiązania pythona do blblioteki regfi
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description -n python-pyregfi
Python bindings for regfi library.

%description -n python-pyregfi -l pl.UTF-8
Dowiązania pythona do biblioteki regfi.

%prep
%setup -q -n %{name}-src-%{version}
%patch0 -p1
%patch1 -p1

%build
%scons

%install
rm -rf $RPM_BUILD_ROOT

DESTDIR=$RPM_BUILD_ROOT \
PREFIX="%{_prefix}" \
BINDIR="%{_bindir}" \
LIBDIR="%{_libdir}" \
MANDIR="%{_mandir}" \
INCLUDEDIR="%{_includedir}" \
%scons install

%{__python} pyregfi-distutils.py install \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

# fix soname
mv $RPM_BUILD_ROOT%{_libdir}/libregfi.so{,.%{version}}
ln -sf libregfi.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libregfi.so.1
ln -sf libregfi.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libregfi.so

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/reglookup*.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/*.so.*.*.*
%attr(755,root,root) %{_libdir}/*.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/*.so
%{_includedir}/regfi

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

%files -n python-pyregfi
%defattr(644,root,root,755)
%dir %{py_sitescriptdir}/pyregfi
%{py_sitescriptdir}/pyregfi/*.py[co]
%{py_sitescriptdir}/*.egg-info
