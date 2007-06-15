%define name	timeconfig
%define version	3.2
%define release	%mkrel 11

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	Text mode tools for setting system time parameters.
License:	GPL
Group:		System/Configuration/Other
Source0:	%{name}-%{version}.tar.bz2
Source5:	timeconfig.pamd
Source6:	timeconfig.apps
Requires:	initscripts
Requires:	usermode-consoleonly
BuildRequires:	gettext newt-devel popt-devel slang-devel
Patch0:		timeconfig-gmt.patch.bz2
Patch1:		timeconfig-mdkconf.patch.bz2
Requires(post):		fileutils, gawk
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

%files -f %{name}.lang
%defattr(-,root,root)
%{_sbindir}/*
%{_mandir}/man*/*
%config(noreplace) %{_sysconfdir}/pam.d/timeconfig-auth
%config(noreplace) %{_sysconfdir}/security/console.apps/timeconfig-auth
