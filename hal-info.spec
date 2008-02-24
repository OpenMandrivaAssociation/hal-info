%define name hal-info
%define version 0.0
%define distversion 20071212
%define release %mkrel 5.%distversion.2

Summary: Device information for HAL
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://hal.freedesktop.org/releases/%{name}-%{distversion}.tar.gz
Source1: 10-camera-storage.fdi
Source2: hal-setup-keymap-keys.txt
# (fc) update to latest git (git diff HAL_INFO_snapshot..master)
#Patch0: now patch now
# (fc) 0.0-4.20070425.1mdv re-add untested quirks (git diff master..mandriva
Patch1: hal-info-20071212-untestedquirks.patch
# (fc) 0.0-5.20070725.1mdv enable intel X.org driver v1.0 specific quirks (only for Mdv 2007.1) (git diff mandriva..mdv2007.1)
Patch2: hal-info-20070725-intelquirks.patch
# (fc) 0.0-5.20070725.2mdv add patches pending merge (git diff master..pending)
#Patch3: no patch now
# (fc) 0.0-5.20070925.5mdv add keymap for ACER 9300 (Mdv bug #32989)
Patch5: hal-info-20071212-acer9300-keymap.patch
# (fc) 0.0-5.20071011.5mdv fix keymap check
Patch6: hal-info-20071011-fixkeymapcheck.patch
# (cg) 0.0.5.20071212.2mdv Suspend fix for Dell Inspiron 6400 (aka MM061) (mdv#29448, fdo#14067)
Patch7: hal-info-20071212-dell-mm061-suspend.patch

License: GPL
Group: System/Kernel and hardware
Url: http://www.freedesktop.org/Software/hal
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch: noarch
Conflicts: hal < 0.5.8.1-10mdv2007.1
%if %mdkversion >= 200800
BuildRequires: hal-devel >= 0.5.10
%else
BuildRequires: hal-devel 
%endif
#needed for make check
BuildRequires: libxml2-utils

%description
hal-info contains device information for HAL.

%prep
%setup -q -n %{name}-%{distversion}
#%patch0 -p1 -b .git
%patch1 -p1 -b .untestedquirks
%if %mdkversion < 200800
%patch2 -p1 -b .intelquirks
%endif
#%patch3 -p1 -b .pending
%patch5 -p1 -b .acer9300-keymap
%patch6 -p1 -b .fixkeymapcheck
%patch7 -p0 -b .dell-mm061-suspend

#install missing file
cp %{SOURCE2} tools/

%build

%configure2_5x
%make

%install
rm -rf %{buildroot}
%makeinstall_std
install %{SOURCE1} %{buildroot}%{_datadir}/hal/fdi/information/10freedesktop/10-camera-storage.fdi

cat << EOF > $RPM_BUILD_ROOT%{_datadir}/hal/fdi/preprobe/10osvendor/10-usb-disable-mediacheck.fdi
<?xml version="1.0" encoding="ISO-8859-1"?> <!-- -*- SGML -*- -->

<deviceinfo version="0.2">
  <device>
    <match key="storage.bus" string="usb">
      <match key="@storage.physical_device:usb.vendor_id" int="0x67b">
        <match key="@storage.physical_device:usb.product_id" int="0x2317">
          <merge key="storage.media_detection_enabled" type="bool">false</merge>
        </match>
      </match>
      <match key="@storage.physical_device:usb.vendor_id" int="0x054c">
        <match key="@storage.physical_device:usb.product_id" int="0x008b">
          <merge key="storage.media_detection_enabled" type="bool">false</merge>
        </match>
      </match>
    </match>
  </device>
</deviceinfo>
EOF

%check
make check

%clean
rm -rf %{buildroot}

%postun
if [ "$1" = "1" -a -r /etc/init.d/haldaemon ]; then 
 service haldaemon condrestart > /dev/null 2>/dev/null
fi

%files
%defattr(-,root,root)
%doc AUTHORS NEWS README
%{_datadir}/hal/fdi/information
%{_datadir}/hal/fdi/preprobe


