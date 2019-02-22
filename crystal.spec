#
# Conditional build:
%bcond_with	bootstrap	# bootstrap build
%bcond_without	tests		# build without tests

# this probably does not have to be very latest
%define		bootstrap_ver	0.27.2
Summary:	Crystal Programming Language
Name:		crystal
Version:	0.27.2
Release:	0.1
License:	Apache v2.0
Group:		Development/Languages
Source0:	https://github.com/crystal-lang/crystal/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	67ff7bdfc67c3b0ad2d7ea2e89753c68
Source1:	https://github.com/crystal-lang/crystal/releases/download/%{bootstrap_ver}/%{name}-%{bootstrap_ver}-1-linux-x86_64.tar.gz
# Source1-md5:	e382b8e6d60eb748dbad3d7ee59843a4
URL:		https://crystal-lang.org/
%{!?with_bootstrap:BuildRequires:	crystal}
BuildRequires:	gmp-devel
BuildRequires:	libbsd-devel
BuildRequires:	libedit-devel
BuildRequires:	libevent-devel
BuildRequires:	libxml2-devel
BuildRequires:	llvm-devel < 7.0
BuildRequires:	llvm-devel >= 3.8
BuildRequires:	openssl-devel
BuildRequires:	pcre-devel
BuildRequires:	pkgconfig
BuildRequires:	readline-devel
BuildRequires:	yaml-devel
%if %{with tests}
BuildRequires:	gc-devel
%endif
ExclusiveArch:	%{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# avoid super weird provides
# crystal(Tuple(T)#unsafe_fetch<Int32>:String)(64bit) crystal(src/compiler/crystal/command.cr:344)(64bit)
%define		_noautoprov	crystal

# Filter GLIBC_PRIVATE Requires
%define		_noautoreq	(GLIBC_PRIVATE)

%description
This is the language reference for the Crystal programming language.

Crystal is a programming language with the following goals:
- Have a syntax similar to Ruby (but compatibility with it is not a
  goal).
- Be statically type-checked, but without having to specify the type
  of variables or method arguments.
- Be able to call C code by writing bindings to it in Crystal.
- Have compile-time evaluation and generation of code, to avoid
  boilerplate code.
- Compile to efficient native code.

%prep
%setup -q %{?with_bootstrap:-a1}

%build
%if %{with bootstrap}
PATH=$PATH:crystal-%{bootstrap_ver}-1/bin
%endif

CFLAGS="%{rpmcflags}" \
CXXFLAGS="%{rpmcxxflags}" \
%{__make} progress=true stats=true \
	CC="%{__cc}" \
	CXX="%{__cxx}"
%{?with_tests:%{__make} spec}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}
install -p .build/crystal $RPM_BUILD_ROOT%{_bindir}/crystal

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md CHANGELOG.md
%attr(755,root,root) %{_bindir}/crystal
