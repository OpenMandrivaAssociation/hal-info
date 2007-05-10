%define name hal-info
%define version 0.0
%define distversion 20070425
%define release %mkrel 4.%distversion.1

Summary: Device information for HAL
Name: %{name}
Version: %{version}
Release: %{release}
# generated with "make dist" from from git://anongit.freedesktop.org/git/hal-info
Source0: %{name}-%{distversion}.tar.bz2
Source1: 10-camera-storage.fdi
# (fc) 0.0-4.20070425.1mdv update to latest git snapshot (20070510)
Patch0: hal-info-20070425-gitsnapshot20070510.patch
# (fc) 0.0-4.20070425.1mdv re-add untested quirks and some tested ones (T43/2668 + nc4200/nc6120)
Patch1: hal-info-20070425-quirksupdate.patch
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
%patch0 -p1 -b .gitsnapshot
%patch1 -p1 -b .quirksupdate

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


