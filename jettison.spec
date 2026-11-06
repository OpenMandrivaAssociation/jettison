Name:		jettison
Version:	1.5.7
Release:	1
Summary:	StAX implementation for JSON
Group:		Development/Java
License:	ASL 2.0
URL:		https://github.com/jettison-json/jettison
Source0:	https://github.com/jettison-json/jettison/archive/refs/tags/jettison-%{version}.tar.gz#/jettison-%{version}.tar.gz

BuildArch:	noarch
Obsoletes:	%{name}-javadoc < %{version}
BuildRequires:	maven
BuildRequires:	java-current-devel
BuildSystem:	maven
BuildOption(install):	--file-name jettison

%description
Jettison maps between XML and JSON through the StAX API, including
the Mapped and BadgerFish conventions. 1.5.7 limits recursion depth
and JSON array length. It uses the JDK StAX API. Tests are skipped.

%prep
%autosetup -n jettison-jettison-%{version}
# packaging bundle needs the Felix plugin, which is not packaged.
# The compiler pin is newer than the toolchain plugin. Test deps are
# junit and woodstox, and woodstox is not packaged.
python - <<'PY'
import re
from pathlib import Path

pom = Path("pom.xml")
text = pom.read_text()
old_pack = "<packaging>bundle</packaging>"
if old_pack not in text:
    raise SystemExit("packaging missing")
text = text.replace(old_pack, "<packaging>jar</packaging>", 1)
text, n = re.subn(
    r"\s*<dependencies>.*?</dependencies>",
    "",
    text,
    count=1,
    flags=re.S,
)
if n != 1:
    raise SystemExit(f"dependencies {n}")
old_ver = "        <artifactId>maven-compiler-plugin</artifactId>\n        <version>3.15.0</version>"
new_ver = "        <artifactId>maven-compiler-plugin</artifactId>"
if old_ver not in text:
    raise SystemExit("compiler version missing")
text = text.replace(old_ver, new_ver, 1)
old_opt = "          <optimize>true</optimize>\n"
if old_opt not in text:
    raise SystemExit("optimize missing")
text = text.replace(old_opt, "", 1)
text, n = re.subn(
    r"\s*<plugin>\s*<groupId>org\.sonatype\.central</groupId>.*?</plugin>",
    "",
    text,
    count=1,
    flags=re.S,
)
if n != 1:
    raise SystemExit(f"central {n}")
text, n = re.subn(
    r"\s*<plugin>\s*<groupId>org\.apache\.felix</groupId>.*?</plugin>",
    "",
    text,
    count=1,
    flags=re.S,
)
if n != 1:
    raise SystemExit(f"bundle {n}")
pom.write_text(text)
PY

%files -f .mfiles
%doc LICENSE README.md
