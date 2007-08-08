%define name hal-info
%define version 0.0
%define distversion 20070725
%define release %mkrel 5.%distversion.1

Summary: Device information for HAL
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://hal.freedesktop.org/releases/%{name}-%{distversion}.tar.gz
Source1: 10-camera-storage.fdi
# (fc) update to latest git
Patch0: hal-info-20070725-git.patch
# (fc) 0.0-4.20070425.1mdv re-add untested quirks
Patch1: hal-info-20070725-untestedquirks.patch
# (fc) 0.0-5.20070725.1mdv enable intel X.org driver v1.0 specific quirks (only for Mdv 2007.1)
Patch2: hal-info-20070725-intelquirks.patch
License: GPL
Group: System/Kernel and hardware
Url: http://www.freedesktop.org/Software/hal
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch: noarch
Conflicts: hal < 0.5.8.1-10mdv2007.1
BuildRequires: hal-devel

%description
hal-info contains device information for HAL.

%prep
%setup -q -n %{name}-%{distversion}
%patch0 -p1 -b .git
%patch1 -p1 -b .untestedquirks
%if %mdkversion < 200800
%patch2 -p1 -b .intelquirks
%endif

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


