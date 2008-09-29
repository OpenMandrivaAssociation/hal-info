%define name hal-info
%define version 0.0
%define distversion 20080929
%define release %mkrel 5.%distversion.1

Summary: Device information for HAL
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://hal.freedesktop.org/releases/%{name}-%{distversion}.tar.gz
Source1: 10-camera-storage.fdi
# (fc) update to latest git (git diff HAL_INFO_snapshot..master)
#Patch0: now patch now
# (fc) 0.0-4.20070425.1mdv re-add untested quirks (git diff master..mandriva
Patch1: hal-info-20080929-untestedquirks.patch
# (fc) 0.0-5.20070725.2mdv add patches pending merge (git diff master..pending)
#Patch3: no patch now
# (hk) 0.0-5.20080317.2mdv add video quirk for Clevo M720SR
Patch7: hal-info-20080317-video-clevo-m720sr.patch
# (fc) 0.0-5.20080317.3mdv disable Multimedia keymaps for Asus Laptops, they are not needed with Mandriva kernel (Mdv bug #39669)
Patch8: hal-info-20080317-disableasuskeymap.patch
# (fc) 0.0-5.20080317.4mdv fix suspend quirk for EEE PC 900 (Mdv bug #40578)
Patch9: hal-info-20080508-eeepc900.patch
# (pt) 0.0-5.20080317.5mdv fix resume on AIRIS
Patch11: hal-info-20080317-airis.patch
# (fc) 0.0-5.20080929.1mdv fix check with latest sony keymap
Patch12: hal-info-20080929-fixcheck.patch

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
#%patch3 -p1 -b .pending
%patch7 -p1 -b .video-clevo-m720sr
%patch8 -p1 -b .disableasuskeymap
%patch9 -p1 -b .eeepc900
%patch11 -p1 -b .airis
%patch12 -p1 -b .fixcheck

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


