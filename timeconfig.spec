%define name	timeconfig
%define version	3.2
%define release	10mdk

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	Text mode tools for setting system time parameters.
License:	GPL
Group:		System/Configuration/Other
Source0:	timeconfig-%{version}.tar.bz2
Source1:	timeconfig.menu
Source2:	timeconfig.png
Source3:	timeconfig-mini.png
Source4:	timeconfig-large.png
Source5:	timeconfig.pamd
Source6:	timeconfig.apps
Requires:	initscripts >= 2.81
Requires:	usermode-consoleonly
BuildRequires:	gettext libnewt-devel popt-devel slang-devel
Patch0:		timeconfig-gmt.patch.bz2
Patch1:		timeconfig-mdkconf.patch.bz2
Prereq:		fileutils, gawk
BuildRoot:	%{_tmppath}/%{name}-root

%description
The timeconfig package contains two utilities: timeconfig and
setclock.  Timeconfig provides a simple text mode tool for configuring
the time parameters in /etc/sysconfig/clock and /etc/localtime. The
setclock tool sets the hardware clock on the system to the current
time stored in the system clock.

%prep
%setup -q
%patch0 -p0 -b .gmt
%patch1 -p0 -b .mdkconf

%build
make RPM_OPT_FLAGS="$RPM_OPT_FLAGS"

%install
make PREFIX=$RPM_BUILD_ROOT%{_prefix} install
rm -f $RPM_BUILD_ROOT/usr/lib/zoneinfo

# fix indonesian locale, its language code is 'id' not 'in'.
mkdir -p $RPM_BUILD_ROOT/usr/share/locale/id/LC_MESSAGES


#install menu
mkdir -p $RPM_BUILD_ROOT/%{_menudir}
install -m644 %{SOURCE1} $RPM_BUILD_ROOT/%{_menudir}/timeconfig

# (fg) 20000915 Icons from LN
mkdir -p $RPM_BUILD_ROOT/%{_iconsdir}/{large,mini}

install -m644 %{SOURCE2} $RPM_BUILD_ROOT/%{_iconsdir}
install -m644 %{SOURCE3} $RPM_BUILD_ROOT/%{_miconsdir}/timeconfig.png
install -m644 %{SOURCE4} $RPM_BUILD_ROOT/%{_liconsdir}/timeconfig.png

# (fg) 20001004 In replacement of kdesu...
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/{pam.d,security/console.apps}

install -m644 %{SOURCE5} $RPM_BUILD_ROOT/%{_sysconfdir}/pam.d/timeconfig-auth
install -m644 %{SOURCE6} $RPM_BUILD_ROOT/%{_sysconfdir}/security/console.apps/timeconfig-auth

ln -fs /usr/bin/consolehelper $RPM_BUILD_ROOT/%{_sbindir}/timeconfig-auth

# remove unpackaged files
rm -rf $RPM_BUILD_ROOT%{_mandir}/pt_BR/

%{find_lang} %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -L /etc/localtime ]; then
    _FNAME=`ls -ld /etc/localtime | awk '{ print $11}' | sed 's/lib/share/'`
    rm /etc/localtime
    cp -f $_FNAME /etc/localtime
    if [ -f /etc/sysconfig/clock ]; then
	grep -q "^ZONE=" /etc/sysconfig/clock && \
	echo "ZONE=\"$_FNAME\"" | sed -e "s|.*/zoneinfo/||" >> /etc/sysconfig/clock
    else
	echo "ZONE=\"$_FNAME\"" | sed -e "s|.*/zoneinfo/||" >> /etc/sysconfig/clock
    fi
fi
%{update_menus}

%postun
%{clean_menus}

%files -f %{name}.lang
%defattr(-,root,root)
%{_sbindir}/*
%{_mandir}/man*/*
%{_menudir}/timeconfig
%{_iconsdir}/timeconfig.png
%{_miconsdir}/timeconfig.png
%{_liconsdir}/timeconfig.png
%config(noreplace) %{_sysconfdir}/pam.d/timeconfig-auth
%config(noreplace) %{_sysconfdir}/security/console.apps/timeconfig-auth
