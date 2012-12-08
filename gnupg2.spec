%define	pkgname	gnupg

%define build_gpgagentscript	0
%{?_without_gpgagentscript:	%global build_gpgagentscript 0}
%{?_with_gpgagentscript:	%global build_gpgagentscript 1}

Summary:	GNU privacy guard - a free PGP replacement
Name:		gnupg2
Version:	2.0.18
Release:	3
License:	GPLv3
Group:		File tools
URL:		http://www.gnupg.org
Source0:	ftp://ftp.gnupg.org/gcrypt/gnupg/%{pkgname}-%{version}.tar.bz2
Source1:	%{SOURCE0}.sig
Source2:	gpg-agent.sh
Source3:	gpg-agent-xinit.sh
Source4:	sysconfig-gnupg2
Patch0:		gnupg-1.9.3-use-ImageMagick-for-photo.patch
Patch1:		gnupg-2.0.14-tests-s2kcount.patch
BuildRequires:	openldap-devel
BuildRequires:	sendmail-command
BuildRequires:	libgpg-error-devel >= 1.4
BuildRequires:	libgcrypt-devel >= 1.2.0
BuildRequires:	libassuan-devel >= 1.0.2
BuildRequires:	libksba-devel >= 1.0.2
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pth-devel >= 2.0.0
BuildRequires:	docbook-utils
BuildRequires:	readline-devel
BuildRequires:	termcap-devel
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libusb)
BuildRequires:	bzip2-devel
BuildRequires:	libassuan-devel
Obsoletes:	newpg
Provides:	newpg = %{version}-%{release}
Requires:	dirmngr
Requires:	pinentry
Requires:	gnupg

%description
GnuPG is GNU's tool for secure communication and data storage.
It can be used to encrypt data and to create digital signatures.
It includes an advanced key management facility and is compliant
with the proposed OpenPGP Internet standard as described in RFC2440.

%prep
%setup -q -n %{pkgname}-%{version}
%patch0 -p1 -b .ImageMagick
%patch1 -p1

%build
%serverbuild

./autogen.sh

%configure2_5x \
	--libexecdir=%{_libdir}/gnupg2 \
	--enable-symcryptrun \
	--disable-rpath \
	--without-capabilities \
	--with-adns=no \
	--with-pkits-tests

# no parallel make (v2.0.5 at least)
%make

# all tests must pass on i586 and x86_64
%check
[[ -n "$GPG_AGENT_INFO" ]] || eval `./agent/gpg-agent --use-standard-socket --daemon --write-env-file gpg-agent-info`
make check
[[ -a gpg-agent-info ]] && kill -0 `cut -d: -f 2 gpg-agent-info`
rm -f gpg-agent-info

%install
%makeinstall_std
#Remove: #60298
%if %{build_gpgagentscript}
install -d %{buildroot}/%{_sysconfdir}/profile.d
install %{SOURCE2} %{buildroot}/%{_sysconfdir}/profile.d/gpg-agent.sh
install -d %{buildroot}/%{_sysconfdir}/X11/xinit.d
install %{SOURCE3} %{buildroot}/%{_sysconfdir}/X11/xinit.d/gpg-agent
install -d %{buildroot}/%{_sysconfdir}/sysconfig
install %{SOURCE4} %{buildroot}/%{_sysconfdir}/sysconfig/%{name}
%endif
# remove this from package because the content of options.skel is the
# identical for both gnupg 1/2, except for comment
rm -rf %{buildroot}%{_datadir}/gnupg

rm -rf %{buildroot}%{_docdir}/gnupg

# fix file conflict with 'gnupg' package
rm %{buildroot}%{_mandir}/man1/gpg-zip.1

%find_lang %{name}

%files -f %{name}.lang
%defattr(-,root,root)
%doc README NEWS THANKS TODO ChangeLog
%doc doc/FAQ doc/HACKING doc/KEYSERVER doc/OpenPGP doc/TRANSLATE doc/DETAILS 
%doc doc/examples
%if %{build_gpgagentscript}
%attr(0755,root,root) %{_sysconfdir}/profile.d/gpg-agent.sh
%attr(0755,root,root) %{_sysconfdir}/X11/xinit.d/gpg-agent
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%endif
%attr(4755,root,root) %{_bindir}/gpgsm
%{_bindir}/gpg-agent
%{_bindir}/gpgconf
%{_bindir}/kbxutil
%{_bindir}/sc*
%{_bindir}/watchgnupg
%{_bindir}/gpgsm-gencert.sh
%{_bindir}/gpgkey2ssh
%{_bindir}/gpg-connect-agent
%{_bindir}/gpgparsemail
%{_bindir}/gpg2
%{_bindir}/gpgv2
%{_bindir}/symcryptrun
%{_sbindir}/addgnupghome
%{_sbindir}/applygnupgdefaults
%dir %{_libdir}/gnupg2
%{_libdir}/gnupg2/gpg-check-pattern
%{_libdir}/gnupg2/gpg-preset-passphrase
%{_libdir}/gnupg2/gpg-protect-tool
%{_libdir}/gnupg2/gnupg-pcsc-wrapper
%{_libdir}/gnupg2/gpg2keys_curl
%{_libdir}/gnupg2/gpg2keys_finger
%{_libdir}/gnupg2/gpg2keys_hkp
%{_libdir}/gnupg2/gpg2keys_ldap
%{_infodir}/gnupg.info*
%{_mandir}/man1/gpg-agent.1*
%{_mandir}/man1/gpg-connect-agent.1*
%{_mandir}/man1/gpg-preset-passphrase.1*
%{_mandir}/man1/gpg2.1*
%{_mandir}/man1/gpgconf.1*
%{_mandir}/man1/gpgparsemail.1*
%{_mandir}/man1/gpgsm-gencert.sh.1*
%{_mandir}/man1/gpgsm.1*
%{_mandir}/man1/gpgv2.1*
%{_mandir}/man1/scdaemon.1*
%{_mandir}/man1/symcryptrun.1*
%{_mandir}/man1/watchgnupg.1*
%{_mandir}/man8/addgnupghome.8*
%{_mandir}/man8/applygnupgdefaults.8*


%changelog
* Thu Aug 04 2011 Lonyai Gergely <aleph@mandriva.org> 2.0.18-1mdv2011.0
+ Revision: 693256
- 2.0.18

* Wed Jun 08 2011 Lonyai Gergely <aleph@mandriva.org> 2.0.17-3
+ Revision: 683217
- Test the gpg-agent without script
- Temporary drop the gpg-agent scripts

* Tue May 03 2011 Oden Eriksson <oeriksson@mandriva.com> 2.0.17-2
+ Revision: 664905
- mass rebuild

* Thu Jan 13 2011 Lonyai Gergely <aleph@mandriva.org> 2.0.17-1
+ Revision: 631011
- 2.0.17
  Remove the applied patch

* Wed Jan 05 2011 Oden Eriksson <oeriksson@mandriva.com> 2.0.16-6mdv2011.0
+ Revision: 628718
- gpg2keys_kdns requires adns
- disable adns support because adns does not have ipv6 support and to mitigate CVE-2008-4100

* Wed Dec 29 2010 Per Ã˜yvind Karlsen <peroyvind@mandriva.org> 2.0.16-5mdv2011.0
+ Revision: 625749
- fix man page file conflict

* Thu Sep 09 2010 Lonyai Gergely <aleph@mandriva.org> 2.0.16-4mdv2011.0
+ Revision: 576917
- Add more condition the gpg-agent running

* Mon Aug 30 2010 Lonyai Gergely <aleph@mandriva.org> 2.0.16-3mdv2011.0
+ Revision: 574346
- Fix missing %%files
- CCBUG: 60298
  Fix: #60298 -  gpg-agent does not shut down properly

* Fri Aug 06 2010 Lonyai Gergely <aleph@mandriva.org> 2.0.16-2mdv2011.0
+ Revision: 566609
- The gpg-agent does not start now by /etc/profile.d/
  CCBUG: #60298
- CCBUG: #60298
  CCBUG: #60297
- 2.0.16
- Fix a gpgsm security bug
- #59727 - gpg-agent not started, email signing/encryption not working

* Sun Jul 11 2010 Lonyai Gergely <aleph@mandriva.org> 2.0.15-12mdv2011.0
+ Revision: 550605
- #59727 - gpg-agent not started, email signing/encryption not working

* Fri May 14 2010 Lonyai Gergely <aleph@mandriva.org> 2.0.15-11mdv2010.1
+ Revision: 544835
- REOPENED #58992 ksh syntax error in gpg-agent.sh

* Thu Apr 29 2010 Lonyai Gergely <aleph@mandriva.org> 2.0.15-10mdv2010.1
+ Revision: 541032
- Fix #58992  -  profile shell script uses the "source" statement

* Thu Apr 22 2010 Lonyai Gergely <aleph@mandriva.org> 2.0.15-9mdv2010.1
+ Revision: 537805
- Fixing to stop the gpg-agent in the %%check
- The check of gnupg2 doesn't work without the gpg-agent. Now the agent start previous check, and stop after it

* Sun Apr 18 2010 GÃ¶tz Waschk <waschk@mandriva.org> 2.0.15-8mdv2010.1
+ Revision: 536314
- fix gpg-agent (bug #58815)

* Sat Apr 17 2010 Lonyai Gergely <aleph@mandriva.org> 2.0.15-6mdv2010.1
+ Revision: 535806
- Fix: #58802 - "exit 0" statement gpg-agent.sh causes su -l postgres to exit prematurely

* Thu Apr 15 2010 Lonyai Gergely <aleph@mandriva.org> 2.0.15-5mdv2010.1
+ Revision: 535023
- Add a UID condition to gpg-agent.sh: (#57312/8: start the gpg-agent with firebird)
- remove the dead $HOME/.gnupg/gpg-agent-info in script

* Wed Mar 17 2010 Lonyai Gergely <aleph@mandriva.org> 2.0.15-4mdv2010.1
+ Revision: 523746
- bug #58207 - broken /etc/profile.d/gpg-agent.sh

* Tue Mar 16 2010 Oden Eriksson <oeriksson@mandriva.com> 2.0.15-3mdv2010.1
+ Revision: 520752
- P1: fix build in a chroot (fedora)
- rebuild

  + Lonyai Gergely <aleph@mandriva.org>
    - 2.0.15
      Fix: #57312 - gnupg2 detects gpg-agent presence in a manner incompatible with keychain

  + Tomasz Pawel Gajc <tpg@mandriva.org>
    - add buildrequires on libassuan-devel

  + Frederik Himpe <fhimpe@mandriva.org>
    - Update to new version 2.0.14

* Mon Sep 07 2009 Lonyai Gergely <aleph@mandriva.org> 2.0.13-1mdv2010.0
+ Revision: 432508
- update to 2.0.13

* Wed Sep 02 2009 Lonyai Gergely <aleph@mandriva.org> 2.0.12-3mdv2010.0
+ Revision: 424361
- fix #53355

* Tue Sep 01 2009 Lonyai Gergely <aleph@mandriva.org> 2.0.12-2mdv2010.0
+ Revision: 423493
- add profile.d and X11/xinit.d scripts (Resolv: #53196)

* Wed Jun 17 2009 Lonyai Gergely <aleph@mandriva.org> 2.0.12-1mdv2010.0
+ Revision: 386578
- update to 2.0.12

* Wed Mar 04 2009 Frederik Himpe <fhimpe@mandriva.org> 2.0.11-1mdv2009.1
+ Revision: 348510
- Update to new version 2.0.11
- Include kdns support

* Wed Feb 25 2009 Oden Eriksson <oeriksson@mandriva.com> 2.0.10-2mdv2009.1
+ Revision: 344702
- rebuilt against new readline

* Tue Jan 20 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 2.0.10-1mdv2009.1
+ Revision: 331498
- patch 2 is not needed anymore
- fix file list
- add more docs
- update to new version 2.0.10

* Sun Jan 04 2009 Oden Eriksson <oeriksson@mandriva.com> 2.0.9-5mdv2009.1
+ Revision: 324382
- disable capabilities, seems unsupported by the build system

* Tue Dec 30 2008 Oden Eriksson <oeriksson@mandriva.com> 2.0.9-4mdv2009.1
+ Revision: 321399
- drop the CVE-2006-3082 patch, allready in there... (caught by --fuzz=0)
- fix deps (cap-devel)

* Tue Jul 22 2008 Oden Eriksson <oeriksson@mandriva.com> 2.0.9-3mdv2009.0
+ Revision: 240835
- fix deps

* Wed May 21 2008 Oden Eriksson <oeriksson@mandriva.com> 2.0.9-2mdv2009.0
+ Revision: 209747
- added one gcc43 patch (debian)

* Thu Mar 27 2008 Oden Eriksson <oeriksson@mandriva.com> 2.0.9-1mdv2008.1
+ Revision: 190623
- 2.0.9 (fixes #39429 (vulns in gnupg 1.4.8 and gnupg2 2.0.8))

* Sun Dec 30 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 2.0.8-1mdv2008.1
+ Revision: 139652
- new version
- do not package COPYING file
- add missing buildrequires on libtermcap-devel, libcurl-devel, bzip2-devel and libusb-devel(this one enables smartcard reader driver)

* Mon Dec 24 2007 Oden Eriksson <oeriksson@mandriva.com> 2.0.7-4mdv2008.1
+ Revision: 137468
- rebuilt against openldap-2.4.7 libs

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sat Dec 15 2007 Emmanuel Andry <eandry@mandriva.org> 2.0.7-3mdv2008.1
+ Revision: 120446
- rebuild for assuan

* Fri Oct 19 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 2.0.7-1mdv2008.1
+ Revision: 100336
- new version
- drop patch 2 (fixed upstream)
- enable parallel build
- add %%check
- enable symcryptrun
- use linux capabilities
- enable additional tests

* Thu Aug 23 2007 Thierry Vignaud <tv@mandriva.org> 2.0.5-3mdv2008.0
+ Revision: 69906
- info file must be unregistered before being uninstalled
- kill file require on info-install

* Mon Jul 09 2007 Andreas Hasenack <andreas@mandriva.com> 2.0.5-2mdv2008.0
+ Revision: 50544
- added patch from Gentoo to fix a problem discovered by make test in x86_64
- updated to version 2.0.5
- adjusted buildrequires (libksba and libassuan)
- no parallel make, doesn't work
- updated license tag to GPLv3

* Wed Jun 27 2007 Andreas Hasenack <andreas@mandriva.com> 2.0.4-2mdv2008.0
+ Revision: 45092
- rebuild with new serverbuild macro (-fstack-protector-all)

* Wed May 09 2007 Andreas Hasenack <andreas@mandriva.com> 2.0.4-1mdv2008.0
+ Revision: 25663
- updated to version 2.0.4


* Thu Mar 08 2007 Andreas Hasenack <andreas@mandriva.com> 2.0.3-1mdv2007.1
+ Revision: 138365
- updated to version 2.0.3
- updated to version 2.0.2
- removed security patch that was already applied

* Tue Jan 02 2007 Andreas Hasenack <andreas@mandriva.com> 2.0.1-2mdv2007.1
+ Revision: 103133
- added security patch for CVE-2006-6235

* Wed Nov 29 2006 Andreas Hasenack <andreas@mandriva.com> 2.0.1-1mdv2007.1
+ Revision: 88675
- adjusted some buildrequires
- enabled full gnupg2 build
- updated to version 2.0.1
- dropped bug728 patch, already fixed
- fix overflow (upstream bug 728)
- commit update to version 2.0.0
- still need to update other libraries

* Thu Aug 31 2006 Andreas Hasenack <andreas@mandriva.com> 1.9.22-2mdv2007.0
+ Revision: 58916
- re-enable test on x86_64, it's working now (#20078)
- updated to version 1.9.22, fixing CVE-2006-3746
- Import gnupg2

* Thu Jun 22 2006 Oden Eriksson <oeriksson@mandriva.com> 1.9.20-3mdv2007.0
- added a security fix for CVE-2006-3082 (P2)

* Fri Jan 20 2006 Andreas Hasenack <andreas@mandriva.com> 1.9.20-2mdk
- skipping make check on x86_64, see:
  http://qa.mandriva.com/show_bug.cgi?id=20078

* Mon Jan 09 2006 Andreas Hasenack <andreas@mandriva.com> 1.9.20-1mdk
- updated to version 1.9.20
- added new binary (gpgparsemail)
- Prereq -> Requires(foo)

* Fri Dec 02 2005 Andreas Hasenack <andreas@mandriva.com> 1.9.19-1mdk
- updated to version 1.9.19
- removed 64bit fixes patch, already applied
- added new binary, gpgkey2ssh
- added docbook-utils buildrequires
- added docbookfix patch to fix detection of some docbook utilities

* Tue Sep 06 2005 Gwenole Beauchesne <gbeauchesne@mandriva.com> 1.9.16-4mdk
- 64-bit fixes

* Sat Jul 23 2005 Nicolas Lécureuil <neoclust@mandriva.org> 1.9.16-3mdk
- Rebuild
- Fix smtpdaemon
- mkrel

* Wed Jun 15 2005 Guillaume Rousse <guillomovitch@mandriva.org> 1.9.16-2mdk 
- buildrequires libassuan-devel >= 0.6.9

* Thu May 19 2005 Arnaud de Lorbeau <devel@mandriva.com> 1.9.16-1mdk
- 1.9.16

* Fri Aug 20 2004 Abel Cheung <deaddog@deaddog.org> 1.9.10-1mdk
- New version
- Remove P1 (upstream)

* Fri May 21 2004 Abel Cheung <deaddog@deaddog.org> 1.9.8-1mdk
- New version
- Use tarball instead, signed upstream
- Requires new libpth
- Patch1: Fix typo which prevents compilation

* Fri May 07 2004 Olivier Blin <blino@mandrake.org> 1.9.3-3mdk
- buildrequires
- rebuild for new libgcrypt

