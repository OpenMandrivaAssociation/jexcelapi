%{?_javapackages_macros:%_javapackages_macros}
%global oname jxl

Name:           jexcelapi
Version:        2.6.12
Release:        9.1
Summary:        A Java API to read, write and modify Excel spreadsheets
Group:		Development/Java
License:        LGPLv3

URL:            http://www.andykhan.com/jexcelapi
Source0:        http://www.andykhan.com/jexcelapi/jexcelapi_2_6_12.tar.gz
Source1:        http://repo1.maven.org/maven2/net/sourceforge/jexcelapi/jxl/2.6.12/jxl-2.6.12.pom
Patch0:         jexcelapi-build.patch
Requires:       java >= 0:1.5.0
Requires:       log4j12
Requires:       jpackage-utils

BuildRequires:  jpackage-utils >= 0:1.7.3
BuildRequires:  java-devel >= 0:1.5.0
BuildRequires:  ant
BuildRequires:  jflex
BuildRequires:  findutils
BuildRequires:  sed
BuildRequires:  log4j12
BuildArch:      noarch

%description
Jexcelapi allows Java developers to read Excel spreadsheets and generate
Excel spreadsheets dynamically. In addition, it contains a mechanism which
allows Java applications to read a spreadsheet, modify some cells and write
the modified spreadsheet.

Thanks to jexcelapi non Windows operating systems can run pure Java
applications which process and deliver Excel spreadsheets. Because it
is Java, this API may be invoked from within a servlet, thus giving access
to Excel functionality over internet and intranet web applications.

Features:
- Reads data from Excel 95, 97, 2000 workbooks
- Reads and writes formulas (Excel 97 and later only)
- Generates spreadsheets in Excel 97 format
- Supports font, number and date formatting
- Supports shading and coloring of cells
- Modifies existing worksheets


%package        javadoc

Summary:        API documentation for %{name}

%description    javadoc
API documentation for %{name}.

%prep
%setup -n %{name} -q

# Clean up binary leftovers
find . -name "*.jar" -exec rm -f {} \;
find . -name "*.class" -exec rm -f {} \;

# Clean up temp files (confuses javadoc 1.3.1)
find . -name ".#*" -exec rm -f {} \;

%patch0 -p1 -b .build
sed -i "s|%{_javadir}/jflex.jar|%{_javadir}/jflex/jflex.jar|" build/build.xml

%build
pushd build
cat > build.properties <<EOBP
logger=Log4jLogger
loggerClasspath=$(build-classpath log4j12-1.2.17)
EOBP

[ -z "$JAVA_HOME" ] && export JAVA_HOME=%{_jvmdir}/java
export CLASSPATH=$(build-classpath jflex)

mkdir out
ant jxlall
popd

# html doc files should not be executable
chmod -x index.html tutorial.html

%install
# jars
install -d -m 0755 $RPM_BUILD_ROOT%{_javadir}/%{name}
install -m 0644 jxl.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar
ln -s %{name}.jar $RPM_BUILD_ROOT%{_javadir}/jxl.jar

# pom
install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}.pom
%add_maven_depmap JPP-%{name}.pom %{name}.jar

# javadoc
install -d -m 0755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -r docs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%files -f .mfiles
%{_javadir}/jxl.jar
%doc *.html

%files javadoc
%doc index.html
%{_javadocdir}/%{name}

%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.12-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.12-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Oct 21 2012 Mat Booth <fedora@matbooth.co.uk> - 2.6.12-5
- Remove unneeded build requirement on jlex.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Mar  1 2012 Andy Grimm <agrimm@gmail.com> - 2.6.12-3
- add jpackage-utils requirement for javadoc subpackage

* Thu Feb 16 2012 Andy Grimm <agrimm@gmail.com> - 2.6.12-2
- bug fixes

* Thu Feb 16 2012 Andy Grimm <agrimm@gmail.com> - 2.6.12-1
- Initial package
