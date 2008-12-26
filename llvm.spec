Summary:	The Low Level Virtual Machine (An Optimizing Compiler Infrastructure)
Summary(pl.UTF-8):	Niskopoziomowa maszyna wirtualna (infrastruktura kompilatora optymalizującego)
Name:		llvm
Version:	2.3
Release:	0.1
License:	University of Illinois/NCSA Open Source License
Group:		Development/Languages
Source0:	http://llvm.org/releases/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	17254d72863b7fa005f3fb327aea3439
Patch0:		%{name}-dirs.patch
URL:		http://llvm.org/
BuildRequires:	gcc >= 5:3.4
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

%description -l pl.UTF-8
LLVM to infrastruktura kompilatora zaprojektowana do optymalizacji
czasu kompilowania, linkowania, działania i bezczynności programów w
dowolnych językach programowania. Jest napisana w C++, rozwijana od
roku 2000 przez Uniwersytet w Illinois i Apple. Aktualnie obsługuje
kompilację programów w C i C++ przy użyciu frontendów wywodzących się
z GCC 4.0.1. W trakcie tworzenia jest nowy frontend do języków z
rodziny C. Infrastruktura kompilatora zawiera lustrzane zestawy
narzędzi programistycznych oraz biblioteki z odpowiadającą narzędziom
funkcjonalnością.

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

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CREDITS.TXT LICENSE.TXT README.txt docs
%attr(755,root,root) %{_bindir}/bugpoint
%attr(755,root,root) %{_bindir}/gccas
%attr(755,root,root) %{_bindir}/gccld
%attr(755,root,root) %{_bindir}/llc
%attr(755,root,root) %{_bindir}/lli
%attr(755,root,root) %{_bindir}/llvm-*
%attr(755,root,root) %{_bindir}/llvm2cpp
%attr(755,root,root) %{_bindir}/llvmc
%attr(755,root,root) %{_bindir}/opt
%dir %{_sysconfdir}
%verify(not md5 mtime size) %config(noreplace) %{_sysconfdir}/c
%verify(not md5 mtime size) %config(noreplace) %{_sysconfdir}/c++
%verify(not md5 mtime size) %config(noreplace) %{_sysconfdir}/cpp
%verify(not md5 mtime size) %config(noreplace) %{_sysconfdir}/cxx
%verify(not md5 mtime size) %config(noreplace) %{_sysconfdir}/ll
%verify(not md5 mtime size) %config(noreplace) %{_sysconfdir}/st
%{_libdir}/LLVM*.o
%{_libdir}/libLLVM*.a
# just example?
%attr(755,root,root) %{_libdir}/LLVMHello.so*
%{_libdir}/LLVMHello.la
%{_libdir}/LLVMHello.a
%{_includedir}/llvm
%{_includedir}/llvm-c
%{_mandir}/man1/bugpoint.1*
%{_mandir}/man1/llc.1*
%{_mandir}/man1/lli.1*
%{_mandir}/man1/llvm-*.1*
%{_mandir}/man1/llvm2cpp.1*
%{_mandir}/man1/llvmc.1*
%{_mandir}/man1/llvmgcc.1*
%{_mandir}/man1/llvmgxx.1*
%{_mandir}/man1/opt.1*
%{_mandir}/man1/stkrc.1*
%{_mandir}/man1/tblgen.1*
