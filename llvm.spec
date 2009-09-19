# TODO
# - gcc/c++ packages: http://cvs.fedoraproject.org/viewvc/rpms/llvm/devel/llvm.spec?revision=HEAD&view=markup
# - test gcc pkgs and all
#
%define		lgcc_vertar		4.2
%define		lgcc_version	4.2
Summary:	The Low Level Virtual Machine (An Optimizing Compiler Infrastructure)
Summary(pl.UTF-8):	Niskopoziomowa maszyna wirtualna (infrastruktura kompilatora optymalizującego)
Name:		llvm
Version:	2.6
Release:	0.1
License:	University of Illinois/NCSA Open Source License
Group:		Development/Languages
Source0:	http://llvm.org/prereleases/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	d4d2cfbb962eca0c96aa1d794e23a681
Source1:	http://llvm.org/prereleases/2.6/clang-%{version}.tar.gz
# Source1-md5:	80a2a9bbe8fa7c403b2ec7aca8b4108f
# http://llvm.org/bugs/show_bug.cgi?id=3153
Patch0:		%{name}-2.6-destdir.patch
Patch1:		%{name}-2.6-destdir-clang.patch
# http://llvm.org/bugs/show_bug.cgi?id=4911
Patch2:		%{name}-2.5-tclsh_check.patch
# Data files should be installed with timestamps preserved
Patch3:		%{name}-2.6-timestamp.patch
URL:		http://llvm.org/
BuildRequires:	bash
BuildRequires:	bison
BuildRequires:	doxygen
BuildRequires:	flex
BuildRequires:	graphviz
BuildRequires:	groff
BuildRequires:	libltdl-devel
BuildRequires:	libstdc++-devel >= 5:3.4
BuildRequires:	ocaml-ocamldoc
# gcc4 might be installed, but not current __cc
%if "%(echo %{cc_version} | cut -d. -f1,2)" < "3.4"
BuildRequires:	__cc >= 3.4
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/%{name}

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

%prep
%setup -q -a1
mv clang-*.* tools/clang
%patch0 -p0 -b .destdir
cd tools/clang
%patch1 -p0 -b .destdir-clang
cd ../..
%patch2 -p1 -b .tclsh_check
%patch3 -p1 -b .timestamp

%build
# Disabling assertions now, rec. by pure and needed for OpenGTL
# no PIC on ix86: http://llvm.org/bugs/show_bug.cgi?id=3239
#
# bash specific 'test a < b'
mkdir obj && cd obj
bash ../%configure \
	--libdir=%{_libdir}/%{name} \
	--datadir=%{_datadir}/%{name}-%{version} \
%ifarch %{ix86}
	--enable-pic=no \
%endif
	--disable-static \
	--disable-assertions \
	--enable-debug-runtime \
	--enable-jit \
	--enable-optimized \
	--enable-shared \
	--with-pic

# FIXME file this
# configure does not properly specify libdir
sed -i 's|(PROJ_prefix)/lib|(PROJ_prefix)/%{_lib}/%{name}|g' Makefile.config

%{__make} \
	OPTIMIZE_OPTION="%{rpmcflags} %{rpmcppflags}"

%install
rm -rf $RPM_BUILD_ROOT

cd obj
chmod -x examples/Makefile

%{__make} -j1 install \
	PROJ_docsdir=/moredocs \
	DESTDIR=$RPM_BUILD_ROOT
cd ..

# Static analyzer not installed by default:
# http://clang-analyzer.llvm.org/installation#OtherPlatforms
install -d $RPM_BUILD_ROOT%{_libdir}/clang-analyzer/libexec
# wrong path used
install -d $RPM_BUILD_ROOT%{_libexecdir}
mv $RPM_BUILD_ROOT/usr/libexec/clang-cc $RPM_BUILD_ROOT%{_libexecdir}/clang-cc
# link clang-cc for scan-build to find
ln -s %{_libexecdir}/clang-cc $RPM_BUILD_ROOT%{_libdir}/clang-analyzer/libexec/
# create launchers
for f in scan-{build,view}; do
  ln -s %{_libdir}/clang-analyzer/$f $RPM_BUILD_ROOT%{_bindir}/$f
done

cd tools/clang/utils
cp -p ccc-analyzer $RPM_BUILD_ROOT%{_libdir}/clang-analyzer/libexec/

for f in scan-build scanview.css sorttable.js; do
  cp -p $f $RPM_BUILD_ROOT%{_libdir}/clang-analyzer/
done
cd ../../..

cd tools/clang/tools/scan-view
cp -pr * $RPM_BUILD_ROOT%{_libdir}/clang-analyzer/
cd ../../../../

# Move documentation back to build directory
#
rm -rf moredocs
mv $RPM_BUILD_ROOT/moredocs .
rm moredocs/*.tar.gz
#rm moredocs/ocamldoc/html/*.tar.gz

# And prepare Clang documentation
#
rm -rf clang-docs
mkdir clang-docs
for f in LICENSE.TXT NOTES.txt README.txt TODO.txt; do
  ln tools/clang/$f clang-docs/
done
#rm -rf tools/clang/docs/{doxygen*,Makefile*,*.graffle,tools}

# Get rid of erroneously installed example files.
rm $RPM_BUILD_ROOT%{_libdir}/%{name}/*LLVMHello.*

# Remove deprecated tools.
rm $RPM_BUILD_ROOT%{_bindir}/gcc{as,ld}

# FIXME file this bug
sed -i 's,ABS_RUN_DIR/lib",ABS_RUN_DIR/%{_lib}/%{name}",' \
	$RPM_BUILD_ROOT%{_bindir}/llvm-config

chmod -x $RPM_BUILD_ROOT%{_libdir}/%{name}/*.a

# remove documentation makefiles:
# they require the build directory to work
find examples -name 'Makefile' | xargs -0r rm -f

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CREDITS.TXT LICENSE.TXT README.txt
%attr(755,root,root) %{_bindir}/bugpoint
%attr(755,root,root) %{_bindir}/llc
%attr(755,root,root) %{_bindir}/lli
%attr(755,root,root) %{_bindir}/opt
%attr(755,root,root) %{_bindir}/llvmc
%attr(755,root,root) %{_bindir}/llvm-*
%exclude %attr(755,root,root) %{_bindir}/llvm-config
%{_mandir}/man1/bugpoint.1*
%{_mandir}/man1/llc.1*
%{_mandir}/man1/lli.1*
%{_mandir}/man1/llvmc.1*
%{_mandir}/man1/llvm-*.1*
%{_mandir}/man1/llvmgcc.1*
%{_mandir}/man1/llvmgxx.1*
%{_mandir}/man1/opt.1*
#%{_mandir}/man1/stkrc.1*
%{_mandir}/man1/tblgen.1*

%files doc
%defattr(644,root,root,755)
%doc docs/*.{html,css} docs/img examples moredocs/html

%files devel
%defattr(644,root,root,755)
#%doc docs/doxygen
%attr(755,root,root) %{_bindir}/llvm-config
%{_includedir}/llvm
%{_includedir}/llvm-c
%{_libdir}/%{name}

%files -n clang
%defattr(644,root,root,755)
%doc clang-docs/*
%doc tools/clang/docs/*
%attr(755,root,root) %{_bindir}/clang*
%attr(755,root,root) %{_bindir}/FileCheck
%attr(755,root,root) %{_bindir}/FileUpdate
%attr(755,root,root) %{_bindir}/tblgen
%{_prefix}/lib/clang
%{_libexecdir}/clang-cc
%{_mandir}/man1/clang.1.*
%{_mandir}/man1/FileCheck.1.*

%files -n clang-analyzer
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/scan-build
%attr(755,root,root) %{_bindir}/scan-view
%dir %{_libdir}/clang-analyzer
%attr(755,root,root) %{_libdir}/clang-analyzer/scan-*
%{_libdir}/clang-analyzer/*.*
%dir %{_libdir}/clang-analyzer/libexec
%attr(755,root,root) %{_libdir}/clang-analyzer/libexec/*
%{_libdir}/clang-analyzer/Resource

%files ocaml
%defattr(644,root,root,755)
%doc moredocs/ocamldoc/html/*
%{_libdir}/ocaml/*.cma
%{_libdir}/ocaml/*.cmi

%files ocaml-devel
%defattr(644,root,root,755)
%{_libdir}/ocaml/*.a
%{_libdir}/ocaml/*.cmx*
%{_libdir}/ocaml/*.mli
