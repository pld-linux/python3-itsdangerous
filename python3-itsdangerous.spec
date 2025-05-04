#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

%define 	module  itsdangerous
Summary:	Various helpers to pass trusted data to untrusted environments and back
Summary(pl.UTF-8):	Wspomaganie przekazywania danych do i z niezaufanych środowisk
Name:		python3-%{module}
Version:	2.2.0
Release:	1
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/itsdangerous
Source0:	https://files.pythonhosted.org/packages/source/i/itsdangerous/%{module}-%{version}.tar.gz
# Source0-md5:	a901babde35694c3577f7655010cd380
URL:		http://github.com/mitsuhiko/itsdangerous
BuildRequires:	python3-build
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.7
%if %{with tests}
# TODO: >= 1.1.0
BuildRequires:	python3-freezegun
BuildRequires:	python3-pytest >= 7.0.1
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-pallets-sphinx-themes >= 2.0.2
BuildRequires:	python3-sphinx_issues >= 3.0.1
BuildRequires:	python3-sphinxcontrib-log-cabinet >= 1.0.1
BuildRequires:	sphinx-pdg-3 >= 4.4.0
%endif
Requires:	python3-modules >= 1:3.7
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
%py3_build_pyproject

%if %{with tests}
%{__python3} -m zipfile -e build-3/*.whl build-3-test
# use explicit plugins list for reliable builds (delete PYTEST_PLUGINS if empty)
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS= \
%{__python3} -m pytest -o pythonpath="$PWD/build-3-test" tests
%endif

%if %{with doc}
%{__python3} -m zipfile -e build-3/*.whl build-3-doc
PYTHONPATH=$(pwd)/build-3-doc \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.rst LICENSE.txt README.md
%{py3_sitescriptdir}/itsdangerous
%{py3_sitescriptdir}/itsdangerous-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
