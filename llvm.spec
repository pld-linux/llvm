# TODO:
# - move and package:
#	%{_datadir}/clang/clang-format-sublime.py - sublime plugin
#	%{_datadir}/clang/clang-format.el - emacs mode
#	%{_datadir}/clang/clang-format.py - vim plugin
# - no content in doc package (it used to contain parts of clang apidocs and some examples)
#
# Conditional build:
%bcond_without	lldb	# LLDB debugger
%bcond_without	polly	# Polly cache-locality optimization, auto-parallelism and vectorization
%bcond_without	rt	# compiler-rt libraries
%bcond_without	ocaml	# OCaml binding
%bcond_without	doc	# HTML docs and man pages
%bcond_with	apidocs	# doxygen docs (HUGE, so they are not built by default)
%bcond_with	tests	# run tests

# No ocaml on other arches or no native ocaml (required for ocaml-ctypes)
%ifnarch %{ix86} %{x8664} arm aarch64 ppc sparc sparcv9 
%undefine	with_ocaml
%endif

Summary:	The Low Level Virtual Machine (An Optimizing Compiler Infrastructure)
Summary(pl.UTF-8):	Niskopoziomowa maszyna wirtualna (infrastruktura kompilatora optymalizującego)
Name:		llvm
Version:	3.7.0
Release:	3
License:	University of Illinois/NCSA Open Source License
Group:		Development/Languages
#Source0Download: http://llvm.org/releases/download.html
Source0:	http://llvm.org/releases/%{version}/%{name}-%{version}.src.tar.xz
# Source0-md5:	b98b9495e5655a672d6cb83e1a180f8e
Source1:	http://llvm.org/releases/%{version}/cfe-%{version}.src.tar.xz
# Source1-md5:	8f9d27335e7331cf0a4711e952f21f01
Source2:	http://llvm.org/releases/%{version}/compiler-rt-%{version}.src.tar.xz
# Source2-md5:	383c10affd513026f08936b5525523f5
Source3:	http://llvm.org/releases/%{version}/lldb-%{version}.src.tar.xz
# Source3-md5:	e5931740400d1dc3e7db4c7ba2ceff68
Source4:	http://llvm.org/releases/%{version}/polly-%{version}.src.tar.xz
# Source4-md5:	32f93ffc9cc7e042df22089761558f8b
Source5:	http://llvm.org/releases/%{version}/clang-tools-extra-%{version}.src.tar.xz
# Source5-md5:	d5a87dacb65d981a427a536f6964642e
Source6:	http://llvm.org/releases/%{version}/lld-%{version}.src.tar.xz
# Source6-md5:	91bd593a67293d84dad0bf11845546c2
Patch0:		%{name}-lld-link.patch
Patch1:		%{name}-pld.patch
Patch2:		libdir.patch
Patch3:		x32-gcc-toolchain.patch
Patch5:		debuginfo-fix.patch
URL:		http://llvm.org/
BuildRequires:	bash
BuildRequires:	bison
BuildRequires:	cmake
BuildRequires:	flex
BuildRequires:	gcc >= 5:3.4
# gcc4 might be installed, but not current __cc
%if "%(echo %{cc_version} | cut -d. -f1,2)" < "3.4"
BuildRequires:	__cc >= 3.4
%endif
%ifarch x32
BuildRequires:	glibc-devel(x86_64)
%endif
BuildRequires:	groff
BuildRequires:	libltdl-devel
BuildRequires:	libstdc++-devel >= 5:3.4
%if %{with ocaml}
BuildRequires:	ocaml-ctypes-devel >= 0.4
BuildRequires:	ocaml-findlib
BuildRequires:	ocaml-ocamldoc
BuildRequires:	ocaml-ounit
%endif
BuildRequires:	perl-base >= 1:5.6
BuildRequires:	perl-tools-pod
BuildRequires:	rpm-pythonprov
%{?with_doc:BuildRequires:	sphinx-pdg}
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
%if %{with apidocs}
BuildRequires:	doxygen
BuildRequires:	graphviz
%endif
%if %{with tests}
BuildRequires:	dejagnu
BuildRequires:	python
BuildRequires:	tcl-devel
%endif
%if %{with lldb}
BuildRequires:	epydoc
%ifarch i386 i486
BuildRequires:	libatomic-devel
%endif
BuildRequires:	libedit-devel
BuildRequires:	libxml2-devel >= 2
BuildRequires:	ncurses-ext-devel
BuildRequires:	python-devel >= 2
BuildRequires:	swig-python
%endif
%if %{with polly}
BuildRequires:	cloog-isl-devel
# >= 0.18.2-2
BuildRequires:	gmp-devel
BuildRequires:	isl-devel >= 0.14
# optional
BuildRequires:	pluto-devel
BuildRequires:	scoplib-devel >= 0.2.1-2
#cuda-devel
%endif
Requires:	%{name}-libs = %{version}-%{release}
# LLVM is not supported on PPC64
# http://llvm.org/bugs/show_bug.cgi?id=3729
ExcludeArch:	ppc64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/%{name}

%define		specflags_ppc	-fno-var-tracking-assignments

# strip corrupts: $RPM_BUILD_ROOT/usr/lib64/llvm-gcc/bin/llvm-c++ ...
%define		_noautostrip	.*/\\(libmud.*\\.a\\|bin/llvm-.*\\|lib.*++\\.a\\)

# clang doesn't know it, and leaving it here would pollute llvm-config
%define		filterout_c	-fvar-tracking-assignments
%define		filterout_cxx	-fvar-tracking-assignments
%define		filterout_ccpp	-fvar-tracking-assignments

# std::__once_call, std::__once_callable non-function symbols
%define		skip_post_check_so	liblldAArch64ELFTarget.so.* liblldARMELFTarget.so.* liblldHexagonELFTarget.so.* liblldMipsELFTarget.so.* liblldb.so.*

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

%package libs
Summary:	LLVM shared library
Summary(pl.UTF-8):	Biblioteka współdzielona LLVM-a
Group:		Libraries
Conflicts:	llvm < 3.2

%description libs
LLVM shared library.

%description libs -l pl.UTF-8
Biblioteka współdzielona LLVM-a.

%package devel
Summary:	Static libraries and header files for LLVM
Summary(pl.UTF-8):	Biblioteki statyczne i pliki nagłówkowe dla LLVM-a
Group:		Development/Languages
Requires:	%{name}-libs = %{version}-%{release}
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

%package polly
Summary:	Polyhedral optimizations for LLVM
Summary(pl.UTF-8):	Optymalizacje wielościanowe dla LLVM-a
Group:		Development/Tools
URL:		http://polly.llvm.org/
Requires:	%{name} = %{version}-%{release}

%description polly
Polly is a high-level loop and data-locality optimizer and
optimization infrastructure for LLVM. It uses an abstract mathematical
representation based on integer polyhedra to analyze and optimize the
memory access pattern of a program.

%description polly -l pl.UTF-8
Polly to wysokopoziomowy optymalizator i infrastruktura LLVM-a do
optymalizacji pętli i położenia danych. Wykorzystuje abstrakcyjną
reprezentację matematyczną opartą na wielościanach całkowitoliczbowych
do analizy i optymalizacji wzorców dostępu do pamięci przez program.

%package polly-devel
Summary:	Header files for LLVM Polly optimization infrastructure
Summary(pl.UTF-8):	Pliki nagłówkowe infrastruktury optymalizacji LLVM-a Polly
Group:		Development/Libraries
URL:		http://polly.llvm.org/
Requires:	%{name}-devel = %{version}-%{release}
Requires:	%{name}-polly = %{version}-%{release}

%description polly-devel
Header files for LLVM Polly optimization infrastructure.

%description polly-devel -l pl.UTF-8
Pliki nagłówkowe infrastruktury optymalizacji LLVM-a Polly.

%package -n clang
Summary:	A C language family frontend for LLVM
Summary(pl.UTF-8):	Frontend LLVM-a do języków z rodziny C
License:	NCSA
Group:		Development/Languages
Requires:	%{name} = %{version}-%{release}

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

%package -n clang-multilib
Summary:	A C language family frontend for LLVM - 32-bit support
Summary(pl.UTF-8):	Frontend LLVM-a do języków z rodziny C - obsługa binariów 32-bitowych
License:	NCSA
Group:		Development/Languages
Requires:	clang = %{version}-%{release}

%description -n clang-multilib
clang: noun 1. A loud, resonant, metallic sound. 2. The strident call
of a crane or goose. 3. C-language family front-end toolkit.

The goal of the Clang project is to create a new C, C++, Objective C
and Objective C++ front-end for the LLVM compiler. Its tools are built
as libraries and designed to be loosely-coupled and extendable.

This package contains the C compiler support for producing 32-bit
programs on 64-bit host.

%description -n clang-multilib -l pl.UTF-8
clang (z angielskiego): 1. głośny, rezonujący, metaliczny dźwięk; 2.
piskliwy odgłos żurawia lub gęsi; 3. narzędzia frontendowe dla języków
z rodziny C.

Celem projektu Clang jest utworzenie nowego frontendu dla kompilatora
LLVM do języków C, C++, Objective C i Objective C++. Narzędzia są
budowane jako biblioteki i zaprojektowane z myślą o swobodnym łączeniu
i rozszerzaniu.

Ten pakiet zawiera rozszerzenie kompilatora C o obsługę tworzenia
programów 32-bitowych na maszynie 64-bitowej.

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
Requires:	%{name}-devel = %{version}-%{release}
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

%package -n clang-tools-extra
Summary:	Extra tools for Clang
Summary(pl.UTF-8):	Dodatkowe narzędzia do kompilatora Clang
Group:		Development/Tools
URL:		http://clang.llvm.org/docs/ClangTools.html
Requires:	clang = %{version}-%{release}

%description -n clang-tools-extra
Extra tools for Clang.

%description -n clang-tools-extra -l pl.UTF-8
Dodatkowe narzędzia do kompilatora Clang.

%package -n lld
Summary:	The LLVM linker
Summary(pl.UTF-8):	Konsolidator z projektu LLVM
Group:		Development/Libraries
URL:		http://lld.llvm.org/
Requires:	%{name} = %{version}-%{release}

%description -n lld
lld is a new set of modular code for creating linker tools.

%description -n lld -l pl.UTF-8
lld to nowy zbiór modularnego kodu do tworzenia narzędzi
konsolidujących.

%package -n lld-devel
Summary:	Development files for LLD linker tools
Summary(pl.UTF-8):	Pliki programistyczne narzędzi konsolidujących LLD
Group:		Development/Tools
URL:		http://lld.llvm.org/
Requires:	%{name}-devel = %{version}-%{release}

%description -n lld-devel
Development files for LLD linker tools.

%description -n lld-devel -l pl.UTF-8
Pliki programistyczne narzędzi konsolidujących LLD.

%package -n lldb
Summary:	Next generation high-performance debugger
Summary(pl.UTF-8):	Wydajny debugger nowej generacji
Group:		Development/Debuggers
URL:		http://lldb.llvm.org/
Requires:	%{name} = %{version}-%{release}

%description -n lldb
LLDB is a next generation, high-performance debugger. It is built as a
set of reusable components which highly leverage existing libraries in
the larger LLVM Project, such as the Clang expression parser and LLVM
disassembler.

%description -n lldb -l pl.UTF-8
LLDB to wydajny debugger nowej generacji. Jest zbudowany w oparciu o
komponenty wielokrotnego użytku, wykorzystujące istniejące biblioteki
w projekcie LLVM, takie jak analizator wyrażeń kompilatora Clang oraz
disasembler LLVM.

%package -n lldb-devel
Summary:	Development files for LLDB debugger
Summary(pl.UTF-8):	Pliki programistyczne debuggera LLDB
Group:		Development/Libraries
URL:		http://lldb.llvm.org/
Requires:	%{name}-devel = %{version}-%{release}
Requires:	clang-devel = %{version}-%{release}
Requires:	lldb = %{version}-%{release}

%description -n lldb-devel
Development files for LLDB debugger.

%description -n lldb-devel -l pl.UTF-8
Pliki programistyczne debuggera LLDB.

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
%setup -q -n %{name}-%{version}.src -a1 %{?with_rt:-a2} %{?with_lldb:-a3} %{?with_polly:-a4} -a5 -a6
mv cfe-%{version}.src tools/clang
%{?with_rt:mv compiler-rt-%{version}.src projects/compiler-rt}
%{?with_lldb:mv lldb-%{version}.src tools/lldb}
%{?with_polly:mv polly-%{version}.src tools/polly}
mv clang-tools-extra-%{version}.src tools/clang/tools/extra
mv lld-%{version}.src tools/lld

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch5 -p1

grep -rl /usr/bin/env tools utils | xargs sed -i -e '1{
	s,^#!.*bin/env python,#!%{__python},
	s,^#!.*bin/env perl,#!%{__perl},
}'

%build
install -d build

# Disabling assertions now, rec. by pure and needed for OpenGTL
# TESTFIX no PIC on ix86: http://llvm.org/bugs/show_bug.cgi?id=3801
cd build
CPPFLAGS="%{rpmcppflags} -D_FILE_OFFSET_BITS=64"

%{cmake} ../ \
%ifarch %{x8664}
	-DLLVM_LIBDIR_SUFFIX:STRING=64 \
%endif
%ifarch x32
	-DLLVM_LIBDIR_SUFFIX:STRING=x32 \
%endif
%ifarch %{ix86}
	-DLLVM_ENABLE_PIC:BOOL=OFF \
%endif
%if %{with apidocs}
	-DLLVM_ENABLE_DOXYGEN:BOOL=ON \
%endif
%if %{with doc}
	-DLLVM_ENABLE_SPHINX:BOOL=ON \
%endif
	-DLLVM_ENABLE_ASSERTIONS:BOOL=OFF \
	-DLLVM_ENABLE_CXX1Y:BOOL=ON \
	-DLLVM_BINDINGS_LIST:LIST="%{?with_ocaml:ocaml}" \
	-DBUILD_SHARED_LIBS:BOOL=ON

%{__make} \
	VERBOSE=1 \
	REQUIRES_RTTI=1 \
	OPTIMIZE_OPTION="%{rpmcflags} %{rpmcppflags}"

%if %{with tests}
%{__make} check 2>&1 | tee llvm-testlog.txt
%{__make} -C tools/clang test 2>&1 | tee clang-testlog.txt
%endif

%if %{with doc}
%{__make} -C docs docs-llvm-html
%{__make} -C docs docs-llvm-man
%if %{with ocaml}
%{__make} -C docs ocaml_doc
%endif
%{__make} -C tools/clang/docs docs-clang-html
%{__make} -C tools/clang/docs docs-clang-man
%{__make} -C tools/lld/docs docs-lld-html
%{__make} -C tools/lldb/docs lldb-python-doc
%{__make} -C tools/lldb/docs lldb-cpp-doc
%{__make} -C ../tools/clang/tools/extra/docs html
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# only some .pyc files are created by make install
%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}

# Static analyzer not installed by default:
# http://clang-analyzer.llvm.org/installation#OtherPlatforms
install -d $RPM_BUILD_ROOT%{_libdir}/clang-analyzer
# create launchers
for f in scan-{build,view}; do
	ln -s %{_libdir}/clang-analyzer/$f/$f $RPM_BUILD_ROOT%{_bindir}/$f
	cp -pr tools/clang/tools/$f $RPM_BUILD_ROOT%{_libdir}/clang-analyzer
done
install -d $RPM_BUILD_ROOT%{_mandir}/man1
%{__mv} $RPM_BUILD_ROOT%{_libdir}/clang-analyzer/scan-build/scan-build.1 $RPM_BUILD_ROOT%{_mandir}/man1
%py_comp $RPM_BUILD_ROOT%{_libdir}/clang-analyzer/scan-view
%py_ocomp $RPM_BUILD_ROOT%{_libdir}/clang-analyzer/scan-view
%py_postclean %{_libdir}/clang-analyzer/scan-view
# not this OS
%{__rm} $RPM_BUILD_ROOT%{_libdir}/clang-analyzer/scan-build/*.bat

# not installed by cmake buildsystem
install build/bin/clang-query $RPM_BUILD_ROOT%{_bindir}
install build/bin/pp-trace $RPM_BUILD_ROOT%{_bindir}

%if %{with doc}
cp -p build/docs/man/*.1 $RPM_BUILD_ROOT%{_mandir}/man1
# these tools are not installed
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/{FileCheck,llvm-build}.1
# make links
echo '.so llvm-ar.1' > $RPM_BUILD_ROOT%{_mandir}/man1/llvm-ranlib.1
%endif

# Move documentation back to build directory
%if %{with ocaml}
rm -rf ocamldocs
mv $RPM_BUILD_ROOT%{_prefix}/docs/ocaml/html/html ocamldocs
%endif

# and separate the apidoc
%if %{with apidocs}
rm -rf clang-apidoc
cp -a build/tools/clang/docs/html clang-apidoc
%endif

# And prepare Clang documentation
rm -rf clang-docs
install -d clang-docs
for f in LICENSE.TXT NOTES.txt README.txt; do
	ln tools/clang/$f clang-docs
done

# Get rid of erroneously installed example files.
%{__rm} $RPM_BUILD_ROOT%{_libdir}/LLVMHello.so
# test?
%{__rm} $RPM_BUILD_ROOT%{_bindir}/llvm-c-test
# not this OS
%{__rm} $RPM_BUILD_ROOT%{_datadir}/clang/clang-format-bbedit.applescript

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%post	-n clang -p /sbin/ldconfig
%postun	-n clang -p /sbin/ldconfig

%post	-n clang-tools-extra -p /sbin/ldconfig
%postun	-n clang-tools-extra -p /sbin/ldconfig

%post	-n lldb -p /sbin/ldconfig
%postun	-n lldb -p /sbin/ldconfig

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
%attr(755,root,root) %{_bindir}/llvm-dsymutil
%attr(755,root,root) %{_bindir}/llvm-dwarfdump
%attr(755,root,root) %{_bindir}/llvm-extract
%attr(755,root,root) %{_bindir}/llvm-lib
%attr(755,root,root) %{_bindir}/llvm-link
%ifarch %{x8664} x32
%attr(755,root,root) %{_bindir}/llvm-lto
%endif
%attr(755,root,root) %{_bindir}/llvm-mc
%attr(755,root,root) %{_bindir}/llvm-mcmarkup
%attr(755,root,root) %{_bindir}/llvm-nm
%attr(755,root,root) %{_bindir}/llvm-objdump
%attr(755,root,root) %{_bindir}/llvm-profdata
%attr(755,root,root) %{_bindir}/llvm-ranlib
%attr(755,root,root) %{_bindir}/llvm-readobj
%attr(755,root,root) %{_bindir}/llvm-rtdyld
%attr(755,root,root) %{_bindir}/llvm-size
%attr(755,root,root) %{_bindir}/llvm-stress
%attr(755,root,root) %{_bindir}/llvm-symbolizer
%attr(755,root,root) %{_bindir}/llvm-tblgen
%attr(755,root,root) %{_bindir}/llvm-cxxdump
%attr(755,root,root) %{_bindir}/llvm-pdbdump
%attr(755,root,root) %{_bindir}/macho-dump
%attr(755,root,root) %{_bindir}/obj2yaml
%attr(755,root,root) %{_bindir}/opt
%attr(755,root,root) %{_bindir}/verify-uselistorder
%attr(755,root,root) %{_bindir}/yaml2obj
%if %{with doc}
%{_mandir}/man1/bugpoint.1*
%{_mandir}/man1/lit.1*
%{_mandir}/man1/llc.1*
%{_mandir}/man1/lli.1*
%{_mandir}/man1/llvm-ar.1*
%{_mandir}/man1/llvm-as.1*
%{_mandir}/man1/llvm-bcanalyzer.1*
%{_mandir}/man1/llvm-cov.1*
%{_mandir}/man1/llvm-diff.1*
%{_mandir}/man1/llvm-dis.1*
%{_mandir}/man1/llvm-dwarfdump.1*
%{_mandir}/man1/llvm-extract.1*
%{_mandir}/man1/llvm-link.1*
%{_mandir}/man1/llvm-nm.1*
%{_mandir}/man1/llvm-profdata.1*
%{_mandir}/man1/llvm-ranlib.1*
%{_mandir}/man1/llvm-readobj.1*
%{_mandir}/man1/llvm-stress.1*
%{_mandir}/man1/llvm-symbolizer.1*
%{_mandir}/man1/opt.1*
%{_mandir}/man1/tblgen.1*
%endif

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libLLVM*.so.%{version}
%attr(755,root,root) %ghost %{_libdir}/libLLVM*.so.3.7
%ifarch %{x8664} x32
%attr(755,root,root) %{_libdir}/libLTO.so.%{version}
%attr(755,root,root) %ghost %{_libdir}/libLTO.so.3.7
%endif

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/llvm-config
%attr(755,root,root) %{_libdir}/libLLVM*.so
%attr(755,root,root) %{_libdir}/BugpointPasses.so
%ifarch %{x8664} x32
%attr(755,root,root) %{_libdir}/libLTO.so
%endif
%{_includedir}/llvm
%{_includedir}/llvm-c
%dir %{_datadir}/llvm
%{_datadir}/llvm/cmake
%if %{with doc}
%{_mandir}/man1/llvm-config.1*
%endif

#%files doc
#%defattr(644,root,root,755)

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc apidoc/*
%endif

%if %{with polly}
%files polly
%defattr(644,root,root,755)
%doc tools/polly/{CREDITS.txt,LICENSE.txt,README}
%attr(755,root,root) %{_libdir}/LLVMPolly.so
%attr(755,root,root) %{_libdir}/libPolly.so

%files polly-devel
%defattr(644,root,root,755)
%{_includedir}/polly
%endif

%files -n clang
%defattr(644,root,root,755)
%doc clang-docs/{LICENSE.TXT,NOTES.txt,README.txt} %{?with_tests:clang-testlog.txt}
%attr(755,root,root) %{_bindir}/clang
%attr(755,root,root) %{_bindir}/clang++
%attr(755,root,root) %{_bindir}/clang-3.7
%attr(755,root,root) %{_bindir}/clang-check
%attr(755,root,root) %{_bindir}/clang-cl
%attr(755,root,root) %{_bindir}/clang-format
%attr(755,root,root) %{_bindir}/git-clang-format
%attr(755,root,root) %{_libdir}/libclang*.so.%{version}
%attr(755,root,root) %ghost %{_libdir}/libclang*.so.3.7
%dir %{_libdir}/clang
%dir %{_libdir}/clang/%{version}
%{_libdir}/clang/%{version}/include
%if %{with rt}
%ifarch %{ix86} %{x8664}
%{_libdir}/clang/%{version}/asan_blacklist.txt
%dir %{_libdir}/clang/%{version}/lib
%dir %{_libdir}/clang/%{version}/lib/linux
%endif
%ifarch %{ix86}
%{_libdir}/clang/%{version}/lib/linux/libclang_rt.*-i*86.a
%attr(755,root,root) %{_libdir}/clang/%{version}/lib/linux/libclang_rt.*-i*86.so
%endif
%ifarch %{x8664}
%{_libdir}/clang/%{version}/dfsan_abilist.txt
%{_libdir}/clang/%{version}/msan_blacklist.txt
%{_libdir}/clang/%{version}/lib/linux/libclang_rt.*-x86_64.a
%attr(755,root,root) %{_libdir}/clang/%{version}/lib/linux/libclang_rt.*-x86_64.so
%{_libdir}/clang/%{version}/lib/linux/libclang_rt.*-x86_64.a.syms
%endif
%endif
%dir %{_datadir}/clang
%{_datadir}/clang/clang-format-diff.py

%if %{with rt}
%ifarch %{x8664}
%files -n clang-multilib
%defattr(644,root,root,755)
%{_libdir}/clang/%{version}/lib/linux/libclang_rt.*-i386.a
%attr(755,root,root) %{_libdir}/clang/%{version}/lib/linux/libclang_rt.*-i386.so
%endif
%endif

%files -n clang-analyzer
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/scan-build
%attr(755,root,root) %{_bindir}/scan-view
%{_mandir}/man1/scan-build.1*
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
%attr(755,root,root) %{_libdir}/libclang*.so
%ifarch %{ix86} # ???
%{_libdir}/libclang.a
%endif
%{_includedir}/clang
%{_includedir}/clang-c

%files -n clang-doc
%defattr(644,root,root,755)
%doc tools/clang/docs/*.{html,png,txt}

%if %{with apidocs}
%files -n clang-apidocs
%defattr(644,root,root,755)
%doc clang-apidoc/*
%endif

%files -n clang-tools-extra
%defattr(644,root,root,755)
%doc tools/clang/tools/extra/{CODE_OWNERS.TXT,README.txt} tools/clang/tools/extra/docs/_build/html/{*.html,*.js,_static}
%attr(755,root,root) %{_bindir}/clang-apply-replacements
%attr(755,root,root) %{_bindir}/clang-modernize
%attr(755,root,root) %{_bindir}/clang-query
%attr(755,root,root) %{_bindir}/clang-rename
%attr(755,root,root) %{_bindir}/clang-tidy
%attr(755,root,root) %{_bindir}/pp-trace
%attr(755,root,root) %{_libdir}/libmodernizeCore.so.%{version}
%attr(755,root,root) %ghost %{_libdir}/libmodernizeCore.so.3.7
# -devel?
%attr(755,root,root) %{_libdir}/libmodernizeCore.so

%files -n lld
%defattr(644,root,root,755)
%doc tools/lld/{LICENSE.TXT,README.md}
%attr(755,root,root) %{_bindir}/lld
%attr(755,root,root) %{_libdir}/liblld[ACDEHMPRXY]*.so.%{version}
%attr(755,root,root) %ghost %{_libdir}/liblld[ACDEHMPRXY]*.so.3.7

%files -n lld-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblld[ACDEHMPRXY]*.so
%{_includedir}/lld

%if %{with lldb}
%files -n lldb
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/argdumper
%attr(755,root,root) %{_bindir}/lldb
%attr(755,root,root) %{_bindir}/lldb-%{version}
%attr(755,root,root) %{_bindir}/lldb-mi
%attr(755,root,root) %{_bindir}/lldb-mi-%{version}
%attr(755,root,root) %{_bindir}/lldb-server
%attr(755,root,root) %{_bindir}/lldb-server-%{version}
%attr(755,root,root) %{_libdir}/liblldb.so.%{version}
%attr(755,root,root) %ghost %{_libdir}/liblldb.so.3.7
%dir %{py_sitedir}/lldb
%attr(755,root,root) %{py_sitedir}/lldb/argdumper
%{py_sitedir}/lldb/formatters
%{py_sitedir}/lldb/runtime
%{py_sitedir}/lldb/utils
%{py_sitedir}/lldb/__init__.py[co]
%{py_sitedir}/lldb/embedded_interpreter.py[co]
%attr(755,root,root) %{py_sitedir}/lldb/_lldb.so
%attr(755,root,root) %{py_sitedir}/readline.so

%files -n lldb-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblldb.so
%{_libdir}/liblldb*.a
%{_includedir}/lldb
%endif

%if %{with ocaml}
%files ocaml
%defattr(644,root,root,755)
%{_libdir}/ocaml/META.llvm*
%attr(755,root,root) %{_libdir}/ocaml/dllllvm*.so
%{_libdir}/ocaml/llvm*.cma
%{_libdir}/ocaml/llvm*.cmi

%files ocaml-devel
%defattr(644,root,root,755)
%{_libdir}/ocaml/libllvm*.a
%{_libdir}/ocaml/llvm*.a
%{_libdir}/ocaml/llvm*.cmx*

%files ocaml-doc
%defattr(644,root,root,755)
%doc ocamldocs/*
%endif
