# TODO
# - gcc/c++ packages: http://cvs.fedoraproject.org/viewvc/rpms/llvm/devel/llvm.spec?revision=HEAD&view=markup
#
# Conditional build:
%bcond_with		ocaml	# build without OCaml bindings
%bcond_with		gcc		# build without gcc
#
%define		lgcc_version	4.2
Summary:	The Low Level Virtual Machine (An Optimizing Compiler Infrastructure)
Summary(pl.UTF-8):	Niskopoziomowa maszyna wirtualna (infrastruktura kompilatora optymalizującego)
Name:		llvm
Version:	2.3
Release:	0.1
License:	University of Illinois/NCSA Open Source License
Group:		Development/Languages
Source0:	http://llvm.org/releases/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	17254d72863b7fa005f3fb327aea3439
Source1:	http://llvm.org/releases/%{version}/%{name}-gcc-%{lgcc_version}-%{version}.source.tar.gz
# Source1-md5:	18aa4f8226ddab58af2f12cff135470d
Patch0:		%{name}-dirs.patch
URL:		http://llvm.org/
BuildRequires:	bash
BuildRequires:	gcc >= 5:3.4
BuildRequires:	libltdl-devel
%{?with_ocaml:BuildRequires:  ocaml}
# gcc4 might be installed, but not current __cc
%if "%(echo %{cc_version} | cut -d. -f1,2)" < "3.4"
BuildRequires:	__cc >= 3.4
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/%{name}

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

%package doc
Summary:	Documentation for LLVM
Group:		Documentation
Requires:	%{name} = %{version}-%{release}

%description doc
Documentation for the LLVM compiler infrastructure.

%package devel
Summary:	Libraries and header files for LLVM
Group:		Development/Languages
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel >= 6:3.4

%description devel
This package contains library and header files needed to develop new
native programs that use the LLVM infrastructure.

%package gcc
Summary:	C compiler for LLVM
License:	GPL+
Group:		Development/Languages
Requires:	%{name} = %{version}-%{release}

%description gcc
C compiler for LLVM.

%package gcc-c++
Summary:	C++ compiler for LLVM
License:	GPL+
Group:		Development/Languages
Requires:	%{name}-gcc = %{version}-%{release}

%description gcc-c++
C++ compiler for LLVM.

%package ocaml
Summary:	OCaml binding for LLVM
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%requires_eq	ocaml-runtime

%description    ocaml
OCaml binding for LLVM.

%package ocaml-devel
Summary:	Development files for %{name}-ocaml
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	%{name}-ocaml = %{version}-%{release}

%description ocaml-devel
The %{name}-ocaml-devel package contains libraries and signature files
for developing applications that use %{name}-ocaml.

%prep
%setup -q %{?with_gcc:-a1}
%patch0 -p0

%build
# bash specific 'test a < b'
bash %configure \
	--libdir=%{_libdir}/%{name} \
	--datadir=%{_datadir}/%{name}-%{version} \
	--enable-bindings=%{!?with_ocaml:no}%{?with_ocaml:ocaml} \
	--disable-static \
	--enable-assertions \
	--enable-debug-runtime \
	--enable-jit \
	--enable-optimized \
	--enable-shared \
	--with-pic

%{__make} OPTIMIZE_OPTION="%{rpmcflags}"

%if %{with gcc}
# Build llvm-gcc.

export PATH=%{_builddir}/%{?buildsubdir}/Release/bin:$PATH

install -d llvm-gcc%{lgcc_version}-%{version}.source/build
cd llvm-gcc%{lgcc_version}-%{version}.source/build
../configure \
	--host=%{_host} \
	--build=%{_build} \
	--target=%{_target_platform} \
	--prefix=%{_libdir}/llvm-gcc \
	--libdir=%{_libdir}/llvm-gcc/%{_lib} \
	--enable-threads \
	--disable-nls \
%ifarch %{x8664}
	--disable-multilib \
	--disable-shared \
%endif
	--enable-languages=c,c++ \
	--enable-llvm=%{_builddir}/%{?buildsubdir} \
	--program-prefix=llvm-

%{__make} LLVM_VERSION_INFO=%{version}
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -name .dir | xargs rm -fv

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CREDITS.TXT LICENSE.TXT README.txt
%attr(755,root,root) %{_bindir}/bugpoint
%attr(755,root,root) %{_bindir}/gccas
%attr(755,root,root) %{_bindir}/gccld
%attr(755,root,root) %{_bindir}/llc
%attr(755,root,root) %{_bindir}/lli
%attr(755,root,root) %{_bindir}/opt
%attr(755,root,root) %{_bindir}/llvmc2
%attr(755,root,root) %{_bindir}/llvm-*
%exclude %attr(755,root,root) %{_bindir}/llvm-config
%{_mandir}/man1/bugpoint.1*
%{_mandir}/man1/llc.1*
%{_mandir}/man1/lli.1*
%{_mandir}/man1/llvm-*.1*
%{_mandir}/man1/llvmgcc.1*
%{_mandir}/man1/llvmgxx.1*
%{_mandir}/man1/opt.1*
%{_mandir}/man1/stkrc.1*
%{_mandir}/man1/tblgen.1*

%files doc
%defattr(644,root,root,755)
%doc docs/*.{html,css} docs/img examples

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/llvm-config
%{_includedir}/llvm
%{_includedir}/llvm-c
%{_libdir}/LLVM*.o
%{_libdir}/libLLVM*.a
# just example?
%attr(755,root,root) %{_libdir}/LLVMHello.so*
%{_libdir}/LLVMHello.la

%if %{with gcc}
%files gcc
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/llvm2cpp
%attr(755,root,root) %{_bindir}/llvmc
%dir %{_sysconfdir}
%verify(not md5 mtime size) %config(noreplace) %{_sysconfdir}/c
%verify(not md5 mtime size) %config(noreplace) %{_sysconfdir}/cpp
%verify(not md5 mtime size) %config(noreplace) %{_sysconfdir}/ll
%verify(not md5 mtime size) %config(noreplace) %{_sysconfdir}/st
%{_mandir}/man1/llvm2cpp.1*
%{_mandir}/man1/llvmc.1*

%files gcc-c++
%defattr(644,root,root,755)
%verify(not md5 mtime size) %config(noreplace) %{_sysconfdir}/c++
%verify(not md5 mtime size) %config(noreplace) %{_sysconfdir}/cxx
%endif
