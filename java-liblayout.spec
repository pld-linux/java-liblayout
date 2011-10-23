#
# Conditional build:
%bcond_without	javadoc		# don't build javadoc

%define		srcname		liblayout
%include	/usr/lib/rpm/macros.java
Summary:	CSS based layouting framework
Name:		java-%{srcname}
Version:	0.2.10
Release:	1
License:	LGPL v2+
Group:		Libraries/Java
Source0:	http://downloads.sourceforge.net/jfreereport/liblayout-%{version}.zip
# Source0-md5:	db60e4fde8dd6d6807523deb71ee34dc
URL:		http://reporting.pentaho.org/
BuildRequires:	ant
BuildRequires:	java-flute
BuildRequires:	java-libbase >= 1.1.3
BuildRequires:	java-libfonts
BuildRequires:	java-libloader
BuildRequires:	java-librepository
BuildRequires:	java-libxml
BuildRequires:	java-sac
BuildRequires:	java-xml-commons
BuildRequires:	jdk
BuildRequires:	jpackage-utils
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.553
Requires:	java-flute
Requires:	java-libbase >= 1.0.0
Requires:	java-libfonts >= 1.1.3
Requires:	java-libloader >= 1.1.3
Requires:	java-librepository >= 1.1.3
Requires:	java-libxml
Requires:	java-sac
Requires:	java-xml-commons-apis
Requires:	jpackage-utils
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LibLayout is a layouting framework. It is based on the Cascading
StyleSheets standard. The layouting expects to receive its content as
a DOM structure (although it does not rely on the W3C-DOM API).

%package javadoc
Summary:	Javadoc for LibLayout
Group:		Documentation
Requires:	jpackage-utils

%description javadoc
Javadoc for LibLayout.

%prep
%setup -qc
%undos README.txt licence-LGPL.txt ChangeLog.txt
find -name "*.jar" | xargs rm -v
install -d lib

%build
build-jar-repository -s -p lib flute libloader librepository libxml libfonts \
	sac jaxp libbase commons-logging-api
%ant jar %{?with_javadoc:javadoc}

%install
rm -rf $RPM_BUILD_ROOT

# jars
install -d $RPM_BUILD_ROOT%{_javadir}
cp -p build/lib/%{srcname}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-%{version}.jar
ln -s %{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}.jar

# javadoc
%if %{with javadoc}
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
cp -a build/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
ln -s %{srcname}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{srcname} # ghost symlink
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{srcname}-%{version} %{_javadocdir}/%{srcname}

%files
%defattr(644,root,root,755)
%doc licence-LGPL.txt README.txt ChangeLog.txt
%{_javadir}/%{srcname}-%{version}.jar
%{_javadir}/%{srcname}.jar

%if %{with javadoc}
%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{srcname}-%{version}
%ghost %{_javadocdir}/%{srcname}
%endif
