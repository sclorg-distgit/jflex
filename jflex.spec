%{?scl:%scl_package jflex}
%{!?scl:%global pkg_name %{name}}

%bcond_without desktop
%bcond_without emacs

Summary:        Fast Scanner Generator
Name:           %{?scl_prefix}jflex
Version:        1.6.1
Release:        8.1%{?dist}
License:        BSD
URL:            http://jflex.de/
BuildArch:      noarch

# ./create-tarball.sh %%{version}
Source0:        %{pkg_name}-%{version}-clean.tar.gz
Source2:        %{pkg_name}.desktop
Source3:        %{pkg_name}.png
Source4:        %{pkg_name}.1
Source5:        create-tarball.sh

BuildRequires:  %{?scl_prefix}maven-local
BuildRequires:  %{?scl_prefix}ant
BuildRequires:  %{?scl_prefix}jflex
BuildRequires:  %{?scl_prefix}junit
BuildRequires:  %{?scl_prefix}sonatype-oss-parent
BuildRequires:  java-devel
BuildRequires:  %{?scl_prefix}java_cup
%if %{with desktop}
BuildRequires:  desktop-file-utils
%endif
%if %{with emacs}
BuildRequires:  emacs
Requires:       emacs-filesystem >= %{_emacs_version}
%endif

%description
JFlex is a lexical analyzer generator (also known as scanner
generator) for Java, written in Java.  It is also a rewrite of the
very useful tool JLex which was developed by Elliot Berk at Princeton
University.  As Vern Paxson states for his C/C++ tool flex: They do
not share any code though.  JFlex is designed to work together with
the LALR parser generator CUP by Scott Hudson, and the Java
modification of Berkeley Yacc BYacc/J by Bob Jamison.  It can also be
used together with other parser generators like ANTLR or as a
standalone tool.

%package javadoc
Summary:        API documentation for %{pkg_name}

%description javadoc
This package provides %{summary}.

%prep
%setup -n %{pkg_name}-%{version} -q
%mvn_file : %{pkg_name}
%pom_add_dep java_cup:java_cup

%pom_remove_plugin :maven-antrun-plugin
%pom_remove_plugin :jflex-maven-plugin

# Tests fail with 320k stacks (default on i686), so lets increase
# stack to 16M to avoid stack overflows.  See rhbz#1119308
%pom_xpath_inject "pom:plugin[pom:artifactId='maven-surefire-plugin']/pom:configuration" "<argLine>-Xss16384k</argLine>"

%build
java -jar $(find-jar java_cup) -parser LexParse -interface -destdir src/main/java src/main/cup/LexParse.cup
jflex -d src/main/java/jflex --skel src/main/jflex/skeleton.nested src/main/jflex/LexScan.flex
%mvn_build

%if %{with emacs}
# Compile Emacs jflex-mode source
%{_emacs_bytecompile} lib/jflex-mode.el
%endif

%install
%mvn_install

# wrapper script for direct execution
%jpackage_script jflex.Main "" "" jflex:java_cup jflex true

# manpage
install -d -m 755 %{buildroot}%{_mandir}/man1
install -p -m 644 %{SOURCE4} %{buildroot}%{_mandir}/man1

# .desktop + icons
%if %{with desktop}
desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{SOURCE2}
install -d -m 755 %{buildroot}%{_datadir}/pixmaps
install -p -m 644 %{SOURCE3} %{buildroot}%{_datadir}/pixmaps/%{pkg_name}.png
%endif

# Emacs files
%if %{with emacs}
install -d -m 755 %{buildroot}%{_emacs_sitelispdir}/%{pkg_name}
install -p -m 644 lib/jflex-mode.el %{buildroot}%{_emacs_sitelispdir}/%{pkg_name}
install -p -m 644 lib/jflex-mode.elc %{buildroot}%{_emacs_sitelispdir}/%{pkg_name}
%endif

%files -f .mfiles
%doc doc
%doc COPYRIGHT
%{_bindir}/%{pkg_name}
%{_mandir}/man1/%{pkg_name}.1.gz
%if %{with desktop}
%{_datadir}/applications/%{pkg_name}.desktop
%{_datadir}/pixmaps/%{pkg_name}.png
%endif
%if %{with emacs}
%{_emacs_sitelispdir}/%{pkg_name}
%endif

%files javadoc
%doc COPYRIGHT
%doc %{_javadocdir}/%{pkg_name}

%changelog
* Wed Jun 21 2017 Java Maintainers <java-maint@redhat.com> - 1.6.1-8.1
- Automated package import and SCL-ization

* Fri Jun  2 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.6.1-8
- Don't hardcode java_cup JAR path

* Wed May 31 2017 Michael Simacek <msimacek@redhat.com> - 1.6.1-7
- Replace absolute path with a macro

* Tue Mar  7 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.6.1-6
- Add bconds for desktop and emacs

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jun 16 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.6.1-4
- Add missing build-requires

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Mar 17 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.6.1-1
- Update to upstream version 1.6.1

* Tue Jul  8 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.6.0-1
- Update to upstream version 1.6.0

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 12 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.5.1-1
- Update to upstream version 1.5.1

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.5.0-3
- Use Requires: java-headless rebuild (#1067528)

* Tue Jan 28 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.5.0-2
- Fix license tag

* Mon Jan 27 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.5.0-1
- Update to upstream version 1.5.0
- Build with Maven

* Fri Aug 02 2013 Michal Srb <msrb@redhat.com> - 0:1.4.3-16
- Add create-tarball.sh script to SRPM

* Thu Jun 20 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.4.3-15
- Fix javadoc generation
- Update to current packaging guidelines

* Thu Jun 20 2013 Michal Srb <msrb@redhat.com> - 0:1.4.3-14
- Build from clean tarball
- Install license file with javadoc package

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.4.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 22 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.4.3-12
- Install Emacs jflex-mode

* Thu Nov 22 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.4.3-11
- Remove bundled java_cup sources
- Resolves: rhbz#877051

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.4.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed May  2 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.4.3-9
- Fix license tag
- Import manpage from Debian's jflex 1.4.1-3 (GPL+)

* Thu Apr 19 2012 Jaromir Capik <jcapik@redhat.com> - 0:1.4.3-8
- Desktop file generated
- Icon created from the GPL licensed logo

* Mon Mar 12 2012 Jaromir Capik <jcapik@redhat.com> - 0:1.4.3-7
- Wrapper script generated
- Minor spec file changes according to the latest guidelines

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.4.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.4.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Feb 15 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.4.3-4
- Add dependency on java_cup in the maven pom.xml.

* Mon Feb 15 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.4.3-3
- Require java_cup.

* Wed Jan 20 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.4.3-3
- Provide JFlex.jar.
- Don't put java_cup classes in the jar.

* Fri Jan 8 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.4.3-2
- Add maven pom and depmaps.

* Fri Jan 8 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.4.3-1
- Update to 1.4.3.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.4.1-0.5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.4.1-0.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:1.4.1-0.3
- drop repotag

* Mon Mar 03 2008 Matt Wringe <mwringe@redhat.com> - 0:1.4.1-0jpp.2
- Add missing buildrequires on java_cup

* Fri Feb 22 2008 Matt Wringe <mwringe@redhat.com> - 0:1.4.1-0jpp.1
- Patch build file to allow bootstrap building

* Mon Feb 18 2008 Lubomir Kundrak <lkundrak@redhat.com> - 0:1.4.1-0jpp.1
- Naive attempt to update to newer version

* Mon Apr 02 2007 Matt Wringe <mwringe@redhat.com> - 0:1.3.5-2jpp.2
- Add patches jflex-CharSet_java.patch and jflex-StateSet_java.patch
  to allow building with the new gcj

* Mon Feb 12 2007 Matt Wringe <mwringe@redhat.com> - 0:1.3.5-2jpp.1
- Remove javadoc post and postun sections due to new jpp standard 
- Update makefile patch to compress jar
- Fix rpmlint issues

* Wed Jan 04 2006 Fernando Nasser <fnasser@redhat.com> - 0:1.3.5-2jpp
- First JPP 1.7 build

* Wed Nov 16 2005 Ralph Apel <r.apel at r-apel.de> - 0:1.3.5-1jpp
- First JPackage release
