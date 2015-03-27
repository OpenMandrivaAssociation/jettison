%{?_javapackages_macros:%_javapackages_macros}
Name:           jettison
Version:        1.3.5
Release:        1
Summary:        A JSON StAX implementation
Group:		Development/Java
License:        ASL 2.0
URL:            http://jettison.codehaus.org/
# svn export http://svn.codehaus.org/jettison/tags/jettison-1.3.3 jettison-1.3.3
# rm -rf jettison-1.3.3/trunk
# tar cvJf jettison-1.3.3.tar.xz jettison-1.3.3
Source0:        http://repo1.maven.org/maven2/org/codehaus/jettison/jettison/1.3.5/jettison-1.3.5-sources.jar
BuildArch:      noarch

# Change the POM to use the version of woodstox that we have available:
Patch0: %{name}-update-woodstox-version.patch

BuildRequires:  maven-local
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-release-plugin)
BuildRequires:  mvn(org.codehaus:codehaus-parent:pom:)
BuildRequires:  mvn(org.codehaus.woodstox:woodstox-core-asl)
BuildRequires:  mvn(stax:stax-api)

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
%mvn_build -f

%install
%mvn_install

%files -f .mfiles
%doc src/main/resources/META-INF/LICENSE

%files javadoc -f .mfiles-javadoc
%doc src/main/resources/META-INF/LICENSE
