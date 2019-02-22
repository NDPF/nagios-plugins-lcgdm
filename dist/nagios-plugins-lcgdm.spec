# Package needs to stay arch specific (due to nagios plugins location), but
# there's nothing to extract debuginfo from
%global debug_package %{nil}

%define nagios_plugins_dir %{_libdir}/nagios/plugins
%define pnp4nagios_templates_dir %{_datadir}/nagios/html/pnp4nagios/templates.lcgdm
%define lpylib lfcmetrics
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%define pylib %{python_sitelib}/%{lpylib}

Name:		nagios-plugins-lcgdm
Version:	0.9.6
Release:	1%{?dist}
Summary:	Nagios probes to be run remotely against DPM / LFC nodes
Group:		Applications/Internet
License:	ASL 2.0
URL:		https://svnweb.cern.ch/trac/lcgdm/wiki/Dpm/Admin/Monitoring
# The source of this package was pulled from upstream's vcs. Use the
# following commands to generate the tarball:
# svn export http://svn.cern.ch/guest/lcgdm/nagios-plugins/tags/nagios-plugins_0_9_5 nagios-plugins-lcgdm-0.9.5
# tar -czvf nagios-plugins-lcgdm-0.9.5.tar.gz nagios-plugins-lcgdm-0.9.5 
Source0:	%{name}-%{version}.tar.gz

Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	cmake
BuildRequires:	gcc-c++
BuildRequires:  python

Requires:	nagios-plugins-lcgdm-common%{?_isa} = %{version}-%{release}
Requires:	php%{?_isa}
Requires:	pnp4nagios%{?_isa}

%description
This package provides the nagios probes for LCGDM components (DPM and LFC) that 
need to be run remotely. Usually they are installed in the nagios host, and
they will contact the remote services running in the DPM and LFC hosts.

The Disk Pool Manager (DPM) is a lightweight grid storage component, allowing
access to data using commonly used grid protocols. The LCG File Catalog (LFC)
is the main catalog being used by grid communities for both file bookkeeping
and meta-data.

%package -n nagios-lcgdm
Summary:	Configuration files for a (DPM/LFC) site monitored using LCGDM nagios probes
Group:		Applications/System
Requires:	php%{?_isa}
Requires:	pnp4nagios%{?_isa}

%description -n nagios-lcgdm
This package provides all the necessary configuration file for a (DPM/LFC) site
monitored using the nagios-plugins-lcgdm probes

%package -n nagios-plugins-lcgdm-common
Summary:	Common libraries and files to all LCGDM nagios packages
Group:		Applications/System
Requires:	nagios-common%{?_isa}
Requires:	nagios-plugins%{?_isa}
Requires:	nrpe%{?_isa}
Requires:	python%{?_isa}
Requires:	python-dateutil

%description -n nagios-plugins-lcgdm-common
LCGDM includes both the Disk Pool Manager (DPM) and LCG File Catalog (LFC)
components. This package provides the common libraries and files used by
all LCGDM nagios probes.

%package -n nagios-plugins-dpm-disk
Summary:	Nagios probes to be run in the DPM disk nodes
Group:		Applications/System
Requires:	nagios-plugins-lcgdm-common%{?_isa} = %{version}-%{release}

%description -n nagios-plugins-dpm-disk
This package provides the LCGDM nagios probes to be run in the grid
Disk Pool Manager (DPM) disk nodes.
They cover monitoring of the status of the different daemons, log file
analysis, host certificate checks, etc.

%package -n nagios-plugins-dpm-head
Summary:	Nagios probes to be run in the DPM head node
Group:		Applications/System
Requires:	nagios-plugins-lcgdm-common%{?_isa} = %{version}-%{release}
Requires:	python-ldap%{?_isa}

%description -n nagios-plugins-dpm-head
This package provides the LCGDM nagios probes to be run in the DPM head nodes.
They cover monitoring of the status of the different daemons, log file
analysis, host certificate checks, etc.

%package -n nagios-plugins-lfc
Summary:	Nagios probes to be run in the LFC node
Group:		Applications/System
Requires:	nagios-plugins-lcgdm-common%{?_isa} = %{version}-%{release}
Requires:	lfc-python

%description -n nagios-plugins-lfc
This package provides the LCGDM nagios probes to be run in the LCG File
Catalog (LFC) node.
They cover monitoring of the status of the different daemons, log file
analysis, host certificate checks, etc.

%prep
%setup -n %{name}-%{version}

%build
%cmake . -DCMAKE_INSTALL_PREFIX=/

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}

make install DESTDIR=%{buildroot}

# SAM-3278
install --directory %{buildroot}%{pylib}
install --mode 644 plugins/%{lpylib}/*.py %{buildroot}%{pylib}
%{__python} plugins/setup.py install_lib -O1 --skip-build --build-dir=%{lpylib} --install-dir=%{buildroot}%{pylib}


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/nagios/generic-service.cfg
%config(noreplace) %{_sysconfdir}/nagios/lcgdm-commands.cfg
%config(noreplace) %{_sysconfdir}/nagios/lcgdm-hosts.cfg
%config(noreplace) %{_sysconfdir}/nagios/lcgdm-services.cfg
%{nagios_plugins_dir}/lcgdm/check_dpm
%{nagios_plugins_dir}/lcgdm/check_dpns
%{nagios_plugins_dir}/lcgdm/check_gridftp
%{nagios_plugins_dir}/lcgdm/check_rfio

%files -n nagios-lcgdm
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/nagios/generic-service.cfg
%config(noreplace) %{_sysconfdir}/nagios/lcgdm-commands.cfg
%config(noreplace) %{_sysconfdir}/nagios/lcgdm-hosts.cfg
%config(noreplace) %{_sysconfdir}/nagios/lcgdm-services.cfg
%dir %{pnp4nagios_templates_dir}
%{pnp4nagios_templates_dir}/check_cpu.php
%{pnp4nagios_templates_dir}/check_dpm_perf.php
%{pnp4nagios_templates_dir}/check_dpm_pool.php
%{pnp4nagios_templates_dir}/check_dpm_req.php
%{pnp4nagios_templates_dir}/check_dpns_perf.php
%{pnp4nagios_templates_dir}/check_gridftp_activity.php
%{pnp4nagios_templates_dir}/check_network.php
%{pnp4nagios_templates_dir}/check_partition_activity.php
%{pnp4nagios_templates_dir}/check_process.php
%{pnp4nagios_templates_dir}/check_rfio_activity.php
%{pnp4nagios_templates_dir}/check_space_token.php

%files -n nagios-plugins-lcgdm-common
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/nrpe.d/lcgdm-common.cfg
%dir %{nagios_plugins_dir}/lcgdm
%{nagios_plugins_dir}/lcgdm/check_cpu
%{nagios_plugins_dir}/lcgdm/check_hostcert
%{nagios_plugins_dir}/lcgdm/check_network
%{nagios_plugins_dir}/lcgdm/check_process
%{nagios_plugins_dir}/lcgdm/lcgdmcommon.py*
%doc LICENSE README RELEASE-NOTES

%files -n nagios-plugins-dpm-disk
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/nrpe.d/lcgdm-disk.cfg
%{nagios_plugins_dir}/lcgdm/check_gridftp_activity
%{nagios_plugins_dir}/lcgdm/check_gridftp_transfer
%{nagios_plugins_dir}/lcgdm/check_partition_activity
%{nagios_plugins_dir}/lcgdm/check_rfio_activity

%files -n nagios-plugins-dpm-head
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/nrpe.d/lcgdm-headnode.cfg
%{nagios_plugins_dir}/lcgdm/check_dpm_infosys
%{nagios_plugins_dir}/lcgdm/check_dpm_perf
%{nagios_plugins_dir}/lcgdm/check_dpm_pool
%{nagios_plugins_dir}/lcgdm/check_dpns_perf
%{nagios_plugins_dir}/lcgdm/check_space_token

%files -n nagios-plugins-lfc
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/nrpe.d/lcgdm-lfc.cfg
%{nagios_plugins_dir}/lcgdm/check_lfc_perf
%{nagios_plugins_dir}/lcgdm/check_oracle_expiration
%{nagios_plugins_dir}/lcgdm/check_lfc_sam
%{nagios_plugins_dir}/lcgdm/LFC-probe
%{pylib}/*.py*

%changelog
* Fri Jul 24 2015 Andrea Manzi <amanzi@cern.ch> - 0.9.6-1
- Remove rfio check as Access protocol

* Wed Dec 03 2014 Ivan Calvet <icalvet@cern.ch> - 0.9.5-3
- Merged the LFC-probe with the other probes

* Mon Jun 03 2013 Emir Imamagic <eimamagi@srce.hr> - 0.9.5-2
- Added LFC-probe https://tomtools.its.cern.ch/jira/browse/SAM-3278

* Wed Mar 06 2013 Alejandro Alvarez <aalvarez@cern.ch> - 0.9.5-1
- Update for new upstream release

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 22 2012 Ricardo Rocha <ricardo.rocha@cern.ch> - 0.9.4-1
- Update for new upstream release

* Tue Oct 16 2012 Ricardo Rocha <ricardo.rocha@cern.ch> - 0.9.3-1
- Update for new upstream release

* Wed Sep 12 2012 Ricardo Rocha <ricardo.rocha@cern.ch> - 0.9.2-1
- Added runtime dep on python ldap for dpm-head package

* Wed Jul 11 2012 Ricardo Rocha <ricardo.rocha@cern.ch> - 0.9.1-1
- Update for new upstream release

* Fri May 25 2012 Alexandre Beche <alexandre.beche@cern.ch> - 0.9.0-1
- Update for new upstream release

* Fri Apr 26 2012 Ricardo Rocha <ricardo.rocha@cern.ch> - 0.8.0-1
- Update for new upstream release
- Moved nagios configuration files to separate package (nagios-lcgdm)

* Fri Mar 16 2012 Ricardo Rocha <ricardo.rocha@cern.ch> - 0.7.0-1
- Update for new upstream release
- Do not generate a debuginfo package (bug #756827)

* Sat Nov 19 2011 Ricardo Rocha <ricardo.rocha@cern.ch> - 0.5.0-1
- Removed unnecessary build dependencies
- python-dateutil is noarch, fixed Requires accordingly
- Moved pnp4nagios templates under the default directory
- Moved nagios config files into /etc/nagios 

* Thu Nov 10 2011 Ricardo Rocha <ricardo.rocha@cern.ch> - 0.4.0-3
- Added byte compile python files 

* Fri Nov 04 2011 Ricardo Rocha <ricardo.rocha@cern.ch> - 0.4.0-2
- Use cmake macro for build 

* Mon Oct 17 2011 Ricardo Rocha <ricardo.rocha@cern.ch> - 0.4.0-1
- Initial build
