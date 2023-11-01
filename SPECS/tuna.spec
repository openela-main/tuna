Name: tuna
Version: 0.18
Release: 12%{?dist}
License: GPLv2
Summary: Application tuning GUI & command line utility
URL: https://git.kernel.org/pub/scm/utils/tuna/tuna.git
Source: https://www.kernel.org/pub/software/utils/%{name}/%{name}-%{version}.tar.xz

BuildArch: noarch
BuildRequires: python3-devel, gettext
Requires: python3-linux-procfs >= 0.6
# This really should be a Suggests...
# Requires: python-inet_diag

# Patches
Patch1: tuna-Update-command-line-interface.patch
Patch2: tuna-Move-get_policy_and_rtprio-call-to-parser-level.patch
Patch3: tuna-Add-sockets-command-line-option.patch
Patch4: tuna-Replace-python_ethtool-with-builtin-funtionalit.patch
Patch5: tuna-Fix-matching-irqs-in-ps_show_thread.patch
Patch6: tuna-Remove-threads-print-statement.patch
Patch7: tuna-tuna_gui.py-use-fstrings.patch
Patch8: tuna-tuna-cmd.py-use-fstrings.patch
Patch9: tuna-tuna.py-use-fstrings.patch
Patch10: tuna-remove-import-and-fix-help-message.patch
Patch11: tuna-Update-manpages-for-argparse-CLI-changes.patch
Patch12: tuna-Adapt-show_threads-cgroup-output-to-terminal-si.patch
Patch13: tuna-Fix-show_threads-cgroups-run-without-a-term.patch

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
%py3_build
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" tuna/
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" tuna-cmd.py

%install
rm -rf %{buildroot}
%py3_install
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

# l10n-ed message catalogues
for lng in `cat po/LINGUAS`; do
        po=po/"$lng.po"
        mkdir -p %{buildroot}/%{_datadir}/locale/${lng}/LC_MESSAGES
        msgfmt $po -o %{buildroot}/%{_datadir}/locale/${lng}/LC_MESSAGES/%{name}.mo
done

%find_lang %name

%files -f %{name}.lang
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
* Wed Nov 23 2022 Leah Leshchinsky <lleshchi@redhat.com> - 0.18-12
- Fix show_threads --cgroups run without term
Resolves: rhbz#2121517

* Fri Nov 18 2022 Leah Leshchinsky <lleshchi@redhat.com> - 0.18-11
- Adapt show_threads cgroup output to terminal size
Resolves: rhbz#2121517

* Wed Nov 09 2022 Leah Leshchinsky <lleshchi@redhat.com> - 0.18-10
- Edit run_tests.sh to support new CLI changes
Resolves: rhbz#2141349

* Tue Nov 08 2022 Leah Leshchinsky <lleshchi@redhat.com> - 0.18-9
- Remove import and fix help message
- Update manpages for argparse CLI changes
Resolves: rhbz#2138692

* Wed Nov 02 2022 Leah Leshchinsky <lleshchi@redhat.com> - 0.18-8
- Use f-strings in tuna where possible
Resolves: rhbz#2120803

* Wed Oct 26 2022 Leah Leshchinsky <lleshchi@redhat.com> - 0.18-7
- Add sockets command line option
Resolves: rhbz#2122781

* Wed Oct 26 2022 Leah Leshchinsky <lleshchi@redhat.com> - 0.18-6
- Update tuna command line interface
- Move get_policy_and_rtprio call to parser level
- Remove threads print statement
Resolves: rhbz#2062865

* Mon Oct 03 2022 John Kacur <jkacur@redhat.com> - 0.18-5
- Match irqs with "irqs/"
Resolves: rhbz#2131343

* Fri Sep 30 2022 John Kacur <jkacur@redhat.com> - 0.18-4
- Remove the "Requires" of python-ethtool from the specfile
Resolves: rhbz#2123751

* Fri Sep 30 2022 John Kacur <jkacur@redhat.com> - 0.18-3
- Replace dependency on python-ethtool with built-in functionality
Resolves: rhbz#2123751

* Wed Jun 29 2022 Leah Leshchinsky <lleshchi@redhat.com> - 0.18-2
- Delete patches
Resolves: rhbz#2068629

* Wed Jun 29 2022 Leah Leshchinsky <lleshchi@redhat.com> - 0.18-1
- Update to latest upstream tuna-0.18
Resolves: rhbz#2068629

* Wed May 11 2022 Leah Leshchinsky <lleshchi@redhat.com> - 0.17-4
- Add logging infrastructure to tuna cmd
- Add cleanlogs rule to Makefile
Resolves: rhbz#2062881

* Mon Apr 11 2022 Leah Leshchinsky <lleshchi@redhat.com> - 0.17-3
- Fix typo for variable parm
- Handle get_policy_and_rtprio exceptions
- Remove finally block in get_policy_and_rtprio
Resolves: rhbz#2049303

* Thu Jan 13 2022 Leah Leshchinsky <lleshchi@redhat.com> - 0.17-2
- Fix ModuleNotFoundError
Resolves: rhbz#2012307

* Tue Jan 11 2022 Leah Leshchinsky <lleshchi@redhat.com> - 0.17-1
- Rebase to upstream version 0.17
Resolves: rhbz#2012307

* Tue Dec 14 2021 John Kacur <jkacur@redhat.com> - 0.16-6
- Display correct cpu-affinity when a cpu is disabled
Resolves: rhbz#2032460

* Thu Nov 11 2021 John Kacur <jkacur@redhat.com> - 0.16-5
- Make it clear in online help and man pages that --include and --isolate
  affect IRQs as well as threads
Resolves: rhbz#2022142

* Tue Nov 02 2021 Leah Leshchinsky <lleshchi@redhat.com> - 0.16-4
- Add distinction between spread and move to error message
Resolves: rhbz#2012243

* Thu Oct 28 2021 John Kacur <jkacur@redhat.com> - 0.16-3
- Print warning if setaffinity causes EBUSY and continue
Resolves: rhbz#2016540

* Tue Aug 10 2021 Mohan Boddu <mboddu@redhat.com> - 0.16-2
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Wed Jun 30 2021 John Kacur <jkacur@redhat.com> - 0.16-1
- Update to latest upstream tuna-0.16
Resolves: rhbz#1890565

* Mon Jun 14 2021 John Kacur <jkacur@redhat.com> - 0.15-3
- Remove oscilloscope from tuna
Resolves: rhbz#1970997

* Fri May 21 2021 John Kacur <jkacur@redhat.com> - 0.15-2
- Remove python3-schedutils from the Requires in the spec file
- Update the URL in the spec file
Resolves: rhbz#1890541

* Mon May 17 2021 John Kacur <jkacur@redhat.com> - 0.15-1
- Rebase to tuna-0.15
- This includes changes to remove the python-schedutils dependency
Resolves: rhbz#1890541

* Fri Apr 16 2021 Mohan Boddu <mboddu@redhat.com> - 0.14.1-5
- Rebuilt for RHEL 9 BETA on Apr 15th 2021. Related: rhbz#1947937

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.14.1-2
- Rebuilt for Python 3.9

* Thu May 21 2020 Jiri Kastner <jkastner@fedoraproject.org> - 0.14.1
- update to 0.14.1
- fixes RHBZ#1773339

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.14-5
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.14-4
- Rebuilt for Python 3.8

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Feb 12 2019 Jiri Kastner <jkastner@fedoraproject.org> - 0.14-3
- upload patch

* Tue Feb 12 2019 Jiri Kastner <jkastner@fedoraproject.org> - 0.14-2
- oscilloscope gtk3 patch

* Tue Feb 12 2019 Jiri Kastner <jkastner@fedoraproject.org> - 0.14-1
- update to 0.14
- switch to python3

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 14 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.13.1-6
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

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
