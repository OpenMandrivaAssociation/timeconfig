Summary:	Text mode tools for setting system time parameters
Name:		timeconfig
Version:	3.2
Release:	%mkrel 20
License:	GPL
Group:		System/Configuration/Other
Source0:	%{name}-%{version}.tar.bz2
Source5:	timeconfig.pamd
Source6:	timeconfig.apps
Patch0:		timeconfig-gmt.patch
Patch1:		timeconfig-mdkconf.patch
Patch2:		timeconfig-3.2-format_not_a_string_literal_and_no_format_arguments.diff
Patch3:		timeconfig-3.2-LDFLAGS.diff
Requires:	initscripts
Requires:	usermode-consoleonly
BuildRequires:	gettext
BuildRequires:	newt-devel
BuildRequires:	popt-devel
BuildRequires:	slang-devel
Requires(post): coreutils, gawk
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
%patch2 -p0 -b .format_not_a_string_literal_and_no_format_arguments
%patch3 -p0 -b .LDFLAGS

%build
make RPM_OPT_FLAGS="%{optflags}" LDFLAGS="%{ldflags}"

%install
rm -rf %{buildroot}

make PREFIX=%{buildroot}%{_prefix} install
rm -f %{buildroot}/usr/lib/zoneinfo

# fix indonesian locale, its language code is 'id' not 'in'.
mkdir -p %{buildroot}%{_datadir}/locale/id/LC_MESSAGES

# (fg) 20001004 In replacement of kdesu...
mkdir -p %{buildroot}/%{_sysconfdir}/{pam.d,security/console.apps}

install -m644 %{SOURCE5} %{buildroot}/%{_sysconfdir}/pam.d/timeconfig
install -m644 %{SOURCE6} %{buildroot}/%{_sysconfdir}/security/console.apps/timeconfig

mkdir -p %{buildroot}%{_bindir}
ln -fs %{_bindir}/consolehelper %{buildroot}/%{_bindir}/timeconfig

# remove unpackaged files
rm -rf %{buildroot}%{_mandir}/pt_BR/

%{find_lang} %{name}

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

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%{_sbindir}/*
%{_bindir}/*
%{_mandir}/man*/*
%config(noreplace) %{_sysconfdir}/pam.d/timeconfig
%config(noreplace) %{_sysconfdir}/security/console.apps/timeconfig
