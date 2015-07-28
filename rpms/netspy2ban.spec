Name: netspy2ban
Version:1.0
Release: 1%{?dist}
Summary: GUI Networking Tool

Group: Applications/System
License:GPL 
URL: https://github.com/ftsiadimos/netspy2ban
Source0: http://github.com/ftsiadimos/netspy2ban/blob/master/rpms/netspy2ban-1.0.tar.gz
BuildArch: noarch

Requires: wxPython, fail2ban, python

%description
GUI Networking Tool and Fail2ban Controller

%prep
%setup -q


%build
%define _unpackaged_files_terminate_build 0

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{python_sitelib}/netspy2ban/
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications/
mkdir -p $RPM_BUILD_ROOT%{_datadir}/polkit-1/actions/
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/pixmaps/
cp netspy2ban $RPM_BUILD_ROOT%{python_sitelib}/netspy2ban/
cp fail2ban.py $RPM_BUILD_ROOT%{python_sitelib}/netspy2ban/
cp mainpanel.py $RPM_BUILD_ROOT%{python_sitelib}/netspy2ban/
cp netstatus.py $RPM_BUILD_ROOT%{python_sitelib}/netspy2ban/
cp networkpanel.py $RPM_BUILD_ROOT%{python_sitelib}/netspy2ban/
cp winmesg.py $RPM_BUILD_ROOT%{python_sitelib}/netspy2ban/
cp netspy2start $RPM_BUILD_ROOT%{_bindir}
cp taskbar.py $RPM_BUILD_ROOT%{python_sitelib}/netspy2ban/
cp -r icons $RPM_BUILD_ROOT%{python_sitelib}/netspy2ban/
cp netspy2ban.desktop $RPM_BUILD_ROOT%{_datadir}/applications/
cp netspy2ban.policy $RPM_BUILD_ROOT%{_datadir}/polkit-1/actions/
cp icons/netspy2ban.png $RPM_BUILD_ROOT%{_datadir}/pixmaps/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc README.md
%defattr(-,root,root,-)
%{_bindir}/netspy2start
%{python_sitelib}/netspy2ban/netspy2ban
%{python_sitelib}/netspy2ban/*.py
%{python_sitelib}/netspy2ban/icons/*
%{_datadir}/applications/netspy2ban.desktop
%{_datadir}/polkit-1/actions/netspy2ban.policy
%{_datadir}/pixmaps/netspy2ban.png

%post
systemctl start fail2ban
systemctl enable fail2ban

%postun
rm -rf %{python_sitelib}/netspy2ban

%changelog
* Sun Jul 05 2015 Fotios Tsiadimos <ftsiadimos@gmail.com> 1.0-1
- Initial setup
