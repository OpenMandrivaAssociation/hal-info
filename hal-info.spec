%define name hal-info
%define version 0.0
%define distversion 20091130
%define release %mkrel 5.%distversion.5

%define git_url git://git.freedesktop.org/git/hal-info

Summary: Device information for HAL
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://hal.freedesktop.org/releases/%{name}-%{distversion}.tar.bz2
Source1: 10-camera-storage.fdi
# (fc) update to latest git (git diff HAL_INFO_snapshot..master)
#Patch0: now patch now
# (fc) 0.0-4.20070425.1mdv re-add untested quirks (git diff master..mandriva
Patch1: hal-info-20090716-untestedquirks.patch
# (fc) 0.0-5.20070725.2mdv add patches pending merge (git diff master..pending)
#Patch3: no patch now

License: AFL or GPLv2
Group: System/Kernel and hardware
Url: https://www.freedesktop.org/Software/hal
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




%changelog
* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 0.0-5.20091130.3mdv2011.0
+ Revision: 665401
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 0.0-5.20091130.2mdv2011.0
+ Revision: 605843
- rebuild

* Mon Jan 04 2010 Emmanuel Andry <eandry@mandriva.org> 0.0-5.20091130.1mdv2010.1
+ Revision: 486277
- Release 20091130

* Mon Jul 27 2009 Frederic Crozat <fcrozat@mandriva.com> 0.0-5.20090716.1mdv2010.0
+ Revision: 400546
- Release 20090716
- Update patch1

* Wed Apr 15 2009 Frederic Crozat <fcrozat@mandriva.com> 0.0-5.20090414.1mdv2009.1
+ Revision: 367371
- Release 20090414

* Tue Mar 31 2009 Frederic Crozat <fcrozat@mandriva.com> 0.0-5.20090330.1mdv2009.1
+ Revision: 362864
- Release 20030330

* Mon Mar 09 2009 Frederic Crozat <fcrozat@mandriva.com> 0.0-5.20090309.1mdv2009.1
+ Revision: 353200
- Release 200900309
- Remove patches 8 & 9 (merged upstream)
- Regenerate patch1, partially merged upstream

* Tue Feb 03 2009 Frederic Crozat <fcrozat@mandriva.com> 0.0-5.20090202.1mdv2009.1
+ Revision: 336977
- Release 20090202
- Add git_url
- Regenerate patches 1, 8, 9
- Remove patches 7, 13 (merged upstream)

* Wed Dec 17 2008 Frederic Crozat <fcrozat@mandriva.com> 0.0-5.20081127.1mdv2009.1
+ Revision: 315193
- Release 20081127
- Remove patches 11, 12 (merged upstream)
- Regenerate patch1

* Wed Oct 01 2008 Frederic Crozat <fcrozat@mandriva.com> 0.0-5.20081001.1mdv2009.0
+ Revision: 290445
- Release 20081001
- Patch13: add requires_eject for N82

* Mon Sep 29 2008 Frederic Crozat <fcrozat@mandriva.com> 0.0-5.20080929.1mdv2009.0
+ Revision: 289705
- Snapshot 20090929
- Remove patch2, obsolete
- Regenerate patch1 (partially merged)
- Remove patch5 (no longer needed)
- Remvoe patch12 (merged upstream)
- Patch12: fix check which doesn't pass with latest sony keymap file
- Patch12:  blacklist CD drive of the Huawei E220 USB HSDPA modem (GIT)

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild early 2009.0 package (before pixel changes)

* Wed Aug 06 2008 Frederic Crozat <fcrozat@mandriva.com> 0.0-5.20080508.1mdv2009.0
+ Revision: 264318
- Release 20080508
- Remove patches 6 & 10 (merged usptream)
- Regenerate patches 1 (partially merged upstream), 9

  + Pascal Terjan <pterjan@mandriva.org>
    - Add suspend quirk for Airis machine

* Wed May 14 2008 Frederic Crozat <fcrozat@mandriva.com> 0.0-5.20080317.4mdv2009.0
+ Revision: 207200
- Patch9: fix suspend quirk for EEEPC 900 (Mdv bug #40578)
- Patch10 (GIT) fix delete key not responsive on Acer Extensa 5220 (Mdv bug #37570)

* Tue Apr 01 2008 Frederic Crozat <fcrozat@mandriva.com> 0.0-5.20080317.3mdv2008.1
+ Revision: 191368
- Patch8: disable multimedia keymaps for Asus laptops, not needed with Mandriva kernels (Mdv bug #39669)

* Tue Mar 25 2008 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 0.0-5.20080317.2mdv2008.1
+ Revision: 190074
- Added video quirk for Clevo M720SR (needed when using video driver
  provided by sis).

* Tue Mar 18 2008 Frederic Crozat <fcrozat@mandriva.com> 0.0-5.20080317.1mdv2008.1
+ Revision: 188487
- Release 20080317
- Remove patch7, merged upstream
- Patch6: ad keymap for HP nx9420 (Mdv bug #37817)

* Fri Mar 14 2008 Frederic Crozat <fcrozat@mandriva.com> 0.0-5.20080313.1mdv2008.1
+ Revision: 187808
- Snapshot 20080313
- Remove source2, no longer needed
- regenerate patch1 (partially merged)

* Fri Feb 29 2008 Frederic Crozat <fcrozat@mandriva.com> 0.0-5.20080215.1mdv2008.1
+ Revision: 176839
- Release 20080215
- Remove patch6, merged upstream

* Sun Feb 24 2008 Colin Guthrie <cguthrie@mandriva.org> 0.0-5.20071212.2mdv2008.1
+ Revision: 174347
- Suspend fix for Dell Inspiron 6400 (aka MM061) (mdv#29448, fdo#14067)

* Wed Jan 09 2008 Frederic Crozat <fcrozat@mandriva.com> 0.0-5.20071212.1mdv2008.1
+ Revision: 147267
- Release 20071212
- Regenerate patches 1 and 5
- Remove patch4, no longer needed

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Mon Dec 17 2007 Thierry Vignaud <tv@mandriva.org> 0.0-5.20071011.1mdv2008.1
+ Revision: 126585
- kill re-definition of %%buildroot on Pixel's request

* Fri Oct 12 2007 Frederic Crozat <fcrozat@mandriva.com> 0.0-5.20071011.1mdv2008.0
+ Revision: 97760
- Release 20071011
- Update patch4, partially merged
- Patch6: fix validation test to discard commented lines

* Fri Sep 28 2007 Frederic Crozat <fcrozat@mandriva.com> 0.0-5.20070925.1mdv2008.0
+ Revision: 93544
- Release 20070925
- Patch4: add fixes from hal mailing-list
- Patch5: add keymap for Acer Aspire 9300 (Mdv bug #32989)

* Mon Sep 03 2007 Frederic Crozat <fcrozat@mandriva.com> 0.0-5.20070831.1mdv2008.0
+ Revision: 78600
- Release 20070831
- Regenerate patch1
- Remove patches 0 & 3 (empty for now)

* Thu Aug 23 2007 Frederic Crozat <fcrozat@mandriva.com> 0.0-5.20070725.4mdv2008.0
+ Revision: 70234
- Rebuild with hal 0.5.10 to get keymap and killswitch related fdi files

* Wed Aug 22 2007 Frederic Crozat <fcrozat@mandriva.com> 0.0-5.20070725.3mdv2008.0
+ Revision: 69024
- Update patches 0, 1, 2, 3 with latest git snapshot : add more laptops quirks and fix Mdv bug #32743)
- add make check to ensure we don't ship unoticed broken fdi files in the future
- add hal internal keymap list to get make check running

* Thu Aug 09 2007 Frederic Crozat <fcrozat@mandriva.com> 0.0-5.20070725.2mdv2008.0
+ Revision: 60844
- Patch3: add quirks pending merge

* Wed Aug 08 2007 Frederic Crozat <fcrozat@mandriva.com> 0.0-5.20070725.1mdv2008.0
+ Revision: 60450
- Release 20070725
- Regenerate patch1, part was merged upstream
- Patch0: update to latest git changes
- Patch2: enable quirks for intel xorg driver 1.x (only when building for Mandriva 2007.1)

* Mon Jun 25 2007 Olivier Blin <oblin@mandriva.com> 0.0-5.20070425.1mdv2008.0
+ Revision: 44113
- add quirks for Elonex M5A (from Arnaud Patard)

* Thu May 10 2007 Frederic Crozat <fcrozat@mandriva.com> 0.0-4.20070425.1mdv2008.0
+ Revision: 26113
- new release (20070425)
- Remove all patches, merged in either patch 0 or 1
- Patch0: update to latest GIT snapshot (20070510)
- Patch1: re-add untested quirks removed from upstream and add
 tested quirks (T42/2668, nc4200, nc6120), pending merge


* Tue Mar 27 2007 Frederic Crozat <fcrozat@mandriva.com> 0.0-4.20070326.2mdv2007.1
+ Revision: 149001
- Patch5: disable vbestate_restore when not needed
- Patch6: remove duplicated entries
- Restart haldaemon if running after package upgrade is finished

* Tue Mar 27 2007 Frederic Crozat <fcrozat@mandriva.com> 0.0-4.20070326.1mdv2007.1
+ Revision: 148861
- Updated snapshot (20070326)
- Remove patch3, merged upstream

* Fri Mar 09 2007 Olivier Blin <oblin@mandriva.com> 0.0-4.20070302.3mdv2007.1
+ Revision: 138615
- use vbe_post quirk on Maxdata Pro 6100X (to fix ghost cursor after resume from S3)

* Tue Mar 06 2007 Frederic Crozat <fcrozat@mandriva.com> 0.0-4.20070302.2mdv2007.1
+ Revision: 133959
- Add missing directories in package

* Fri Mar 02 2007 Frederic Crozat <fcrozat@mandriva.com> 0.0-4.20070302.1mdv2007.1
+ Revision: 131583
-New git snapshot (20070302)
-Patch3 : fix vbe_save key to correct one
-add usb-disable-media-check fdi from hal package
-regenerate patches 0 and 1
-package preprobe information fdi

* Wed Jan 17 2007 Olivier Blin <oblin@mandriva.com> 0.0-4mdv2007.1
+ Revision: 110044
- move camera storage information file in its own source
- add Z61m video quirks (settings from Frederic Crozat)
- add D420 video quirks (settings from Arnaud Patard)

* Tue Jan 09 2007 Olivier Blin <oblin@mandriva.com> 0.0-3mdv2007.1
+ Revision: 106352
- fix hal conflicts version

* Mon Jan 08 2007 Olivier Blin <oblin@mandriva.com> 0.0-2mdv2007.1
+ Revision: 106202
- move hal information scripts to hal-info

* Sun Jan 07 2007 Olivier Blin <oblin@mandriva.com> 0.0-1mdv2007.1
+ Revision: 105374
- initial hal-info release
- Create hal-info

