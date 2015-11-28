#
# Conditional build:
%bcond_without	doc		# don't build doc
%bcond_without	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module  itsdangerous
Summary:	Various helpers to pass trusted data to untrusted environments and back
Summary(pl.UTF-8):	Wspomaganie przekazywania danych do i z niebezpiecznych środowisk
Name:		python-%{module}
Version:	0.24
Release:	4
License:	BSD
Group:		Libraries/Python
Source0:	http://pypi.python.org/packages/source/i/%{module}/%{module}-%{version}.tar.gz
# Source0-md5:	a3d55aa79369aef5345c036a8a26307f
URL:		http://github.com/mitsuhiko/itsdangerous
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
%if %{with python2}
BuildRequires:	python-devel
BuildRequires:	python-distribute
%endif
%if %{with python3}
BuildRequires:	python3-devel
BuildRequires:	python3-distribute
BuildRequires:	python3-modules
%endif
Requires:	python-modules
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Various helpers to pass data to untrusted environments and to get it
back safe and sound.

# %description -l pl.UTF-8

%package -n python3-%{module}
Summary:	Various helpers to pass data to untrusted environments and to get it back safe and sound
Summary(pl.UTF-8):	Wspomaganie przekazywania danych do i z niebezpiecznych środowisk
Group:		Libraries/Python
Requires:	python3-modules

%description -n python3-%{module}

%description -n python3-%{module} -l pl.UTF-8

%package apidocs
Summary:	%{module} API documentation
Summary(pl.UTF-8):	Dokumentacja API %{module}
Group:		Documentation

%description apidocs
API documentation for %{module}.

%description apidocs -l pl.UTF-8
Dokumentacja API %{module}.

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
cd docs
%{__make} -j1 html
rm -rf _build/html/_sources
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
# %doc AUTHORS CREDITS ChangeLog NEWS README THANKS TODO
%{py_sitescriptdir}/%{module}.py[co]
%if "%{py_ver}" > "2.4"
%{py_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
# %doc AUTHORS CHANGES LICENSE
%{py3_sitescriptdir}/%{module}.py
%{py3_sitescriptdir}/__pycache__/*.py[co]
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif
