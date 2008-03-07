# Copyright (c) 2000-2007, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define gcj_support 1

# If you don't want to build with maven, and use straight ant instead,
# give rpmbuild option '--without maven'

%define with_maven %{!?_without_maven:1}%{?_without_maven:0}
%define without_maven %{?_without_maven:1}%{!?_without_maven:0}

%define section     free

Name:           jettison
Version:        1.0
Release:        %mkrel 0.0.1
Epoch:          0
Summary:        A JSON StAX Implementation
License:        Apache License
Url:            http://jettison.codehaus.org
Group:          Development/Java

Source0:        %{name}-%{version}.tar.bz2
# svn export http://svn.codehaus.org/jettison/tags/jettison-1.0

Source1:        %{name}-settings.xml
Source2:        %{name}-jpp-depmap.xml
Source3:        %{name}-build.xml
Patch0:         %{name}-BadgerFishXMLStreamWriterTest.patch

BuildRequires:  jpackage-utils >= 0:1.7.2
BuildRequires:  ant >= 0:1.6
BuildRequires:  junit >= 0:3.8.2
%if %{with_maven}
BuildRequires:  maven2 >= 2.0.4-10jpp
BuildRequires:  maven2-plugin-compiler
BuildRequires:  maven2-plugin-install
BuildRequires:  maven2-plugin-jar
BuildRequires:  maven2-plugin-javadoc
BuildRequires:  maven2-plugin-resources
BuildRequires:  maven2-plugin-release
BuildRequires:  maven2-plugin-surefire
%endif
Requires(post):    jpackage-utils >= 0:1.7.2
Requires(postun):  jpackage-utils >= 0:1.7.2
%if %{gcj_support}
BuildRequires:    java-gcj-compat-devel
%endif
BuildRequires:  jetty5
BuildRequires:  servletapi5
BuildRequires:  bea-stax-api
BuildRequires:  xml-commons-jaxp-1.3-apis

Requires:       jpackage-utils >= 0:1.7.2
Requires:       jetty5
Requires:       servletapi5
Requires:       bea-stax-api
Requires:  xml-commons-jaxp-1.3-apis

%if ! %{gcj_support}
BuildArch:      noarch
%endif

BuildRoot:      %{_tmppath}/%{name}-%{version}-buildroot

%description
Jettison is a collection of StAX parsers and writers which 
read and write JSON. This allows nearly transparent 
enablement of JSON based web services in services 
frameworks like CXF.
There are currently two included conventions for mapping 
JSON to XML. The first, is BadgerFish which implements the 
full XML infoset in JSON using various techniques. 
The second, is called the "mapped" convention. It allows 
you to manually map XML namespaces to JSON element prefixes.
Jettison was developed for usage in XFire and CXF to enable 
JSON based services.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Documentation

%description javadoc
%{summary}.

%prep
%setup -q -n %{name}-%{version}
cp %{SOURCE1} settings.xml
cp %{SOURCE3} build.xml
%patch0 -b .sav

%build
%if %{with_maven}
sed -i -e "s|<url>__JPP_URL_PLACEHOLDER__</url>|<url>file://`pwd`/.m2/repository</url>|g" settings.xml
sed -i -e "s|<url>__JAVADIR_PLACEHOLDER__</url>|<url>file://`pwd`/external_repo</url>|g" settings.xml
sed -i -e "s|<url>__MAVENREPO_DIR_PLACEHOLDER__</url>|<url>file://`pwd`/.m2/repository</url>|g" settings.xml
sed -i -e "s|<url>__MAVENDIR_PLUGIN_PLACEHOLDER__</url>|<url>file:///usr/share/maven2/plugins</url>|g" settings.xml
sed -i -e "s|<url>__ECLIPSEDIR_PLUGIN_PLACEHOLDER__</url>|<url>file:///usr/share/eclipse/plugins</url>|g" settings.xml

export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mkdir -p $MAVEN_REPO_LOCAL

mkdir external_repo
ln -s %{_javadir} external_repo/JPP

mvn-jpp \
        -e \
        -s $(pwd)/settings.xml \
        -Dmaven2.jpp.mode=true \
        -Dmaven2.jpp.depmap.file=%{SOURCE2} \
        -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
        install javadoc:javadoc
%else
export CLASSPATH=$(build-classpath \
bea-stax-api \
jetty5/jetty5 \
servletapi5 \
)
CLASSPATH=$CLASSPATH:target/classes:target/test-classes
%{ant} -Dbuild.sysclasspath=only jar javadoc
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -m 644 target/%{name}-%{version}.jar \
           $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
%add_to_maven_depmap org.codehaus.jettison %{name} %{version} JPP %{name}

# create unprefixed and unversioned symlinks
%create_jar_links

# poms
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/maven2/poms
install -pm 644 pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{name}.pom

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%aot_compile_rpm_bin

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_maven_depmap
%if %{gcj_support}
%{update_gcjdb}
%endif

%postun
%update_maven_depmap 
%if %{gcj_support}
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%{_javadir}/*.jar
%{_datadir}/maven2/poms/*
%{_mavendepmapfragdir}
%gcj_files

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}
