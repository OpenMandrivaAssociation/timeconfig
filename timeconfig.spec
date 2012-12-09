Summary:	Text mode tools for setting system time parameters
Name:		timeconfig
Version:	3.2
Release:	%mkrel 21
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


%changelog
* Fri May 06 2011 Oden Eriksson <oeriksson@mandriva.com> 3.2-20mdv2011.0
+ Revision: 670686
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 3.2-19mdv2011.0
+ Revision: 607996
- rebuild

* Mon Mar 15 2010 Oden Eriksson <oeriksson@mandriva.com> 3.2-18mdv2010.1
+ Revision: 520285
- rebuilt for 2010.1

* Thu Sep 03 2009 Christophe Fergeau <cfergeau@mandriva.com> 3.2-17mdv2010.0
+ Revision: 427374
- rebuild

* Tue Dec 23 2008 Oden Eriksson <oeriksson@mandriva.com> 3.2-16mdv2009.1
+ Revision: 317900
- bunzip patches
- fix build with -Werror=format-security (P2)
- use %%ldflags (P3)

* Wed Jun 18 2008 Thierry Vignaud <tv@mandriva.org> 3.2-15mdv2009.0
+ Revision: 225748
- rebuild

* Wed Mar 05 2008 Oden Eriksson <oeriksson@mandriva.com> 3.2-14mdv2008.1
+ Revision: 179650
- rebuild

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request
    - fix summary-ended-with-dot

* Mon Oct 01 2007 Andreas Hasenack <andreas@mandriva.com> 3.2-13mdv2008.0
+ Revision: 94186
- fix usermode configuration
- fix pam configuration (#31658)

* Thu Aug 23 2007 Thierry Vignaud <tv@mandriva.org> 3.2-12mdv2008.0
+ Revision: 70355
- fileutils, sh-utils & textutils have been obsoleted by coreutils a long time ago

* Fri Jun 15 2007 Adam Williamson <awilliamson@mandriva.org> 3.2-11mdv2008.0
+ Revision: 40160
- drop menu entry (CLI app); rebuild for new era
- Import timeconfig



* Sun Jan 01 2006 Mandriva Linux Team <http://www.mandrivaexpert.com/> 3.2-10mdk
- Rebuild

* Mon Oct 20 2003 Frederic Lepied <flepied@mandrakesoft.com> 3.2-9mdk
- rebuild for rewriting /etc/pam.d file

* Fri Jun 06 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 3.2-8mdk
- use double %%'s in changelog

* Mon Jan  6 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.2-7mdk
- Rebuild, use PNG for menu icons, remove unpackaged files

* Mon Nov  4 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.2-6mdk
- Ooops, how come newt library was not installed?

* Mon Nov  4 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.2-5mdk
- Rebuild for newt updates
- Patch2: Link with libslang
- BuildRequires: slang-devel

* Tue Oct 29 2002 Stefan van der Eijk <stefan@eijk.nu> 3.2-4mdk
- BuildRequires: gettext

* Fri Feb 22 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 3.2-3mdk
- require usermode-consoleonly

* Wed Jul 18 2001 Francis Galiegue <fg@mandrakesoft.com> 3.2-2mdk
- Recompile to get correct distrib tag
- Fixed %%post script

* Tue May 22 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 3.2-1mdk
- Bump out the nice and tasty 3.2 for everyone in cooker.
- s/Copyright/License/;

* Thu Apr 12 2001 Frederic Crozat <fcrozat@mandrakesoft.com> 3.0.13-2mdk
- Correct menu entry to use terminal

* Thu Jan 18 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 3.0.13-1mdk
- new and shiny source.
- remove the BM fix from Francis, should no longer be needed.
- add a specific requirement on usermode.
- remove the glibc requirement. With glibc 2.2 already out that's a bit silly.
- force linking to consolehelper to build on machines without usermode.

* Thu Jan 04 2001 Francis Galiegue <fg@mandrakesoft.com> 3.0.2-13mdk

- Menu title now capitalised to please rpmlint
- s,newt-devel,lib&, in BuildRequires for lib policy

* Tue Oct 10 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.0.2-12mdk
- remove ownership on %%{_iconsdir} and the like

* Wed Oct 04 2000 Francis Galiegue <fg@mandrakesoft.com> 3.0.2-11mdk
- Use usermode, not kdesu

* Wed Sep 20 2000 Francis Galiegue <fg@mandrakesoft.com> 3.0.2-10mdk
- Mini and large icons made transparent

* Fri Sep 15 2000 Francis Galiegue <fg@mandrakesoft.com> 3.0.2-9mdk
- Icons from LN
- Updated menu entry accordingly

* Mon Aug 07 2000 Frederic Lepied <flepied@mandrakesoft.com> 3.0.2-8mdk
- automatically added BuildRequires

* Fri Jul 28 2000 Francis Galiegue <fg@mandrakesoft.com> 3.0.2-7mdk
- BMacros
- %%files list fixes
- What was doing that rm -f /usr/lib/zoneinfo in %%install?
- Really apply patch 0 ;)

* Tue May  9 2000 Vincent Saugey <vince@mandrakesoft.com> 3.0.2-6mdk
- Remove menu entry for setclock

* Fri Mar 31 2000 DindinX <odin@mandrakesoft.com> 3.0.2-5mdk
- Spec fixes
- change group
- Added Menu

* Thu Dec 30 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Add standard mandrake colors.

* Tue Dec 14 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Fix if gmt entry is in clock.

* Sat Nov 06 1999 John Buswell <johnb@mandrakesoft.com>
- 3.0.2
- Build Release

* Tue Oct 26 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- 3.0.1
- fix setlock script(r).

* Mon Oct 25 1999 Pixel <pixel@mandrakesoft.com>
- fixed post (once again :)

* Fri Oct  1 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Rebuild for newt0.50.

* Tue Sep 07 1999 Pablo Saratxaga <pablo@mandrakesoft.com>
- fixed indonesian language code (it is 'id' not 'in')

* Wed Aug 25 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- fix post more..

* Thu Jul 15 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- fix %%post.

* Fri Jul  2 1999 Axalon Bloodstone <axalon@linux-mandrake.com
- version 3.0

* Sat Apr 10 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- Mandrake adaptions
- bzip2 man/info pages
- add de locale

* Tue Mar  9 1999 Jeff Johnson <jbj@redhat.com>
- add in_ID.po

* Sun Jan 10 1999 Matt Wilson <msw@redhat.com>
- rebuilt against newt 0.40

* Tue Dec 15 1998 Jeff Johnson <jbj@redhat.com>
- add ru.po.

* Thu Oct 22 1998 Bill Nottingham <notting@redhat.com>
- built for Raw Hide (slang-1.2.2)

* Thu Oct 08 1998 Cristian Gafton <gafton@redhat.com>
- updated czech translation (and use cs instead of cz)

* Fri Sep 25 1998 Arnaldo Carvalho de Melo <acme@conectiva.com.br>
- added pt_BR translations
- pt_BR man translations
- man tree, with Makefile
- top level Makefile calls make -C po clean & make -C man install

* Fri Sep 25 1998 Jeff Johnson <jbj@redhat.com>
- add sr.po.

* Sun Aug 02 1998 Erik Troan <ewt@redhat.com>
- added NEWT_FLAG_SCROLL to listbox creation for newt 0.30
- added --test

* Fri Jun 05 1998 Erik Troan <ewt@redhat.com>
- return 0 on success

* Thu May 07 1998 Erik Troan <ewt@redhat.com>
- many more translations

* Mon Apr 20 1998 Erik Troan <ewt@redhat.com>
- uses a build root
- added de and en_RN translations

* Mon Mar 23 1998 Erik Troan <ewt@redhat.com>
- shortended window a bit -- white (rather, blue) space is a good thing

* Sun Mar 22 1998 Erik Troan <ewt@redhat.com>
- added --back option

* Sat Oct 11 1997 Erik Troan <ewt@redhat.com>
- use proper flags for hwclock

* Tue Sep 16 1997 Erik Troan <ewt@redhat.com>
- instead of creating /usr/lib/zoneinfo, just update /etc/localtime

* Wed Sep 10 1997 Erik Troan <ewt@redhat.com>
- look for zoneinfo in /usr/share instead of /usr/lib
- provide /usr/lib/zoneinfo symlink
