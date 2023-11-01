Name: tuna
Version: 0.18
Release: 6%{?dist}
License: GPLv2
Summary: Application tuning GUI & command line utility
Group: Applications/System
Source: https://www.kernel.org/pub/software/utils/tuna/%{name}-%{version}.tar.xz
URL: https://git.kernel.org/pub/scm/utils/tuna/tuna.git

BuildArch: noarch
BuildRequires: python3-devel, gettext
Requires: python3-linux-procfs >= 0.6
# This really should be a Suggests...
# Requires: python-inet_diag
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

# PATCHES
Patch1: tuna-Replace-python_ethtool-with-builtin-funtionalit.patch
Patch2: tuna-Fix-matching-irqs-in-ps_show_thread.patch
Patch3: tuna-tuna.py-use-fstrings.patch
Patch4: tuna-tuna_gui.py-use-fstrings.patch
Patch5: tuna-tuna-cmd.py-use-fstrings.patch
Patch6: tuna-Adapt-show_threads-cgroup-output-to-terminal-si.patch
Patch7: tuna-Fix-show_threads-cgroup-without-a-term.patch

%description
Provides interface for changing scheduler and IRQ tunables, at whole CPU and at
per thread/IRQ level. Allows isolating CPUs for use by a specific application
and moving threads and interrupts to a CPU by just dragging and dropping them.
Operations can be done on CPU sockets, understanding CPU topology.

Can be used as a command line utility without requiring the GUI libraries to be
installed.

%prep
%autosetup -p1

%build
%{__python3} setup.py build

%install
rm -rf %{buildroot}
%{__python3} setup.py install --skip-build --root %{buildroot}
mkdir -p %{buildroot}/%{_sysconfdir}/tuna/
mkdir -p %{buildroot}/{%{_bindir},%{_datadir}/tuna/help/kthreads,%{_mandir}/man8}
mkdir -p %{buildroot}/%{_datadir}/polkit-1/actions/
install -p -m644 tuna/tuna_gui.glade %{buildroot}/%{_datadir}/tuna/
install -p -m755 tuna-cmd.py %{buildroot}/%{_bindir}/tuna
install -p -m644 help/kthreads/* %{buildroot}/%{_datadir}/tuna/help/kthreads/
install -p -m644 docs/tuna.8 %{buildroot}/%{_mandir}/man8/
install -p -m644 etc/tuna/example.conf %{buildroot}/%{_sysconfdir}/tuna/
install -p -m644 etc/tuna.conf %{buildroot}/%{_sysconfdir}/
install -p -m644 org.tuna.policy %{buildroot}/%{_datadir}/polkit-1/actions/

# Manually fix the shebang
pathfix.py -pni "%{__python3}" %{buildroot}%{_bindir}/tuna

# l10n-ed message catalogues
for lng in `cat po/LINGUAS`; do
        po=po/"$lng.po"
        mkdir -p %{buildroot}/%{_datadir}/locale/${lng}/LC_MESSAGES
        msgfmt $po -o %{buildroot}/%{_datadir}/locale/${lng}/LC_MESSAGES/%{name}.mo
done

%find_lang %name

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc ChangeLog
%{python3_sitelib}/*.egg-info
%{_bindir}/tuna
%{_datadir}/tuna/
%{python3_sitelib}/tuna/
%{_mandir}/man8/tuna.8*
%{_sysconfdir}/tuna.conf
%{_sysconfdir}/tuna/*
%{_datadir}/polkit-1/actions/org.tuna.policy

%changelog
* Wed Nov 23 2022 Leah Leshchinsky <lleshchi@redhat.com> - 0.18-6
- Fix show_threads --cgroups without a term
Resolves: rhbz#2121518

* Fri Nov 18 2022 Leah Leshchinsky <lleshchi@redhat.com> - 0.18-5
- Adapt show_threads cgroup output to terminal size
Resolves: rhbz#2121518

* Wed Nov 02 2022 Leah Leshchinsky <lleshchi@redhat.com> - 0.18-4
- Use f-strings in tuna where possible
Resolves: rhbz#2120805

* Mon Oct 03 2022 John Kacur <jkacur@redhat.com> - 0.18-3
- Match irqs with "irqs/"
Resolves: rhbz#2131353

* Fri Sep 30 2022 John Kacur <jkacur@redhat.com> - 0.18-2
- Replace dependency on python-ethtool with built-in functionality
Resolves: rhbz#2123753

* Wed Jun 29 2022 Leah Leshchinsky <lleshchi@redhat.com> - 0.18-1
- Rebase to upstream version 0.18
Resolves: rhbz#2073555

* Thu May 19 2022 Leah Leshchinsky <lleshchi@redhat.com> - 0.17-3
- Add logging infrastructure to tuna
- Add cleanlogs rule to Makefile
Resolves: rhbz#2062882

* Mon Apr 11 2022 Leah Leshchinsky <lleshchi@redhat.com> - 0.17-2
- Fix typo for variable parm
- Handle get_policy_and_rtprio exceptions
- Remove finally block in get_policy_and_rtprio
Resolves: rhbz#2049746

* Thu Jan 13 2022 Leah Leshchinsky <lleshchi@redhat.com> - 0.17-1
- Rebase to upstream version 0.17
- Fix ModuleNotFoundError
Resolves: rhbz#2012306

* Tue Dec 14 2021 John Kacur <jkacur@redhat.com> - 0.16-5
- Display correct cpu-affinity when a cpu is disabled
Resolves: rhbz#2032614

* Wed Nov 10 2021 John Kacur <jkacur@redhat.com> - 0.16-4
- Make it clear in online help and man pages that --include and --isolate
  affect IRQs as well as threads
Resolves: rhbz#1886804

* Thu Oct 28 2021 John Kacur <jkacur@redhat.com> - 0.16-3
- Print warning if setaffinity causes EBUSY and continue
Resolves: rhbz#2018285

* Tue Oct 26 2021 Leah Leshchinsky <lleshchi@redhat.com> - 0.16-2
- Add distinction between --spread and --move to error message
Resolves: rhbz#2012241

* Wed Jun 30 2021 John Kacur <jkacur@redhat.com> - 0.16-1
- Upgrade to latest upstream
Resolves: rhbz#1947069

* Thu Jan 21 2021 John Kacur <jkacur@redhat.com> - 0.15-1
- Upgrade to latest upstream code
- Upstream drops python-schedutils and uses built-in schedutils
Resolves: rhbz#1890558

* Tue Apr 02 2019 Clark Williams <williams@redhat.com> - 0.14-4
- added OSCI gating framework
Resolves: rhbz#1682423

* Fri Feb 01 2019 John Kacur <jkacur@redhat.com> - 0.14-3
- fix undefined global name stderr
Resolves: rhbz#1671440

* Tue Dec 04 2018 John Kacur <jkacur@redhat.com> - 0.14-2
- Add method to compare class cpu for sorting
- Use args attributes for exceptions for python3
Resolves: rhbz#1651465

* Fri Aug 10 2018 John Kacur <jkacur@redhat.com> - 0.14-1
- Sync with upstream and fix URL reference in spec
Resolves: rhbz#1596855

* Wed Aug 08 2018 John Kacur <jkacur@redhat.com> - 0.13.3-5
- Remove some functions that are now available in python-linux-procfs
Resolves: rhbz#1522865

* Tue Jul 03 2018 Tomas Orsava <torsava@redhat.com> - 0.13.3-4
- Switch hardcoded python3 shebangs into the %%{__python3} macro

* Thu May 31 2018 John Kacur <jkacur@redhat.com> - 0.13.3-3
- Remove deprecated oscilloscope
Resolves: rhbz#1584302

* Fri May 25 2018 John Kacur <jkacur@redhat.com> - 0.13.3-2
- Correct the dependencies to require python3 package versions
Resolves: rhbz#1581192

* Wed May 16 2018 John Kacur <jkacur@redhat.com> - 0.13.3-1
- Changes for python3
Resolves: rhbz#1518679

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Nov 29 2017 Lubomir Rintel <lkundrak@v3.sk> - 0.13.1-4
- Add a missing dependency for oscilloscope

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Dec 21 2016 Jiri Kastner <jkastner@redhat.com> - 0.13.1-1
- new version

* Mon Sep 26 2016 Dominik Mierzejewski <rpm@greysector.net> - 0.12-5
- rebuilt for matplotlib-2.0.0

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Oct 10 2014 Jiri Kastner <jkastner@redhat.com> - 0.12-1
- new upstream release

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jul 29 2013 Jiri Kastner <jkastner@redhat.com> - 0.11.1-1
- New upstream release

* Tue Jun 11 2013 Jiri Kastner <jkastner@redhat.com> - 0.11-2
- changed dependencies from python-numeric to numpy
- merged spec changes from upstream

* Thu Jun  6 2013 Jiri Kastner <jkastner@redhat.com> - 0.11-1
- New upstream release

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Aug 01 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu Sep 03 2009 Arnaldo Carvalho de Melo <acme@redhat.com> - 0.9.1-1
- New upstream release

* Wed Aug 26 2009 Arnaldo Carvalho de Melo <acme@redhat.com> - 0.9-3
- Rewrite the oscilloscope package summary
- Remove the shebang in tuna/oscilloscope.py

* Mon Aug 17 2009 Arnaldo Carvalho de Melo <acme@redhat.com> - 0.9-2
- Use install -p
- Add BuildRequires for gettext

* Fri Jul 10 2009 Arnaldo Carvalho de Melo <acme@redhat.com> - 0.9-1
- Fedora package reviewing changes: introduce ChangeLog file
