Name:           jettison
Version:        1.3
Release:        3
Summary:        A JSON StAX implementation
Group:          Development/Java
License:        ASL 2.0
URL:            http://jettison.codehaus.org/
Source0:        http://repo1.maven.org/maven2/org/codehaus/%{name}/%{name}/%{version}/%{name}-%{version}-sources.jar
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:     java-devel >= 0:1.6.0
BuildRequires:     jpackage-utils
Requires:          java >= 0:1.6.0
Requires:          jpackage-utils

%description
Jettison is a collection of Java APIs (like STaX and DOM) which read
and write JSON. This allows nearly transparent enablement of JSON based
web services in services frameworks like CXF or XML serialization
frameworks like XStream.


%package javadoc
Summary:           Javadocs for jettison
Group:             Development/Java
Requires:          %{name} = %{version}-%{release}
Requires:          jpackage-utils

%description javadoc
jettison development documentation.


%prep
%setup -q -c
mkdir target doc


%build
javac -d target `find -name '*.java'`
jar -cf %{name}-%{version}.jar -C target .
javadoc -author -version -public -d doc `find . -name '*.java'`

%install
rm -rf $RPM_BUILD_ROOT

# jar
install -d $RPM_BUILD_ROOT%{_javadir}
install -m644 %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

# javadoc
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -rp doc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc META-INF/LICENSE
%{_javadir}/%{name}-%{version}.jar
%{_javadir}/%{name}.jar

%files javadoc
%defattr(-,root,root,-)
%dir %{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}
%{_javadocdir}/%{name}-%{version}/*




%changelog
* Sun Nov 27 2011 Guilherme Moro <guilherme@mandriva.com> 1.3-3
+ Revision: 734046
- rebuild
- imported package jettison

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

* Fri Mar 07 2008 Alexander Kurtakov <akurtakov@mandriva.org> 0:1.0-0.0.2mdv2008.1
+ Revision: 181216
- fix javadoc package group
- add maven2-plugin-release BR
- import jettison


