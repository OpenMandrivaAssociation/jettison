%{?_javapackages_macros:%_javapackages_macros}
Name:           jettison
Version:        1.3.3
Release:        2.0%{?dist}
Summary:        A JSON StAX implementation

License:        ASL 2.0
URL:            http://jettison.codehaus.org/
# svn export http://svn.codehaus.org/jettison/tags/jettison-1.3.3 jettison-1.3.3
# rm -rf jettison-1.3.3/trunk
# tar cvJf jettison-1.3.3.tar.xz jettison-1.3.3
Source0:        %{name}-%{version}.tar.xz
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# Change the POM to use the version of woodstox that we have available:
Patch0: %{name}-update-woodstox-version.patch

%if 0%{?rhel} <= 5
BuildRequires:     java-devel
Requires:          java
%else
BuildRequires:     java-devel >= 1:1.6.0
Requires:          java >= 1:1.6.0
%endif
BuildRequires:     jpackage-utils
BuildRequires:     maven-local
BuildRequires:     maven-compiler-plugin
BuildRequires:     maven-install-plugin
BuildRequires:     maven-jar-plugin
BuildRequires:     maven-javadoc-plugin
BuildRequires:     maven-release-plugin
BuildRequires:     maven-resources-plugin
BuildRequires:     woodstox-core
BuildRequires:     stax2-api
Requires:          jpackage-utils


%description
Jettison is a collection of Java APIs (like STaX and DOM) which read
and write JSON. This allows nearly transparent enablement of JSON based
web services in services frameworks like CXF or XML serialization
frameworks like XStream.


%package javadoc
Summary:           Javadocs for %{name}

Requires:          %{name} = %{version}-%{release}
Requires:          jpackage-utils

%description javadoc
This package contains the API documentation for %{name}.


%prep
%setup -q
%patch0 -p1
# We don't need wagon-webdav
%pom_xpath_remove pom:build/pom:extensions

%build
# Disable the tests until BZ#796739 is fixed:
mvn-rpmbuild -Dproject.build.sourceEncoding=UTF-8 -Dmaven.test.skip=true install javadoc:aggregate


%install
# Jar files:
install -d -m 755 %{buildroot}%{_javadir}
cp -p target/%{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar

# Javadoc files:
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}
cp -rp target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}/.

# POM files:
install -d -m 755 %{buildroot}%{_mavenpomdir}
cp -p pom.xml %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom

# Dependencies map:
%add_maven_depmap JPP-%{name}.pom %{name}.jar


%files
%doc src/main/resources/META-INF/LICENSE
%{_javadir}/%{name}.jar
%{_mavenpomdir}/JPP-%{name}.pom
%{_mavendepmapfragdir}/%{name}


%files javadoc
%doc src/main/resources/META-INF/LICENSE
%{_javadocdir}/%{name}


%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar  8 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.3.3-1
- Check woodstox version patch into SCM
- Upload jettison-1.3.3.tar.xz

* Fri Mar 08 2013 David Xie <david.scriptfan@gmail.com> - 1.3.3-1
- Update to v1.3.3

* Tue Feb 26 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.3.1-9
- Remove wagon-webdav build extension

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.3.1-7
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Fri Sep 21 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.3.1-6
- Install LICENSE file with javadoc package

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Mar 12 2012 Juan Hernandez <juan.hernandez at redhat.com> - 1.3.1-4
- Make sure the maven dependencies map is created and added

* Thu Feb 23 2012 Juan Hernandez <juan.hernandez at redhat.com> - 1.3.1-3
- Use maven to build and add the POM to the package

* Sun Jan 15 2012 Sandro Mathys <red at fedoraproject.org> - 1.3.1-2
- Drop the requirement for java* >= 1.6.0 for EL <= 5

* Sun Jan 15 2012 Sandro Mathys <red at fedoraproject.org> - 1.3.1-1
- New upstream release

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jun 30 2011 Sandro Mathys <red at fedoraproject.org> - 1.3-1
- New upstream version

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Apr 25 2010 Sandro Mathys <red at fedoraproject.org> - 1.2-1
- update to upstream 1.2

* Sun Jun 28 2009 Sandro Mathys <red at fedoraproject.org> - 1.1-1
- initial build
