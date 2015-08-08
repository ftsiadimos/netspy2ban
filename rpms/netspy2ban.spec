Name: netspy2ban
Version:1.0
Release: 1%{?dist}
Summary: GUI Live Networking Tool and Fail2ban Interface

Group: Applications/System
License: GPLv3+ 
URL: https://github.com/ftsiadimos/netspy2ban
Source0: https://raw.githubusercontent.com/ftsiadimos/netspy2ban/master/rpms/netspy2ban-1.0.tar.gz
Source1: https://raw.githubusercontent.com/ftsiadimos/netspy2ban/master/rpms/%{name}.desktop
BuildArch: noarch

Requires: python2 
Requires: wxPython
Requires: fail2ban

%description
GUI Networking Tool and Fail2ban Graphic User Interface.
The program serves three functions. The first function is to view
connected network cards and their speed. The second is to allow 
real time monitoring of your network connections. Lastly, NetSpy2Ban
includes a graphic user interface to provide user-friendly functionality 
for the Fail2Ban service.

%prep
%setup -q


%build
%define _unpackaged_files_terminate_build 0

%install
mkdir -p %{buildroot}%{_datadir}/applications/
mkdir -p %{buildroot}%{_datadir}/polkit-1/actions/
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/pixmaps/
mkdir -p %{buildroot}%{_mandir}/man1/
mkdir -p %{buildroot}%{python_sitelib}/netspy2ban/
cp netspy2ban %{buildroot}%{python_sitelib}/netspy2ban/
cp fail2ban.py %{buildroot}%{python_sitelib}/netspy2ban/
cp mainpanel.py %{buildroot}%{python_sitelib}/netspy2ban/
cp netstatus.py %{buildroot}%{python_sitelib}/netspy2ban/
cp networkpanel.py %{buildroot}%{python_sitelib}/netspy2ban/
cp winmesg.py %{buildroot}%{python_sitelib}/netspy2ban/
cp netspy2start %{buildroot}%{_bindir}
cp taskbar.py %{buildroot}%{python_sitelib}/netspy2ban/
cp -r icons %{buildroot}%{python_sitelib}/netspy2ban/
cp netspy2ban.policy %{buildroot}%{_datadir}/polkit-1/actions/
cp icons/netspy2ban.png %{buildroot}%{_datadir}/pixmaps/
gzip -9c netspy2ban.1 > netspy2ban.1.gz 
install -m 644 netspy2ban.1.gz  %{buildroot}%{_mandir}/man1/ 
desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{SOURCE1}


%files
%doc README.md 
%license LICENSE
%{_bindir}/netspy2start
%{python_sitelib}/netspy2ban/netspy2ban
%{python_sitelib}/netspy2ban/*.py
%{python_sitelib}/netspy2ban/icons/*
%{_datadir}/applications/netspy2ban.desktop
%{_datadir}/polkit-1/actions/netspy2ban.policy
%{_datadir}/pixmaps/netspy2ban.png
%{_mandir}/man1/%{name}.*

%post
systemctl start fail2ban
systemctl enable fail2ban

%postun
rm -rf %{python_sitelib}/netspy2ban

%changelog
* Sun Jul 05 2015 Fotios Tsiadimos <ftsiadimos@gmail.com> 1.0-1
- Initial setup
