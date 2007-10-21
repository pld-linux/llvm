Summary:	The Low Level Virtual Machine (An Optimizing Compiler Infrastructure)
Name:		llvm
Version:	2.1
Release:	0.1
License:	University of Illinois/NCSA Open Source License
Group:		Development/Languages
URL:		http://llvm.org/
Source0:	http://llvm.org/releases/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	b930e7213b37acc934d0d163cf13af18
Patch0:		%{name}-dirs.patch
BuildRequires:	gcc >= 3.4
Requires:	/sbin/ldconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define	_sysconfdir	/etc/%{name}

%description
LLVM is a compiler infrastructure designed for compile-time,
link-time, runtime, and idle-time optimization of programs from
arbitrary programming languages. LLVM is written in C++ and has been
developed since 2000 at the University of Illinois and Apple. It
currently supports compilation of C and C++ programs, using front-ends
derived from GCC 4.0.1. A new front-end for the C family of languages
is in development. The compiler infrastructure includes mirror sets of
programming tools as well as libraries with equivalent functionality.

%prep
%setup -q
%patch0 -p0

%build
%configure \
	--enable-optimized \
	--enable-assertions

%{__make} tools-only

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -name .dir |xargs rm -f

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CREDITS.TXT LICENSE.TXT README.txt docs
%attr(755,root,root) %{_bindir}/*
%dir %{_sysconfdir}
%verify(not md5 mtime size) %config(noreplace) %{_sysconfdir}/*
%{_libdir}/*.o
%{_libdir}/*.a
%{_libdir}/*.la
%attr(755,root,root) %{_libdir}/*.so*
%{_includedir}/llvm
%{_includedir}/llvm-c
%{_mandir}/man?/llvm*
