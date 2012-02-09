#
# TODO:
# make *** No rule to make target (...)/rpm/BUILD/llvm-3.0.src/obj/bindings/ocaml/llvm/Release/META.llvm, needed by install-meta.
#
# Conditional build:
%bcond_without	ocaml	# ocaml binding
%bcond_with	apidocs	# The doxygen docs are HUGE, so they are not built by default.
%bcond_with	tests	# run tests

%ifarch s390 s390x sparc64
# No ocaml on these arches
%undefine	with_ocaml
%endif

Summary:	The Low Level Virtual Machine (An Optimizing Compiler Infrastructure)
Summary(pl.UTF-8):	Niskopoziomowa maszyna wirtualna (infrastruktura kompilatora optymalizującego)
Name:		llvm
Version:	3.0
Release:	0.1
License:	University of Illinois/NCSA Open Source License
Group:		Development/Languages
Source0:	http://llvm.org/releases/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	a8e5f5f1c1adebae7b4a654c376a6005
Source1:	http://llvm.org/releases/%{version}/clang-%{version}.tar.gz
# Source1-md5:	43350706ae6cf05d0068885792ea0591
# Data files should be installed with timestamps preserved
Patch3:		%{name}-2.6-timestamp.patch
Patch4:		%{name}-pld.patch
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
BuildRequires:	perl-base >= 1:5.6
BuildRequires:	perl-tools-pod
BuildRequires:	rpm-pythonprov
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
currently supports compilation of C and C++ programs using clang
frontend.

%description -l pl.UTF-8
LLVM to infrastruktura kompilatora zaprojektowana do optymalizacji
czasu kompilowania, linkowania, działania i bezczynności programów w
dowolnych językach programowania. Jest napisana w C++, rozwijana od
roku 2000 przez Uniwersytet w Illinois i Apple. Aktualnie obsługuje
kompilację programów w C i C++ przy użyciu frontendu clang.

%package devel
Summary:	Static libraries and header files for LLVM
Summary(pl.UTF-8):	Biblioteki statyczne i pliki nagłówkowe dla LLVM-a
Group:		Development/Languages
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel >= 6:3.4

%description devel
This package contains static libraries and header files needed to
develop new native programs that use the LLVM infrastructure.

%description devel -l pl.UTF-8
Ten pakiet zawiera biblioteki statyczne oraz pliki nagłówkowe
potrzebne do tworzenia nowych programów natywnych wykorzystujących
infrastrukturę LLVM.

%package doc
Summary:	Documentation for LLVM
Summary(pl.UTF-8):	Dokumentacja do LLVM-a
Group:		Documentation
# does not require base

%description doc
Documentation for the LLVM compiler infrastructure.

%description doc -l pl.UTF-8
Dokumentacja do infrastruktury kompilatorów LLVM.

%package apidocs
Summary:	API documentation for LLVM
Summary(pl.UTF-8):	Dokumentacja API LLVM-a
Group:		Development/Languages
Requires:	%{name}-doc = %{version}-%{release}

%description apidocs
API documentation for the LLVM compiler infrastructure.

%description apidocs -l pl.UTF-8
Dokumentacja API infrastruktury kompilatorów LLVM.

%package -n clang
Summary:	A C language family frontend for LLVM
Summary(pl.UTF-8):	Frontend LLVM-a do języków z rodziny C
License:	NCSA
Group:		Development/Languages

%description -n clang
clang: noun 1. A loud, resonant, metallic sound. 2. The strident call
of a crane or goose. 3. C-language family front-end toolkit.

The goal of the Clang project is to create a new C, C++, Objective C
and Objective C++ front-end for the LLVM compiler. Its tools are built
as libraries and designed to be loosely-coupled and extendable.

%description -n clang -l pl.UTF-8
clang (z angielskiego): 1. głośny, rezonujący, metaliczny dźwięk; 2.
piskliwy odgłos żurawia lub gęsi; 3. narzędzia frontendowe dla języków
z rodziny C.

Celem projektu Clang jest utworzenie nowego frontendu dla kompilatora
LLVM do języków C, C++, Objective C i Objective C++. Narzędzia są
budowane jako biblioteki i zaprojektowane z myślą o swobodnym łączeniu
i rozszerzaniu.

%package -n clang-analyzer
Summary:	A source code analysis framework
Summary(pl.UTF-8):	Szkielet do analizy kodu źródłowego
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

%description -n clang-analyzer -l pl.UTF-8
Clang Static Analyzer składa się ze szkieletu do analizy kodu
źródłowego oraz samodzielnego narzędzia znajdującego błędy w
programach w C i C++. Narzędzie jest wywoływane z linii poleceń, z
myślą o uruchamianiu wraz z kompilacją projektu lub kodu.

%package -n clang-devel
Summary:	Header files for Clang
Summary(pl.UTF-8):	Pliki nagłówkowe Clanga
Group:		Development/Languages
Requires:	clang = %{version}-%{release}

%description -n clang-devel
This package contains header files for the Clang compiler.

%description -n clang-devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe kompilatora Clang.

%package -n clang-doc
Summary:	Documentation for Clang
Summary(pl.UTF-8):	Dokumentacja do Clanga
Group:		Documentation
Requires:	%{name} = %{version}-%{release}

%description -n clang-doc
Documentation for the Clang compiler front-end.

%description -n clang-doc -l pl.UTF-8
Dokumentacja do frontendu kompilatora Clang.

%package -n clang-apidocs
Summary:	API documentation for Clang
Summary(pl.UTF-8):	Dokumentacja API Clanga
Group:		Development/Languages
Requires:	clang-doc = %{version}-%{release}

%description -n clang-apidocs
API documentation for the Clang compiler.

%description -n clang-apidocs -l pl.UTF-8
Dokumentacja API kompilatora Clang.

%package ocaml
Summary:	OCaml binding for LLVM
Summary(pl.UTF-8):	Wiązanie OCamla do LLVM-a
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
%requires_eq	ocaml-runtime

%description ocaml
OCaml binding for LLVM.

%description ocaml -l pl.UTF-8
Wiązanie OCamla do LLVM-a.

%package ocaml-devel
Summary:	Development files for LLVM OCaml binding
Summary(pl.UTF-8):	Pliki programistyczne wiązania OCamla do LLVM-a
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	%{name}-ocaml = %{version}-%{release}

%description ocaml-devel
The llvm-ocaml-devel package contains libraries and signature files
for developing applications that use llvm-ocaml binding.

%description ocaml-devel -l pl.UTF-8
Ten pakiet zawiera biblioteki i pliki sygnatur do tworzenia aplikacji
wykorzystujących wiązanie llvm-ocaml.


%package ocaml-doc
Summary:	Documentation for LLVM's OCaml binding
Summary(pl.UTF-8):	Dokumentacja wiązania OCamla do LLVM-a
Group:		Documentation
Requires:	%{name}-ocaml = %{version}-%{release}

%description ocaml-doc
HTML documentation for LLVM's OCaml binding.

%description ocaml-doc -l pl.UTF-8
Dokumentacja HTML wiązania OCamla do LLVM-a.

%prep
%setup -q -a1 -n %{name}-%{version}.src
mv clang-*.* tools/clang
%patch3 -p1
%patch4 -p1

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
	--enable-bindings=%{?with_ocaml:ocaml}%{!?with_ocaml:none} \
	--disable-static \
	--disable-assertions \
	--enable-debug-runtime \
	--enable-jit \
	--enable-optimized \
	--enable-shared \
	--with-pic

%{__make} \
	REQUIRES_RTTI=1 \
	OPTIMIZE_OPTION="%{rpmcflags} %{rpmcppflags}"

%if %{with tests}
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
%py_comp $RPM_BUILD_ROOT%{_libdir}/clang-analyzer/scan-view
%py_ocomp $RPM_BUILD_ROOT%{_libdir}/clang-analyzer/scan-view
%py_postclean %{_libdir}/clang-analyzer/scan-view

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
for f in LICENSE.TXT NOTES.txt README.txt; do
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
%doc CREDITS.TXT LICENSE.TXT README.txt %{?with_tests:llvm-testlog.txt}
%attr(755,root,root) %{_bindir}/bugpoint
%attr(755,root,root) %{_bindir}/llc
%attr(755,root,root) %{_bindir}/lli
%attr(755,root,root) %{_bindir}/llvm-ar
%attr(755,root,root) %{_bindir}/llvm-as
%attr(755,root,root) %{_bindir}/llvm-bcanalyzer
%attr(755,root,root) %{_bindir}/llvm-cov
%attr(755,root,root) %{_bindir}/llvm-diff
%attr(755,root,root) %{_bindir}/llvm-dis
%attr(755,root,root) %{_bindir}/llvm-dwarfdump
%attr(755,root,root) %{_bindir}/llvm-extract
%attr(755,root,root) %{_bindir}/llvm-ld
%attr(755,root,root) %{_bindir}/llvm-link
%attr(755,root,root) %{_bindir}/llvm-mc
%attr(755,root,root) %{_bindir}/llvm-nm
%attr(755,root,root) %{_bindir}/llvm-objdump
%attr(755,root,root) %{_bindir}/llvm-prof
%attr(755,root,root) %{_bindir}/llvm-ranlib
%attr(755,root,root) %{_bindir}/llvm-rtdyld
%attr(755,root,root) %{_bindir}/llvm-size
%attr(755,root,root) %{_bindir}/llvm-stub
%attr(755,root,root) %{_bindir}/llvm-tblgen
%attr(755,root,root) %{_bindir}/macho-dump
%attr(755,root,root) %{_bindir}/opt
%attr(755,root,root) %{_libdir}/libLLVM-%{version}.so
%{_mandir}/man1/bugpoint.1*
%{_mandir}/man1/lit.1*
%{_mandir}/man1/llc.1*
%{_mandir}/man1/lli.1*
%{_mandir}/man1/llvm-ar.1*
%{_mandir}/man1/llvm-as.1*
%{_mandir}/man1/llvm-bcanalyzer.1*
%{_mandir}/man1/llvm-diff.1*
%{_mandir}/man1/llvm-dis.1*
%{_mandir}/man1/llvm-extract.1*
%{_mandir}/man1/llvm-ld.1*
%{_mandir}/man1/llvm-link.1*
%{_mandir}/man1/llvm-nm.1*
%{_mandir}/man1/llvm-prof.1*
%{_mandir}/man1/llvm-ranlib.1*
%{_mandir}/man1/opt.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/llvm-config
%attr(755,root,root) %{_libdir}/libprofile_rt.so
%{_libdir}/libLLVM*.a
%{_libdir}/libprofile_rt.a
%ifarch %{x8664}
%attr(755,root,root) %{_libdir}/BugpointPasses.so
%attr(755,root,root) %{_libdir}/libLTO.so
%{_libdir}/libEnhancedDisassembly.a
%{_libdir}/libLTO.a
%endif
%{_includedir}/llvm
%{_includedir}/llvm-c
%{_mandir}/man1/llvm-config.1*

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
%doc clang-docs/{LICENSE.TXT,NOTES.txt,README.txt} %{?with_tests:clang-testlog.txt}
%attr(755,root,root) %{_bindir}/clang
%attr(755,root,root) %{_bindir}/clang++
%attr(755,root,root) %{_bindir}/clang-tblgen
%attr(755,root,root) %{_libdir}/libclang.so
%{_prefix}/lib/clang
%{_mandir}/man1/clang.1*
%{_mandir}/man1/tblgen.1*

%files -n clang-analyzer
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/scan-build
%attr(755,root,root) %{_bindir}/scan-view
%dir %{_libdir}/clang-analyzer

%dir %{_libdir}/clang-analyzer/scan-build
%{_libdir}/clang-analyzer/scan-build/*.css
%{_libdir}/clang-analyzer/scan-build/*.js
%attr(755,root,root) %{_libdir}/clang-analyzer/scan-build/scan-build
%attr(755,root,root) %{_libdir}/clang-analyzer/scan-build/*-analyzer

%dir %{_libdir}/clang-analyzer/scan-view
%attr(755,root,root) %{_libdir}/clang-analyzer/scan-view/scan-view
%{_libdir}/clang-analyzer/scan-view/Resources
%{_libdir}/clang-analyzer/scan-view/*.py[co]

%files -n clang-devel
%defattr(644,root,root,755)
%{_libdir}/libclang*.a
%{_includedir}/clang
%{_includedir}/clang-c

%files -n clang-doc
%defattr(644,root,root,755)
%doc tools/clang/docs/*.{css,html,png,txt}

%if %{with apidocs}
%files -n clang-apidocs
%defattr(644,root,root,755)
%doc clang-apidoc/*
%endif

%if %{with ocaml}
%files ocaml
%defattr(644,root,root,755)
%{_libdir}/ocaml/llvm*.cma
%{_libdir}/ocaml/llvm*.cmi

%files ocaml-devel
%defattr(644,root,root,755)
%{_libdir}/ocaml/libLLVM*.a
%{_libdir}/ocaml/libllvm*.a
%{_libdir}/ocaml/llvm*.a
%{_libdir}/ocaml/llvm*.cmx*
%{_libdir}/ocaml/llvm*.mli

%files ocaml-doc
%defattr(644,root,root,755)
%doc moredocs/ocamldoc/html/*
%endif
