%define name hal-info
%define version 0.0
%define distversion 20070326
%define release %mkrel 4.%distversion.2

Summary: Device information for HAL
Name: %{name}
Version: %{version}
Release: %{release}
# generated with "make dist" from from git://anongit.freedesktop.org/git/hal-info
Source0: %{name}-%{distversion}.tar.bz2
Source1: 10-camera-storage.fdi
# (fc) 0.5.7.1-6mdv add another nonname card reader
Patch0: hal-0.5.7.1-usbcardreader.patch
Patch1: hal-info-d420.patch
Patch2: hal-info-z61m.patch
Patch4: hal-info-max6100.patch
Patch5: hal-info-vbestate.patch
# (fc) remove duplicated entries
Patch6: hal-info-20070326-duplicate.patch
License: GPL
Group: System/Kernel and hardware
Url: http://www.freedesktop.org/Software/hal
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch: noarch
Conflicts: hal < 0.5.8.1-10mdv2007.1

%description
hal-info contains device information for HAL.

%prep
%setup -q -n %{name}-%{distversion}
%patch0 -p1 -b .usbcardreader
%patch1 -p1 -b .d420
%patch2 -p1 -b .z61m
%patch4 -p1 -b .max6100
%patch5 -p1 -b .vbestate
%patch6 -p1 -b .duplicate

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
%dir %{_sysconfdir}/hal/fdi/*
%{_datadir}/hal/fdi/information
%{_datadir}/hal/fdi/preprobe


