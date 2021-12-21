#
# NOTE:
#  - normal build (x86_64) requires about 80 GB of disk space
#
# TODO:
# - move and package:
#	%{_datadir}/clang/bash-autocomplete.sh
#	%{_datadir}/clang/clang-format-sublime.py - sublime plugin
#	%{_datadir}/clang/clang-format.el - clang tools emacs integration
#	%{_datadir}/clang/clang-include-fixer.el
#	%{_datadir}/clang/clang-rename.el
# - no content in doc package (it used to contain parts of clang apidocs and some examples)
# - system isl in polly?
#
# Conditional build:
%bcond_without	lldb			# LLDB debugger
%bcond_without	polly			# Polly cache-locality optimization, auto-parallelism and vectorization
%bcond_without	rt			# compiler-rt libraries
%bcond_without	multilib		# compiler-rt multilib libraries
%bcond_without	ocaml			# OCaml binding
%bcond_without	z3			# Z3 constraint solver support in Clang Static Analyzer
%bcond_without	doc			# HTML docs and man pages
%bcond_without	target_aarch64		# AArch64 target support
%bcond_without	target_amdgpu		# AMDGPU target support
%bcond_without	target_arm		# ARM target support
%bcond_without	target_avr		# AVR target support
%bcond_without	target_bpf		# BPF target support
%bcond_without	target_hexagon		# Hexagon target support
%bcond_without	target_lanai		# Lanai target support
%bcond_without	target_mips		# Mips target support
%bcond_without	target_msp430		# MSP430 target support
%bcond_without	target_nvptx		# NVPTX target support
%bcond_without	target_powerpc		# PowerPC target support
%bcond_without	target_riscv		# RISCV target support
%bcond_without	target_sparc		# Sparc target support
%bcond_without	target_systemz		# SystemZ target support
%bcond_without	target_webassembly	# WebAssembly target support
%bcond_without	target_x86		# X86 target support
%bcond_without	target_xcore		# XCore target support
%bcond_with	flang			# flang (Fortran18) compiler (broken as of 11.0.1)
%bcond_with	cxxmodules		# C++20 modules (requires support in bootstrap compiler)
%bcond_with	apidocs			# doxygen docs (HUGE, so they are not built by default)
%bcond_with	tests			# run tests
%bcond_with	lowmem			# lower memory requirements

# No ocaml on other arches or no native ocaml (required for ocaml-ctypes)
%ifnarch %{ix86} %{x8664} %{arm} aarch64 ppc sparc sparcv9
%undefine	with_ocaml
%endif

%ifarch armv3l armv4b armv4l armv4tl armv5tl armv5tel armv5tejl armv6l armv6hl
%undefine	with_rt
%endif

%ifarch %{arm} aarch64
%define		with_lowmem		1
%endif

%define		targets_to_build	%{?with_target_aarch64:AArch64;}%{?with_target_amdgpu:AMDGPU;}%{?with_target_arm:ARM;}%{?with_target_avr:AVR;}%{?with_target_bpf:BPF;}%{?with_target_hexagon:Hexagon;}%{?with_target_lanai:Lanai;}%{?with_target_mips:Mips;}%{?with_target_msp430:MSP430;}%{?with_target_nvptx:NVPTX;}%{?with_target_powerpc:PowerPC;}%{?with_target_riscv:RISCV;}%{?with_target_sparc:Sparc;}%{?with_target_systemz:SystemZ;}%{?with_target_webassembly:WebAssembly;}%{?with_target_x86:X86;}%{?with_target_xcore:XCore;}

Summary:	The Low Level Virtual Machine (An Optimizing Compiler Infrastructure)
Summary(pl.UTF-8):	Niskopoziomowa maszyna wirtualna (infrastruktura kompilatora optymalizującego)
Name:		llvm
Version:	13.0.0
Release:	3
License:	University of Illinois/NCSA Open Source License
Group:		Development/Languages
#Source0Download: https://github.com/llvm/llvm-project/releases/
Source0:	https://github.com/llvm/llvm-project/releases/download/llvmorg-%{version}/%{name}-%{version}.src.tar.xz
# Source0-md5:	8c24626dce3ee9d87d1079ebf0897db5
Source1:	https://github.com/llvm/llvm-project/releases/download/llvmorg-%{version}/clang-%{version}.src.tar.xz
# Source1-md5:	020cbac6e5786094fe4f96f72e290763
Source2:	https://github.com/llvm/llvm-project/releases/download/llvmorg-%{version}/compiler-rt-%{version}.src.tar.xz
# Source2-md5:	e2e136656d27d60c5f40e20260f63c07
Source3:	https://github.com/llvm/llvm-project/releases/download/llvmorg-%{version}/lldb-%{version}.src.tar.xz
# Source3-md5:	0956c6078d1fd3bee22d064e2addd784
Source4:	https://github.com/llvm/llvm-project/releases/download/llvmorg-%{version}/polly-%{version}.src.tar.xz
# Source4-md5:	4bde9e5c4d739576cf2d804d50c822d6
Source5:	https://github.com/llvm/llvm-project/releases/download/llvmorg-%{version}/clang-tools-extra-%{version}.src.tar.xz
# Source5-md5:	f86778fc0d97508b4d7c244d93ebf944
Source6:	https://github.com/llvm/llvm-project/releases/download/llvmorg-%{version}/lld-%{version}.src.tar.xz
# Source6-md5:	e4f95d6cb895ebedf2c3224585682159
Source7:	https://github.com/llvm/llvm-project/releases/download/llvmorg-%{version}/flang-%{version}.src.tar.xz
# Source7-md5:	4125a570905dd2755748e6f33442b74d
# "mlir" subdir extracted from https://github.com/llvm/llvm-project/releases/download/llvmorg-13.0.0/llvm-project-13.0.0.src.tar.xz
Source8:	mlir-%{version}.tar.xz
# Source8-md5:	de6a9476ef2a52b59d7c29a8bb786719
Patch1:		%{name}-pld.patch
Patch2:		%{name}-python-modules.patch
Patch3:		x32-gcc-toolchain.patch
Patch4:		cmake-buildtype.patch
Patch5:		%{name}-ocaml-shared.patch
Patch6:		%{name}-flang.patch
Patch7:		llvm12-build_fixes.patch
Patch8:		%{name}-selective_bindings.patch
Patch9:		%{name}-libexecdir.patch
URL:		http://llvm.org/
BuildRequires:	bash
BuildRequires:	binutils-devel
BuildRequires:	bison
BuildRequires:	cmake >= 3.13.4
BuildRequires:	flex
BuildRequires:	groff
BuildRequires:	libedit-devel
BuildRequires:	libltdl-devel
BuildRequires:	libpfm-devel
BuildRequires:	libstdc++-devel >= 6:5
BuildRequires:	libxml2-devel >= 2
BuildRequires:	ncurses-devel
%if %{with ocaml}
BuildRequires:	ocaml >= 4.00.0
BuildRequires:	ocaml-ctypes-devel >= 0.4
BuildRequires:	ocaml-findlib
BuildRequires:	ocaml-ocamldoc
%{?with_tests:BuildRequires:	ocaml-ounit >= 2}
%endif
BuildRequires:	perl-base >= 1:5.6
BuildRequires:	perl-tools-pod
BuildRequires:	python3 >= 1:3
BuildRequires:	python3-PyYAML
BuildRequires:	python3-pygments >= 2.0
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.742
%{?with_doc:BuildRequires:	sphinx-pdg}
BuildRequires:	tar >= 1:1.22
BuildRequires:	xar-devel >= 1.6
BuildRequires:	xz
%{?with_z3:BuildRequires:	z3-devel >= 4.7.1}
BuildRequires:	zlib-devel
%if %{with apidocs}
BuildRequires:	doxygen
BuildRequires:	graphviz
%endif
%if %{with tests}
BuildRequires:	dejagnu
BuildRequires:	tcl-devel
%endif
%if %{with rt} && %{with multilib}
%ifarch %{x8664}
BuildRequires:	gcc-c++-multilib-32
BuildRequires:	libstdc++-multilib-32-devel
%endif
%ifarch x32
BuildRequires:	gcc-c++-multilib-32
BuildRequires:	gcc-c++-multilib-64
BuildRequires:	glibc-devel(x86_64)
BuildRequires:	libstdc++-multilib-32-devel
BuildRequires:	libstdc++-multilib-64-devel
%endif
%endif
%if %{with lldb}
BuildRequires:	epydoc
%ifarch i386 i486 %{arm}
BuildRequires:	libatomic-devel
%endif
BuildRequires:	libxml2-devel >= 2
BuildRequires:	lua-devel
BuildRequires:	ncurses-ext-devel
BuildRequires:	python3-devel >= 1:3.2
%{?with_doc:BuildRequires:	python3-recommonmark}
BuildRequires:	swig-python >= 3.0.11
BuildRequires:	xz-devel
%endif
%if %{with polly}
#BuildRequires:	gmp-devel or imath-devel (private copy in polly/lib/External/isl/imath)
# private copy in polly/lib/External/isl
#BuildRequires:	isl-devel >= 0.22.1
#TODO (bcond): cuda-devel (with POLLY_ENABLE_GPGPU_CODEGEN=ON)
%{?with_target_nvptx:BuildRequires:	ocl-icd-libOpenCL-devel}
%endif
%if %{with ocaml}
BuildConflicts:	llvm-ocaml
%endif
Requires:	%{name}-libs = %{version}-%{release}
# LLVM is not supported on PPC64
# http://llvm.org/bugs/show_bug.cgi?id=3729
ExcludeArch:	ppc64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		abi	13
%define		_sysconfdir	/etc/%{name}

%define		specflags_ppc	-fno-var-tracking-assignments

# objcopy: BFD (GNU Binutils) 2.32 assertion fail format.c:459
# objcopy: error: .../libLLVM-8.so(.debug_gnu_pubtypes) is too large (0x1ceee347 bytes)
# objcopy: .../libLLVM-8.so[.debug_gnu_pubtypes]: memory exhausted
%ifarch x32
%define		_enable_debug_packages	0
%endif
# ix86 and x32 - the same issue as https://llvm.org/bugs/show_bug.cgi?id=27237
# use -gsplit-dwarf only when building packages with debuginfo
# to avoid excessive disk space usage
%if 0%{?_enable_debug_packages}
%define		specflags	-gsplit-dwarf
%endif

# strip corrupts: $RPM_BUILD_ROOT/usr/lib64/llvm-gcc/bin/llvm-c++ ...
%define		_noautostrip	.*/\\(libmud.*\\.a\\|bin/llvm-.*\\|lib.*++\\.a\\)

# clang doesn't know -fvar-tracking-assignments, and leaving it here would pollute llvm-config
# -Werror=format-security is for swig
# TODO: add - -Werror=format-security to tools/lldb/scripts/LLDBWrapPython.cpp
%define		filterout_c	-fvar-tracking-assignments
%define		filterout_cxx	-fvar-tracking-assignments -Werror=format-security
%define		filterout_ccpp	-fvar-tracking-assignments

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
Summary:	LLVM shared libraries
Summary(pl.UTF-8):	Biblioteki współdzielone LLVM-a
Group:		Libraries
Conflicts:	llvm < 3.2

%description libs
LLVM shared libraries.

%description libs -l pl.UTF-8
Biblioteki współdzielone LLVM-a.

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
Requires:	clang-libs = %{version}-%{release}

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

%package -n clang-libs
Summary:	Clang shared libraries
Summary(pl.UTF-8):	Biblioteki współdzielone Clanga
Group:		Libraries

%description -n clang-libs
Clang shared libraries.

%description -n clang-libs -l pl.UTF-8
Biblioteki współdzielone Clanga.

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
Requires:	python3

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
%{?with_polly:Requires:	llvm-polly-devel = %{version}-%{release}}

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
Requires:	xar-devel >= 1.6

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
Requires:	python3-six

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
%if %{with ocaml}
%requires_eq	ocaml-runtime
%endif

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

%package opt-viewer
Summary:	Optimization records visualization tools
Summary(pl.UTF-8):	Narzędzia do wizualizacji rekordów optymalizacji
Group:		Development/Tools
Requires:	%{name} = %{version}
BuildArch:	noarch

%description opt-viewer
Optimization records visualization tools.

%description opt-viewer -l pl.UTF-8
Narzędzia do wizualizacji rekordów optymalizacji.

%package -n vim-plugin-clang
Summary:	Clang format and rename integration for Vim
Summary(pl.UTF-8):	Integracja narzędzi Clang do formatowania i zmiany nazw z Vimem
Group:		Applications/Editors/Vim
Requires:	vim-rt >= 4:7.0
BuildArch:	noarch

%description -n vim-plugin-clang
Clang format and rename integration for Vim.

%description -n vim-plugin-clang -l pl.UTF-8
Integracja narzędzi Clang do formatowania i zmiany nazw z Vimem.

%prep
%setup -q -n %{name}-%{version}.src -a1 %{?with_rt:-a2} %{?with_lldb:-a3} %{?with_polly:-a4} -a5 -a6 %{?with_flang:-a7 -a8}
%{__mv} clang-%{version}.src tools/clang
%{?with_rt:%{__mv} compiler-rt-%{version}.src projects/compiler-rt}
%{?with_lldb:%{__mv} lldb-%{version}.src tools/lldb}
%{?with_polly:%{__mv} polly-%{version}.src tools/polly}
%{__mv} clang-tools-extra-%{version}.src tools/clang/tools/extra
%{__mv} lld-%{version}.src tools/lld
%if %{with flang}
%{__mv} flang-%{version}.src tools/flang
%{__mv} mlir tools/mlir
%endif

%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%if %{with flang}
%patch6 -p1
%endif
%patch7 -p1
%patch8 -p1
%patch9 -p1

grep -rl /usr/bin/env projects tools utils | xargs sed -i -e '1{
	s,^#!.*bin/env python,#!%{__python3},
	s,^#!.*bin/env perl,#!%{__perl},
}'

find -name '*.py' -print0 | xargs -0 sed -i -e '1{
	s,^#!.*bin/python.*,#!%{__python3},
}'

%build
install -d build

# Disabling assertions now, rec. by pure and needed for OpenGTL
# TESTFIX no PIC on ix86: http://llvm.org/bugs/show_bug.cgi?id=3801
cd build
CPPFLAGS="%{rpmcppflags} -D_FILE_OFFSET_BITS=64"

%if %{with lowmem}
export CFLAGS="%{rpmcflags} -g0"
export CXXFLAGS="%{rpmcxxflags} -g0"
export LDFLAGS="%{rpmldflags} -Wl,--reduce-memory-overheads"
%endif

%cmake .. \
	-DBUILD_SHARED_LIBS:BOOL=OFF \
	-DENABLE_LINKER_BUILD_ID:BOOL=ON \
	-DLLVM_BINDINGS_LIST:LIST="%{?with_ocaml:ocaml}" \
	-DLLVM_BINUTILS_INCDIR:STRING=%{_includedir} \
	-DLLVM_BUILD_LLVM_DYLIB:BOOL=ON \
	-DLLVM_ENABLE_ASSERTIONS:BOOL=OFF \
%if %{with apidocs}
	-DLLVM_ENABLE_DOXYGEN:BOOL=ON \
%endif
	%{?with_cxxmodules:-DLLVM_ENABLE_MODULES:BOOL=ON} \
	-DLLVM_ENABLE_PIC:BOOL=ON \
	-DLLVM_ENABLE_RTTI:BOOL=ON \
%if %{with doc}
	-DLLVM_ENABLE_SPHINX:BOOL=ON \
%endif
	%{?with_z3:-DLLVM_ENABLE_Z3_SOLVER:BOOL=ON} \
%if "%{_lib}" == "lib64"
	-DLLVM_LIBDIR_SUFFIX:STRING=64 \
%endif
%if "%{_lib}" == "libx32"
	-DLLVM_LIBDIR_SUFFIX:STRING=x32 \
%endif
	-DLLVM_LINK_LLVM_DYLIB:BOOL=ON \
	-DLLVM_DEFAULT_TARGET_TRIPLE:STRING=%{_target_platform} \
%if %{with lowmem}
	-DLLVM_PARALLEL_LINK_JOBS:STRING=1 \
%endif
	-DLLVM_TARGETS_TO_BUILD="%{targets_to_build}" \
%if %{with polly}
	%{cmake_on_off target_nvptx POLLY_ENABLE_GPGPU_CODEGEN} \
%endif
	-DSPHINX_WARNINGS_AS_ERRORS=OFF

%{__make} \
	VERBOSE=1 \
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
# workaround failed import of _lldb
cp -pnL %{_lib}/python%{py3_ver}/site-packages/lldb/_lldb.so tools/lldb/docs/lldb
%{__make} \
	LD_LIBRARY_PATH=$(pwd)/%{_lib} \
	-C tools/lldb/docs lldb-python-doc-package
%{__make} -C tools/lldb/docs lldb-cpp-doc
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -j1 -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# only some .pyc files are created by make install
%py3_comp $RPM_BUILD_ROOT%{py3_sitedir}
%py3_ocomp $RPM_BUILD_ROOT%{py3_sitedir}

# Adjust static analyzer installation (see -libexecdir patch)
abs_ca_libexecdir="%{_libexecdir}/clang-analyzer"
rel_ca_libexecdir="${abs_ca_libexecdir#%{_prefix}}"
%{__sed} -i -e "s,/\.\./libexec/,/..${rel_ca_libexecdir}/," $RPM_BUILD_ROOT%{_bindir}/scan-build
%py3_comp $RPM_BUILD_ROOT%{_datadir}/scan-view
%py3_ocomp $RPM_BUILD_ROOT%{_datadir}/scan-view

# not installed by cmake buildsystem
install build/bin/pp-trace $RPM_BUILD_ROOT%{_bindir}

%if %{with doc}
cp -p build/docs/man/*.1 $RPM_BUILD_ROOT%{_mandir}/man1
# these tools are not installed
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/{FileCheck,clang-tblgen,lldb-tblgen}.1
# make links
echo '.so llvm-ar.1' > $RPM_BUILD_ROOT%{_mandir}/man1/llvm-ranlib.1
%endif

# Move documentation back to build directory
%if %{with ocaml}
rm -rf ocamldocs
%{__mv} $RPM_BUILD_ROOT%{_docdir}/llvm/ocaml-html ocamldocs
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

%{__rm} $RPM_BUILD_ROOT%{_bindir}/{c-index-test,llvm-c-test}
# not this OS
%{__rm} $RPM_BUILD_ROOT%{_datadir}/clang/clang-format-bbedit.applescript
# use system six
%{?with_lldb:%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/{,__pycache__/}six*.py*}
# it seems it is used internally by an extra clang tool
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libfindAllSymbols.a

# disable completeness check incompatible with split packaging
%{__sed} -i -e '/^foreach(target .*IMPORT_CHECK_TARGETS/,/^endforeach/d; /^unset(_IMPORT_CHECK_TARGETS)/d' $RPM_BUILD_ROOT%{_libdir}/cmake/llvm/LLVMExports.cmake

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%post	-n clang-libs -p /sbin/ldconfig
%postun	-n clang-libs -p /sbin/ldconfig

%post	-n lldb -p /sbin/ldconfig
%postun	-n lldb -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CREDITS.TXT LICENSE.TXT README.txt %{?with_tests:llvm-testlog.txt}
%attr(755,root,root) %{_bindir}/bugpoint
%attr(755,root,root) %{_bindir}/dsymutil
%attr(755,root,root) %{_bindir}/llc
%attr(755,root,root) %{_bindir}/lli
%attr(755,root,root) %{_bindir}/llvm-addr2line
%attr(755,root,root) %{_bindir}/llvm-ar
%attr(755,root,root) %{_bindir}/llvm-as
%attr(755,root,root) %{_bindir}/llvm-bcanalyzer
%attr(755,root,root) %{_bindir}/llvm-bitcode-strip
%attr(755,root,root) %{_bindir}/llvm-cat
%attr(755,root,root) %{_bindir}/llvm-cfi-verify
%attr(755,root,root) %{_bindir}/llvm-cov
%attr(755,root,root) %{_bindir}/llvm-cvtres
%attr(755,root,root) %{_bindir}/llvm-cxxdump
%attr(755,root,root) %{_bindir}/llvm-cxxfilt
%attr(755,root,root) %{_bindir}/llvm-cxxmap
%attr(755,root,root) %{_bindir}/llvm-diff
%attr(755,root,root) %{_bindir}/llvm-dis
%attr(755,root,root) %{_bindir}/llvm-dlltool
%attr(755,root,root) %{_bindir}/llvm-dwarfdump
%attr(755,root,root) %{_bindir}/llvm-dwp
%attr(755,root,root) %{_bindir}/llvm-exegesis
%attr(755,root,root) %{_bindir}/llvm-extract
%attr(755,root,root) %{_bindir}/llvm-gsymutil
%attr(755,root,root) %{_bindir}/llvm-ifs
%attr(755,root,root) %{_bindir}/llvm-install-name-tool
%attr(755,root,root) %{_bindir}/llvm-jitlink
%attr(755,root,root) %{_bindir}/llvm-lib
%attr(755,root,root) %{_bindir}/llvm-libtool-darwin
%attr(755,root,root) %{_bindir}/llvm-link
%attr(755,root,root) %{_bindir}/llvm-lipo
%attr(755,root,root) %{_bindir}/llvm-lto
%attr(755,root,root) %{_bindir}/llvm-lto2
%attr(755,root,root) %{_bindir}/llvm-mc
%attr(755,root,root) %{_bindir}/llvm-mca
%attr(755,root,root) %{_bindir}/llvm-ml
%attr(755,root,root) %{_bindir}/llvm-modextract
%attr(755,root,root) %{_bindir}/llvm-mt
%attr(755,root,root) %{_bindir}/llvm-nm
%attr(755,root,root) %{_bindir}/llvm-objcopy
%attr(755,root,root) %{_bindir}/llvm-objdump
%attr(755,root,root) %{_bindir}/llvm-opt-report
%attr(755,root,root) %{_bindir}/llvm-otool
%attr(755,root,root) %{_bindir}/llvm-pdbutil
%attr(755,root,root) %{_bindir}/llvm-profdata
%attr(755,root,root) %{_bindir}/llvm-profgen
%attr(755,root,root) %{_bindir}/llvm-ranlib
%attr(755,root,root) %{_bindir}/llvm-rc
%attr(755,root,root) %{_bindir}/llvm-readelf
%attr(755,root,root) %{_bindir}/llvm-readobj
%attr(755,root,root) %{_bindir}/llvm-reduce
%attr(755,root,root) %{_bindir}/llvm-rtdyld
%attr(755,root,root) %{_bindir}/llvm-sim
%attr(755,root,root) %{_bindir}/llvm-size
%attr(755,root,root) %{_bindir}/llvm-split
%attr(755,root,root) %{_bindir}/llvm-strip
%attr(755,root,root) %{_bindir}/llvm-stress
%attr(755,root,root) %{_bindir}/llvm-strings
%attr(755,root,root) %{_bindir}/llvm-symbolizer
%attr(755,root,root) %{_bindir}/llvm-tapi-diff
%attr(755,root,root) %{_bindir}/llvm-tblgen
%attr(755,root,root) %{_bindir}/llvm-undname
%attr(755,root,root) %{_bindir}/llvm-windres
%attr(755,root,root) %{_bindir}/llvm-xray
%attr(755,root,root) %{_bindir}/opt
%attr(755,root,root) %{_bindir}/sancov
%attr(755,root,root) %{_bindir}/sanstats
%attr(755,root,root) %{_bindir}/split-file
%attr(755,root,root) %{_bindir}/verify-uselistorder
%if %{with doc}
%{_mandir}/man1/bugpoint.1*
%{_mandir}/man1/dsymutil.1*
%{_mandir}/man1/lit.1*
%{_mandir}/man1/llc.1*
%{_mandir}/man1/lli.1*
%{_mandir}/man1/llvm-addr2line.1*
%{_mandir}/man1/llvm-ar.1*
%{_mandir}/man1/llvm-as.1*
%{_mandir}/man1/llvm-bcanalyzer.1*
%{_mandir}/man1/llvm-cov.1*
%{_mandir}/man1/llvm-cxxfilt.1*
%{_mandir}/man1/llvm-cxxmap.1*
%{_mandir}/man1/llvm-diff.1*
%{_mandir}/man1/llvm-dis.1*
%{_mandir}/man1/llvm-dwarfdump.1*
%{_mandir}/man1/llvm-exegesis.1*
%{_mandir}/man1/llvm-extract.1*
%{_mandir}/man1/llvm-install-name-tool.1*
%{_mandir}/man1/llvm-lib.1*
%{_mandir}/man1/llvm-libtool-darwin.1*
%{_mandir}/man1/llvm-link.1*
%{_mandir}/man1/llvm-lipo.1*
%{_mandir}/man1/llvm-locstats.1*
%{_mandir}/man1/llvm-mca.1*
%{_mandir}/man1/llvm-nm.1*
%{_mandir}/man1/llvm-objcopy.1*
%{_mandir}/man1/llvm-objdump.1*
%{_mandir}/man1/llvm-otool.1*
%{_mandir}/man1/llvm-pdbutil.1*
%{_mandir}/man1/llvm-profdata.1*
%{_mandir}/man1/llvm-profgen.1*
%{_mandir}/man1/llvm-ranlib.1*
%{_mandir}/man1/llvm-readelf.1*
%{_mandir}/man1/llvm-readobj.1*
%{_mandir}/man1/llvm-size.1*
%{_mandir}/man1/llvm-stress.1*
%{_mandir}/man1/llvm-strings.1*
%{_mandir}/man1/llvm-strip.1*
%{_mandir}/man1/llvm-symbolizer.1*
%{_mandir}/man1/llvm-tblgen.1*
%{_mandir}/man1/opt.1*
%{_mandir}/man1/tblgen.1*
%endif

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/LLVMgold.so
%attr(755,root,root) %{_libdir}/libLLVM-%{abi}.so
# non-soname symlink
%attr(755,root,root) %{_libdir}/libLLVM-%{version}.so
%attr(755,root,root) %{_libdir}/libLTO.so.13
%attr(755,root,root) %{_libdir}/libRemarks.so.13
%attr(755,root,root) %{_libdir}/libclang-cpp.so.13

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/llvm-config
%attr(755,root,root) %{_libdir}/libLLVM.so
%attr(755,root,root) %{_libdir}/libLTO.so
%attr(755,root,root) %{_libdir}/libRemarks.so
%attr(755,root,root) %{_libdir}/libclang-cpp.so
%{_libdir}/libLLVM*.a
%{_includedir}/llvm
%{_includedir}/llvm-c
%{_libdir}/cmake/llvm
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
%doc tools/polly/{CREDITS.txt,LICENSE.TXT,README} tools/polly/www/{bugs,changelog,contributors}.html
%attr(755,root,root) %{_libdir}/LLVMPolly.so
%{?with_target_nvptx:%attr(755,root,root) %{_libdir}/libGPURuntime.so}

%files polly-devel
%defattr(644,root,root,755)
%{_libdir}/libPolly.a
%{_libdir}/libPollyISL.a
%{?with_target_nvptx:%{_libdir}/libPollyPPCG.a}
%{_includedir}/polly
%{_libdir}/cmake/polly
%endif

%files -n clang
%defattr(644,root,root,755)
%doc clang-docs/{LICENSE.TXT,NOTES.txt,README.txt} %{?with_tests:clang-testlog.txt}
%attr(755,root,root) %{_bindir}/clang
%attr(755,root,root) %{_bindir}/clang++
%attr(755,root,root) %{_bindir}/clang-%{abi}
%attr(755,root,root) %{_bindir}/clang-check
%attr(755,root,root) %{_bindir}/clang-cl
%attr(755,root,root) %{_bindir}/clang-cpp
%attr(755,root,root) %{_bindir}/clang-doc
%attr(755,root,root) %{_bindir}/clang-format
%attr(755,root,root) %{_bindir}/clang-offload-bundler
%attr(755,root,root) %{_bindir}/clang-offload-wrapper
%attr(755,root,root) %{_bindir}/clang-repl
%attr(755,root,root) %{_bindir}/git-clang-format
%dir %{_libdir}/clang
%dir %{_libdir}/clang/%{version}
%{_libdir}/clang/%{version}/include
%if %{with rt}
%ifarch %{x8664} aarch64
%dir %{_libdir}/clang/%{version}/bin
%attr(755,root,root) %{_libdir}/clang/%{version}/bin/hwasan_symbolize
%endif
%ifarch %{ix86} %{x8664} aarch64 armv7hl armv7hnl
%dir %{_libdir}/clang/%{version}/lib
%dir %{_libdir}/clang/%{version}/lib/linux
%dir %{_libdir}/clang/%{version}/share
%endif
%ifarch x32
%if %{with multilib}
%dir %{_libdir}/clang/%{version}/lib
%dir %{_libdir}/clang/%{version}/lib/linux
%dir %{_libdir}/clang/%{version}/share
%endif
%endif
%ifarch %{ix86}
%{_libdir}/clang/%{version}/lib/linux/clang_rt.*-i*86.o
%{_libdir}/clang/%{version}/lib/linux/libclang_rt.*-i*86.a
%attr(755,root,root) %{_libdir}/clang/%{version}/lib/linux/libclang_rt.*-i*86.so
%endif
%ifarch %{x8664}
%{_libdir}/clang/%{version}/lib/linux/clang_rt.*-x86_64.o
%{_libdir}/clang/%{version}/lib/linux/libclang_rt.*-x86_64.a
%attr(755,root,root) %{_libdir}/clang/%{version}/lib/linux/libclang_rt.*-x86_64.so
%{_libdir}/clang/%{version}/lib/linux/libclang_rt.*-x86_64.a.syms
%endif
%ifarch aarch64
%{_libdir}/clang/%{version}/lib/linux/clang_rt.*-aarch64.o
%{_libdir}/clang/%{version}/lib/linux/libclang_rt.*-aarch64.a
%attr(755,root,root) %{_libdir}/clang/%{version}/lib/linux/libclang_rt.*-aarch64.so
%{_libdir}/clang/%{version}/lib/linux/libclang_rt.*-aarch64.a.syms
%endif
%ifarch armv7hl armv7hnl
%{_libdir}/clang/%{version}/lib/linux/clang_rt.*-armhf.o
%{_libdir}/clang/%{version}/lib/linux/libclang_rt.*-armhf.a
%attr(755,root,root) %{_libdir}/clang/%{version}/lib/linux/libclang_rt.*-armhf.so
%{_libdir}/clang/%{version}/lib/linux/libclang_rt.*-armhf.a.syms
%endif
%ifarch %{ix86} %{x8664} %{arm} aarch64 mips mips64 ppc64
%{_libdir}/clang/%{version}/share/asan_ignorelist.txt
%endif
%ifarch %{ix86} %{x8664} mips64 aarch64 armv7hl armv7hnl
%{_libdir}/clang/%{version}/share/cfi_ignorelist.txt
%endif
%ifarch %{x8664} aarch64 mips64
%{_libdir}/clang/%{version}/share/dfsan_abilist.txt
%{_libdir}/clang/%{version}/share/msan_ignorelist.txt
%endif
%ifarch %{x8664} aarch64
%{_libdir}/clang/%{version}/share/hwasan_ignorelist.txt
%endif
%ifarch x32
%if %{with multilib}
%{_libdir}/clang/%{version}/share/asan_ignorelist.txt
%{_libdir}/clang/%{version}/share/cfi_ignorelist.txt
%{_libdir}/clang/%{version}/share/dfsan_abilist.txt
%{_libdir}/clang/%{version}/share/msan_ignorelist.txt
%{_libdir}/clang/%{version}/share/hwasan_ignorelist.txt
%endif
%endif
%endif
%dir %{_datadir}/clang
%{_datadir}/clang/clang-format-diff.py

%files -n clang-libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libclang.so.%{abi}
%attr(755,root,root) %{_libdir}/libclang.so.*.*.*

%if %{with rt} && %{with multilib}
%ifarch %{x8664} x32
%files -n clang-multilib
%defattr(644,root,root,755)
%{_libdir}/clang/%{version}/lib/linux/clang_rt.*-i386.o
%{_libdir}/clang/%{version}/lib/linux/libclang_rt.*-i386.a
%attr(755,root,root) %{_libdir}/clang/%{version}/lib/linux/libclang_rt.*-i386.so
%endif
%ifarch x32
%{_libdir}/clang/%{version}/lib/linux/clang_rt.*-x86_64.o
%{_libdir}/clang/%{version}/lib/linux/libclang_rt.*-x86_64.a
%attr(755,root,root) %{_libdir}/clang/%{version}/lib/linux/libclang_rt.*-x86_64.so
%{_libdir}/clang/%{version}/lib/linux/libclang_rt.*-x86_64.a.syms
%endif
%endif

%files -n clang-analyzer
%defattr(644,root,root,755)
%dir %{_libexecdir}/clang-analyzer
# perl tools
%attr(755,root,root) %{_bindir}/scan-build
%attr(755,root,root) %{_libexecdir}/clang-analyzer/c++-analyzer
%attr(755,root,root) %{_libexecdir}/clang-analyzer/ccc-analyzer
%{_datadir}/scan-build
%{_mandir}/man1/scan-build.1*
# python tools
%attr(755,root,root) %{_bindir}/analyze-build
%attr(755,root,root) %{_bindir}/intercept-build
%attr(755,root,root) %{_bindir}/scan-build-py
%attr(755,root,root) %{_bindir}/scan-view
%attr(755,root,root) %{_libexecdir}/clang-analyzer/analyze-c++
%attr(755,root,root) %{_libexecdir}/clang-analyzer/analyze-cc
%attr(755,root,root) %{_libexecdir}/clang-analyzer/intercept-c++
%attr(755,root,root) %{_libexecdir}/clang-analyzer/intercept-cc
%{_prefix}/lib/libear
%{_prefix}/lib/libscanbuild
%{_datadir}/scan-view

%files -n clang-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libclang.so
%{_libdir}/libclang*.a
%{_includedir}/clang
%{_includedir}/clang-c
%{_includedir}/clang-tidy
%{_libdir}/cmake/clang

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
%doc tools/clang/tools/extra/{CODE_OWNERS.TXT,README.txt}
%attr(755,root,root) %{_bindir}/clang-apply-replacements
%attr(755,root,root) %{_bindir}/clang-change-namespace
%attr(755,root,root) %{_bindir}/clang-extdef-mapping
%attr(755,root,root) %{_bindir}/clang-include-fixer
%attr(755,root,root) %{_bindir}/clang-move
%attr(755,root,root) %{_bindir}/clang-query
%attr(755,root,root) %{_bindir}/clang-refactor
%attr(755,root,root) %{_bindir}/clang-rename
%attr(755,root,root) %{_bindir}/clang-reorder-fields
%attr(755,root,root) %{_bindir}/clang-scan-deps
%attr(755,root,root) %{_bindir}/clang-tidy
%attr(755,root,root) %{_bindir}/clangd
%attr(755,root,root) %{_bindir}/diagtool
%attr(755,root,root) %{_bindir}/find-all-symbols
%attr(755,root,root) %{_bindir}/hmaptool
%attr(755,root,root) %{_bindir}/modularize
%attr(755,root,root) %{_bindir}/pp-trace
%attr(755,root,root) %{_bindir}/run-clang-tidy
%{_datadir}/clang/clang-include-fixer.py
%{_datadir}/clang/clang-tidy-diff.py
%{_datadir}/clang/run-find-all-symbols.py

%files -n lld
%defattr(644,root,root,755)
%doc tools/lld/{LICENSE.TXT,README.md}
%attr(755,root,root) %{_bindir}/ld.lld
%attr(755,root,root) %{_bindir}/ld64.lld
%attr(755,root,root) %{_bindir}/ld64.lld.darwinnew
%attr(755,root,root) %{_bindir}/ld64.lld.darwinold
%attr(755,root,root) %{_bindir}/lld
%attr(755,root,root) %{_bindir}/lld-link
%attr(755,root,root) %{_bindir}/wasm-ld

%files -n lld-devel
%defattr(644,root,root,755)
%{_libdir}/liblld[ACDEHMRWXY]*.a
%{_includedir}/lld
%{_libdir}/cmake/lld

%if %{with lldb}
%files -n lldb
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/lldb
%attr(755,root,root) %{_bindir}/lldb-argdumper
%attr(755,root,root) %{_bindir}/lldb-instr
%attr(755,root,root) %{_bindir}/lldb-server
%attr(755,root,root) %{_bindir}/lldb-vscode
%attr(755,root,root) %{_libdir}/liblldb.so.%{version}
%attr(755,root,root) %ghost %{_libdir}/liblldb.so.13
%attr(755,root,root) %ghost %{_libdir}/liblldbIntelFeatures.so.13
%dir %{py3_sitedir}/lldb
%attr(755,root,root) %{py3_sitedir}/lldb/lldb-argdumper
%{py3_sitedir}/lldb/formatters
%{py3_sitedir}/lldb/utils
%{py3_sitedir}/lldb/__init__.py
%{py3_sitedir}/lldb/__pycache__
%{py3_sitedir}/lldb/embedded_interpreter.py
%dir %{py3_sitedir}/lldb/plugins
%{py3_sitedir}/lldb/plugins/__pycache__
%{py3_sitedir}/lldb/plugins/__init__.py
%{py3_sitedir}/lldb/plugins/scripted_process.py
%attr(755,root,root) %{py3_sitedir}/lldb/_lldb.so

%files -n lldb-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblldb.so
%attr(755,root,root) %{_libdir}/liblldbIntelFeatures.so
%{_includedir}/lldb
%endif

%if %{with ocaml}
%files ocaml
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/ocaml/stublibs/dllllvm*.so
%dir %{_libdir}/ocaml/llvm
%{_libdir}/ocaml/llvm/llvm*.cma
%{_libdir}/ocaml/llvm/llvm*.cmi
%{_libdir}/ocaml/META.llvm*

%files ocaml-devel
%defattr(644,root,root,755)
%{_libdir}/ocaml/llvm/libllvm*.a
%{_libdir}/ocaml/llvm/llvm*.a
%{_libdir}/ocaml/llvm/llvm*.cmx
%{_libdir}/ocaml/llvm/llvm*.cmxa
%{_libdir}/ocaml/llvm/llvm*.mli

%files ocaml-doc
%defattr(644,root,root,755)
%doc ocamldocs/*
%endif

%files opt-viewer
%defattr(644,root,root,755)
%{_datadir}/opt-viewer

%files -n vim-plugin-clang
%defattr(644,root,root,755)
%{_datadir}/clang/clang-format.py
%{_datadir}/clang/clang-rename.py
