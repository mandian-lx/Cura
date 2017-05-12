%define oname Cura
%define lname %(echo %oname | tr [:upper:] [:lower:])

Summary:	A 3D printer slicing GUI built on top of the Uranium framework 
Name:		%{oname}
Version:	2.3.1
Release:	0
Group:		Development/Other
License:	AGPLv3+
URL:		https://github.com/Ultimaker/%{name}
Source0:	https://github.com/Ultimaker/%{name}/archive/%{version}/%{name}-%{version}.tar.gz
Patch0:	 	%{oname}-2.3.1-CMakeLists.patch
Patch1:		%{oname}-2.3.1-plugins.patch
BuildArch:	noarch

BuildRequires:	cmake
BuildRequires:	desktop-file-utils
BuildRequires:	font(opensans)
BuildRequires:	pkgconfig(python)
BuildRequires:  python-uranium == %{version}
# test
#BuildRequires:  python-pytest

Requires:	CuraEngine == %{version}
Requires:	font(opensans)
Requires:	python-uranium == %{version}
Requires:	python-arcus == %{version}
#Requires:	python-qt5
Requires:	python-qt5-core
Requires:	python-qt5-gui
Requires:	python-qt5-opengl
Requires:	python-qt5-qml
Requires:	python-qt5-quick
Requires:	python-qt5-quickwidgets
Requires:	python-qt5-widgets
Requires:	python3egg(pyserial)
Requires:	font-ttf-open-sans

%description
CuraEngine is a powerful, fast and robust engine for processing 3D
models into 3D printing instruction for Ultimaker and other GCode
based 3D printers.

It is part of the larger open source project called "Cura".

%files -n %{name}.lang
%{_bindir}/%{lname}
%{py_puresitedir}/cura
%{_datadir}/%{lname}
%{_datadir}/uranium/
%{_datadir}/applications/*desktop
%{_datadir}/mime/packages/%{lname}.xml
%doc README.md
%doc CHANGES
%doc LICENSE

#----------------------------------------------------------------------------

%prep
%setup -q

# Apply all patches
%patch0 -p1 -b .orig
%patch1 -p1 #-b .plugins

# Use system fonts
rm -rf %{buildroot}%{_datadir}/%{name}/resources/themes/%{lname}/fonts/
ln -s %{_datadir}/fonts/open-sans/ %{buildroot}%{_datadir}/%{name}/resources/themes/%{lname}/fonts

%build
%cmake
%make

%install
%makeinstall_std -C build

# Fix .desktop
desktop-file-edit \
	--remove-key="Version" \
	%{buildroot}%{_datadir}/applications/%{lname}.desktop

# Add missing icons
#%__install -dm 0755%{buildroot}%{_iconsdir}/hicolor/{16x16,48x48,64x64}/apps/
#convert -scale 16x16 data/%{name}_32.png %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png
#convert -scale 48x48 data/%{name}_128.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png
#convert -scale 64x64 data/%{name}_128.png %{buildroot}%{_iconsdir}/hicolor/64x64/apps/%{name}.png

# Use system fonts
#rm -rf %{buildroot}%{_datadir}/%{name}/resources/themes/cura/fonts/
#ln -s %{_datadir}/fonts/open-sans/ %{buildroot}%{_datadir}/%{name}/resources/themes/cura/fonts

%find_lang %{name} --all-name

%check
# desktop file
desktop-file-validate %{buildroot}%{_datadir}/applications/%{lname}.desktop

