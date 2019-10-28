#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module  itsdangerous
Summary:	Various helpers to pass trusted data to untrusted environments and back
Summary(pl.UTF-8):	Wspomaganie przekazywania danych do i z niezaufanych środowisk
Name:		python-%{module}
Version:	1.1.0
Release:	2
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.python.org/simple/itsdangerous
Source0:	https://pypi.python.org/packages/source/i/itsdangerous/%{module}-%{version}.tar.gz
# Source0-md5:	9b7f5afa7f1e3acfb7786eeca3d99307
URL:		http://github.com/mitsuhiko/itsdangerous
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.710
%if %{with python2}
BuildRequires:	python-devel >= 2
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	python3-modules >= 1:3.2
BuildRequires:	python3-setuptools
%endif
Requires:	python-modules >= 2
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Various helpers to pass data to untrusted environments and to get it
back safe and sound.

%description -l pl.UTF-8
Funkcje pomocnicze do przekazywania danych do niezaufanych środowisk i
pobierania ich w sposób bezpieczny.

%package -n python3-%{module}
Summary:	Various helpers to pass data to untrusted environments and to get it back safe and sound
Summary(pl.UTF-8):	Wspomaganie przekazywania danych do i z niebezpiecznych środowisk
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.2

%description -n python3-%{module}
Various helpers to pass data to untrusted environments and to get it
back safe and sound.

%description -n python3-%{module} -l pl.UTF-8
Funkcje pomocnicze do przekazywania danych do niezaufanych środowisk i
pobierania ich w sposób bezpieczny.

%package apidocs
Summary:	Documentation for Python itsdangerous module
Summary(pl.UTF-8):	Dokumentacja do moduły Pythona itsdangerous
Group:		Documentation

%description apidocs
Documentation for Python itsdangerous module.

%description apidocs -l pl.UTF-8
Dokumentacja do moduły Pythona itsdangerous.

%prep
%setup -q -n %{module}-%{version}

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%if %{with doc}
%{__make} -C docs html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGES.rst LICENSE.rst README.rst
%{py_sitescriptdir}/itsdangerous
%if "%{py_ver}" > "2.4"
%{py_sitescriptdir}/itsdangerous-%{version}-py*.egg-info
%endif
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc CHANGES.rst LICENSE.rst README.rst
%{py3_sitescriptdir}/itsdangerous
%{py3_sitescriptdir}/itsdangerous-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
