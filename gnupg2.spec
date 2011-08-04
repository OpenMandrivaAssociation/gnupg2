%define	pkgname	gnupg

%define build_gpgagentscript	0
%{?_without_gpgagentscript:	%global build_gpgagentscript 0}
%{?_with_gpgagentscript:	%global build_gpgagentscript 1}

Summary:	GNU privacy guard - a free PGP replacement
Name:		gnupg2
Version:	2.0.18
Release:	%mkrel 1
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
BuildRequires:	automake
BuildRequires:	openldap-devel
BuildRequires:	sendmail-command
BuildRequires:	libgpg-error-devel >= 1.4
BuildRequires:	libgcrypt-devel >= 1.2.0
BuildRequires:	libassuan-devel >= 1.0.2
BuildRequires:	libksba-devel >= 1.0.2
BuildRequires:	zlib-devel
BuildRequires:	pth-devel >= 2.0.0
BuildRequires:	docbook-utils
BuildRequires:	libreadline-devel
BuildRequires:	libtermcap-devel
BuildRequires:	libcurl-devel
BuildRequires:	libusb-devel
BuildRequires:	bzip2-devel
BuildRequires:	libassuan-devel
Requires(post):	info-install
Requires(preun): info-install
Requires:	info-install
Obsoletes:	newpg
Provides:	newpg = %{version}-%{release}
Requires:	dirmngr
Requires:	pinentry
Requires:	gnupg
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
rm -rf %{buildroot}

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

%post
%_install_info gnupg.info

%preun
%_remove_install_info gnupg.info

%clean
rm -rf %{buildroot}

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
