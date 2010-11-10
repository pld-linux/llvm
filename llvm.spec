# TODO
#warning: Installed (but unpackaged) file(s) found:
#   /usr/share/man/man1/lit.1.gz
#
# Conditional build:
%bcond_without	ocaml	# ocaml binding
%bcond_with		apidocs	# The doxygen docs are HUGE, so they are not built by default.
%bcond_with		tests	# run tests

%ifarch s390 s390x sparc64
# No ocaml on these arches
%undefine	with_ocaml
%endif

Summary:	The Low Level Virtual Machine (An Optimizing Compiler Infrastructure)
Summary(pl.UTF-8):	Niskopoziomowa maszyna wirtualna (infrastruktura kompilatora optymalizującego)
Name:		llvm
Version:	2.8
Release:	3
License:	University of Illinois/NCSA Open Source License
Group:		Development/Languages
Source0:	http://llvm.org/releases/%{version}/%{name}-%{version}.tgz
# Source0-md5:	220d361b4d17051ff4bb21c64abe05ba
Source1:	http://llvm.org/releases/%{version}/clang-%{version}.tgz
# Source1-md5:	10e14c901fc3728eecbd5b829e011b59
# Data files should be installed with timestamps preserved
Patch3:		%{name}-2.6-timestamp.patch
URL:		http://llvm.org/
BuildRequires:	bash
BuildRequires:	bison
BuildRequires:	flex
%if %{with apidocs}
BuildRequires:	doxygen
BuildRequires:	graphviz
%endif
%if %{with tests}
BuildRequires:	dejagnu
BuildRequires:	python
BuildRequires:	tcl-devel
%endif
BuildRequires:	groff
BuildRequires:	libltdl-devel
BuildRequires:	libstdc++-devel >= 5:3.4
BuildRequires:	ocaml-ocamldoc
# gcc4 might be installed, but not current __cc
%if "%(echo %{cc_version} | cut -d. -f1,2)" < "3.4"
BuildRequires:	__cc >= 3.4
%endif
# LLVM is not supported on PPC64
# http://llvm.org/bugs/show_bug.cgi?id=3729
ExcludeArch:	ppc64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/%{name}

%define		specflags_ppc	-fno-var-tracking-assignments

# strip corrupts: $RPM_BUILD_ROOT/usr/lib64/llvm-gcc/bin/llvm-c++ ...
%define		_noautostrip	.*/\\(libmud.*\\.a\\|bin/llvm-.*\\|lib.*++\\.a\\)

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

%package devel
Summary:	Libraries and header files for LLVM
Group:		Development/Languages
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel >= 6:3.4

%description devel
This package contains library and header files needed to develop new
native programs that use the LLVM infrastructure.

%package doc
Summary:	Documentation for LLVM
Group:		Documentation
# does not require base

%description doc
Documentation for the LLVM compiler infrastructure.

%package apidocs
Summary:	API documentation for LLVM
Group:		Development/Languages
Requires:	%{name}-doc = %{version}-%{release}

%description apidocs
API documentation for the LLVM compiler infrastructure.

%package -n clang
Summary:	A C language family frontend for LLVM
License:	NCSA
Group:		Development/Languages

%description -n clang
clang: noun 1. A loud, resonant, metallic sound. 2. The strident call
of a crane or goose. 3. C-language family front-end toolkit.

The goal of the Clang project is to create a new C, C++, Objective C
and Objective C++ front-end for the LLVM compiler. Its tools are built
as libraries and designed to be loosely-coupled and extendable.

%package -n clang-analyzer
Summary:	A source code analysis framework
License:	NCSA
Group:		Development/Languages
Requires:	clang = %{version}-%{release}
# not picked up automatically since files are currently not instaled
# in standard Python hierarchies yet
Requires:	python

%description -n clang-analyzer
The Clang Static Analyzer consists of both a source code analysis
framework and a standalone tool that finds bugs in C and Objective-C
programs. The standalone tool is invoked from the command-line, and is
intended to run in tandem with a build of a project or code base.

%package -n clang-devel
Summary:	Header files for clang
Group:		Development/Languages
Requires:	clang = %{version}-%{release}

%description -n clang-devel
This package contains header files for the Clang compiler.

%package -n clang-doc
Summary:	Documentation for Clang
Group:		Documentation
Requires:	%{name} = %{version}-%{release}

%description -n clang-doc
Documentation for the Clang compiler front-end.

%package -n clang-apidocs
Summary:	API documentation for Clang
Group:		Development/Languages
Requires:	clang-doc = %{version}-%{release}

%description -n clang-apidocs
API documentation for the Clang compiler.

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
The llvm-ocaml-devel package contains libraries and signature files
for developing applications that use llvm-ocaml.

%package ocaml-doc
Summary:	Documentation for LLVM's OCaml binding
Group:		Documentation
Requires:	%{name}-ocaml = %{version}-%{release}

%description ocaml-doc
HTML documentation for LLVM's OCaml binding.

%prep
%setup -q -a1
mv clang-*.* tools/clang
%patch3 -p1

# configure does not properly specify libdir
sed -i 's|(PROJ_prefix)/lib|(PROJ_prefix)/%{_lib}|g' Makefile.config.in

grep -rl /usr/bin/env tools utils | xargs sed -i -e '1{
	s,^#!.*bin/env python,#!%{__python},
	s,^#!.*bin/env perl,#!%{__perl},
}'

install -d obj

%build
# Disabling assertions now, rec. by pure and needed for OpenGTL
# TESTFIX no PIC on ix86: http://llvm.org/bugs/show_bug.cgi?id=3801
#
# bash specific 'test a < b'
cd obj
bash ../%configure \
	--libdir=%{_libdir}/%{name} \
	--datadir=%{_datadir}/%{name}-%{version} \
%ifarch %{ix86}
	--enable-pic=no \
%endif
%if %{with apidocs}
	--enable-doxygen \
%endif
	--disable-static \
	--disable-assertions \
	--enable-debug-runtime \
	--enable-jit \
	--enable-optimized \
	--enable-shared \
	--with-pic

%{__make} \
	OPTIMIZE_OPTION="%{rpmcflags} %{rpmcppflags}"

%if %{with test}
%{__make} check 2>&1 | tee llvm-testlog.txt
%{__make} -C tools/clang test 2>&1 | tee clang-testlog.txt
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C obj -j1 install \
	PROJ_docsdir=/moredocs \
	DESTDIR=$RPM_BUILD_ROOT

# Static analyzer not installed by default:
# http://clang-analyzer.llvm.org/installation#OtherPlatforms
install -d $RPM_BUILD_ROOT%{_libdir}/clang-analyzer
# create launchers
for f in scan-{build,view}; do
	ln -s %{_libdir}/clang-analyzer/$f/$f $RPM_BUILD_ROOT%{_bindir}/$f
	cp -pr tools/clang/tools/$f $RPM_BUILD_ROOT%{_libdir}/clang-analyzer
done

# Move documentation back to build directory
rm -rf moredocs
mv $RPM_BUILD_ROOT/moredocs .
rm -fv moredocs/*.tar.gz
rm -fv moredocs/ocamldoc/html/*.tar.gz

# and separate the apidoc
%if %{with apidocs}
rm -rf apidoc clang-apidoc
mv moredocs/html/doxygen apidoc
cp -a tools/clang/docs/doxygen/html clang-apidoc
%endif

# And prepare Clang documentation
rm -rf clang-docs
install -d clang-docs
for f in LICENSE.TXT NOTES.txt README.txt TODO.txt; do
	ln tools/clang/$f clang-docs
done

# Get rid of erroneously installed example files.
rm -v $RPM_BUILD_ROOT%{_libdir}/*LLVMHello.*

# FIXME file this bug
sed -i 's,ABS_RUN_DIR/lib",ABS_RUN_DIR/%{_lib}",' \
	$RPM_BUILD_ROOT%{_bindir}/llvm-config

# remove documentation makefiles:
# they require the build directory to work
rm -rf moredocs/examples
cp -a examples moredocs/examples
find moredocs/examples -name Makefile | xargs -0r rm -f

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CREDITS.TXT LICENSE.TXT README.txt
%{?with_tests:%doc llvm-testlog.txt}
%attr(755,root,root) %{_bindir}/bugpoint
%attr(755,root,root) %{_bindir}/llc
%attr(755,root,root) %{_bindir}/lli
%attr(755,root,root) %{_bindir}/opt
%attr(755,root,root) %{_bindir}/llvmc
%attr(755,root,root) %{_bindir}/llvm-*
%exclude %attr(755,root,root) %{_bindir}/llvm-config
%attr(755,root,root) %{_libdir}/libLLVM-*.*.so
%{_mandir}/man1/bugpoint.1*
%{_mandir}/man1/llc.1*
%{_mandir}/man1/lli.1*
%{_mandir}/man1/llvmc.1*
%{_mandir}/man1/llvm-*.1*
%{_mandir}/man1/llvmgcc.1*
%{_mandir}/man1/llvmgxx.1*
%{_mandir}/man1/opt.1*
#%{_mandir}/man1/stkrc.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/llvm-config
%{_includedir}/llvm
%{_includedir}/llvm-c
%{_libdir}/lib*.a
# x86-64 only .a/.so?
%ifarch %{x8664}
%attr(755,root,root) %{_libdir}/libBugpointPasses.so
%attr(755,root,root) %{_libdir}/libEnhancedDisassembly.so
%attr(755,root,root) %{_libdir}/libLTO.so
%endif
#
%exclude %attr(755,root,root) %{_libdir}/libLLVM-*.*.so
%exclude %attr(755,root,root) %{_libdir}/libclang.so
%attr(755,root,root) %{_libdir}/libprofile_rt.so

%files doc
%defattr(644,root,root,755)
%doc moredocs/examples moredocs/html

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc apidoc/*
%endif

%files -n clang
%defattr(644,root,root,755)
%doc clang-docs/*
%{?with_tests:%doc clang-testlog.txt}
%attr(755,root,root) %{_bindir}/clang*
%attr(755,root,root) %{_bindir}/tblgen
%attr(755,root,root) %{_bindir}/c-index-test
%attr(755,root,root) %{_libdir}/libclang.so
%{_prefix}/lib/clang
%{_mandir}/man1/clang.1.*
%{_mandir}/man1/tblgen.1*

%files -n clang-analyzer
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/scan-build
%attr(755,root,root) %{_bindir}/scan-view
%dir %{_libdir}/clang-analyzer

%dir %{_libdir}/clang-analyzer/scan-view
%attr(755,root,root) %{_libdir}/clang-analyzer/scan-view/scan-view
%{_libdir}/clang-analyzer/scan-view/Resources
%{_libdir}/clang-analyzer/scan-view/*.py

%dir %{_libdir}/clang-analyzer/scan-build
%{_libdir}/clang-analyzer/scan-build/*.css
%{_libdir}/clang-analyzer/scan-build/*.js
%attr(755,root,root) %{_libdir}/clang-analyzer/scan-build/scan-build
%attr(755,root,root) %{_libdir}/clang-analyzer/scan-build/*-analyzer

%files -n clang-devel
%defattr(644,root,root,755)
%{_includedir}/clang
%{_includedir}/clang-c

%files -n clang-doc
%defattr(644,root,root,755)
%doc tools/clang/docs/*

%if %{with apidocs}
%files -n clang-apidocs
%defattr(644,root,root,755)
%doc clang-apidoc/*
%endif

%if %{with ocaml}
%files ocaml
%defattr(644,root,root,755)
%{_libdir}/ocaml/*.cma
%{_libdir}/ocaml/*.cmi

%files ocaml-devel
%defattr(644,root,root,755)
%{_libdir}/ocaml/*.a
%{_libdir}/ocaml/*.cmx*
%{_libdir}/ocaml/*.mli

%files ocaml-doc
%defattr(644,root,root,755)
%doc moredocs/ocamldoc/html/*
%endif
