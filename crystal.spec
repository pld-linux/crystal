#
# Conditional build:
%bcond_without	tests		# build without tests

Summary:	Crystal Programming Language
Name:		crystal
Version:	0.27.2
Release:	0.1
License:	Apache v2.0
Group:		Development/Languages
Source0:	https://github.com/crystal-lang/crystal/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	67ff7bdfc67c3b0ad2d7ea2e89753c68
URL:		https://crystal-lang.org/
BuildRequires:	gmp-devel
BuildRequires:	libbsd-devel
BuildRequires:	libedit-devel
BuildRequires:	libevent-devel
BuildRequires:	libxml2-devel
BuildRequires:	llvm < 7.0
BuildRequires:	llvm >= 3.8
BuildRequires:	openssl-devel
BuildRequires:	readline-devel
BuildRequires:	yaml-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
%setup -q

%build
CFLAGS="%{rpmcflags}" \
CXXFLAGS="%{rpmcxxflags}" \
%{__make} \
	CXX="%{__cxx}"
%{?with_tests:%{__make} spec}

%install
rm -rf $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md CHANGELOG.md
