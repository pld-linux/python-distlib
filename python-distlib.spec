#
# Conditional build:
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	Distribution utilities
Summary(pl.UTF-8):	Narzędzia do dystrybuowania
Name:		python-distlib
Version:	0.3.0
Release:	2
License:	PSF v2
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/distlib/
Source0:	https://files.pythonhosted.org/packages/source/d/distlib/distlib-%{version}.zip
# Source0-md5:	f92e0f3ac43397da86a82781117e8351
Patch0:		%{name}-obsoletes.patch
Patch1:		%{name}-sequencer.patch
URL:		https://pypi.org/project/distlib/
%if %(locale -a | grep -q '^C\.utf8$'; echo $?)
BuildRequires:	glibc-localedb-all
%endif
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.2
%if %{with tests}
BuildConflicts:	python3-astroid < 2.3.3-2
BuildConflicts:	python3-pylint < 2.4.4-2
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	sed >= 4.0
BuildRequires:	unzip
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Low-level components of distutils2/packaging, augmented with
higher-level APIs for making packaging easier.

%description -l pl.UTF-8
Niskopoziomowe komponenty distutils2/packaging, rozszerzone o
wysokopoziomowe API ułatwiające pakietowanie.

%package -n python3-distlib
Summary:	Distribution utilities
Summary(pl.UTF-8):	Narzędzia do dystrybuowania
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.2

%description -n python3-distlib
Low-level components of distutils2/packaging, augmented with
higher-level APIs for making packaging easier.

%description -n python3-distlib -l pl.UTF-8
Niskopoziomowe komponenty distutils2/packaging, rozszerzone o
wysokopoziomowe API ułatwiające pakietowanie.

%prep
%setup -q -n distlib-%{version}
%patch0 -p1
%patch1 -p1

%if "%{_host_cpu}" == "x32"
# distlib.wheel doesn't distinguish x32 from x86_64
%{__sed} -i -e 's/test_mount_extensions/disabled&/' tests/test_wheel.py
%endif

%build
%if %{with python2}
%py_build

%if %{with tests}
LC_ALL=C.UTF-8 \
SKIP_ONLINE=1 \
PYTHONPATH=$(pwd) \
%{__python} tests/test_all.py
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
LC_ALL=C.UTF-8 \
SKIP_ONLINE=1 \
PYTHONPATH=$(pwd) \
%{__python3} tests/test_all.py
%endif
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
%doc CHANGES.rst CONTRIBUTORS.txt LICENSE.txt README.rst
%{py_sitescriptdir}/distlib
%{py_sitescriptdir}/distlib-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-distlib
%defattr(644,root,root,755)
%doc CHANGES.rst CONTRIBUTORS.txt LICENSE.txt README.rst
%{py3_sitescriptdir}/distlib
%{py3_sitescriptdir}/distlib-%{version}-py*.egg-info
%endif
