#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

%define 	module  itsdangerous
Summary:	Various helpers to pass trusted data to untrusted environments and back
Summary(pl.UTF-8):	Wspomaganie przekazywania danych do i z niezaufanych środowisk
Name:		python3-%{module}
Version:	2.0.1
Release:	1
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.python.org/simple/itsdangerous
Source0:	https://pypi.python.org/packages/source/i/itsdangerous/%{module}-%{version}.tar.gz
# Source0-md5:	996b9763d1b4bd0edd6eb86f0a490629
URL:		http://github.com/mitsuhiko/itsdangerous
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	python3-modules >= 1:3.6
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-freezegun
BuildRequires:	python3-pytest
%endif
%if %{with doc}
BuildRequires:	python3-pallets-sphinx-themes >= 1.1.0
BuildRequires:	sphinx-pdg-3 >= 1.8.0
%endif
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Various helpers to pass data to untrusted environments and to get it
back safe and sound.

%description -l pl.UTF-8
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
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(pwd)/src \
%{__python3} -m pytest tests
%endif

%if %{with doc}
PYTHONPATH=$(pwd)/src \
%{__make} -C docs html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.rst LICENSE.rst README.rst
%{py3_sitescriptdir}/itsdangerous
%{py3_sitescriptdir}/itsdangerous-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
