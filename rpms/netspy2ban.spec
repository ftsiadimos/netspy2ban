Name: netspy2ban		
Version:1.0	
Release:	1%{?dist}
Summary: GUI Networking Tool 	

Group:	Applications
License:GPL	
URL:	https://github.com/ftsiadimos/netspy2ban	
Source0:	netspy2ban-1.0.tar.gz
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
mkdir -p $RPM_BUILD_ROOT/usr/lib/python2.7/site-packages/netspy2ban/
mkdir -p $RPM_BUILD_ROOT/usr/share/applications/
mkdir -p $RPM_BUILD_ROOT/usr/share/polkit-1/actions/
mkdir -p $RPM_BUILD_ROOT/usr/bin/
mkdir -p $RPM_BUILD_ROOT/usr/share/pixmaps/
cp netspy2ban $RPM_BUILD_ROOT/usr/lib/python2.7/site-packages/netspy2ban/
cp fail2ban.py $RPM_BUILD_ROOT/usr/lib/python2.7/site-packages/netspy2ban/
cp mainpanel.py $RPM_BUILD_ROOT/usr/lib/python2.7/site-packages/netspy2ban/
cp netstatus.py $RPM_BUILD_ROOT/usr/lib/python2.7/site-packages/netspy2ban/
cp networkpanel.py $RPM_BUILD_ROOT/usr/lib/python2.7/site-packages/netspy2ban/
cp winmesg.py $RPM_BUILD_ROOT/usr/lib/python2.7/site-packages/netspy2ban/
cp netspy2start $RPM_BUILD_ROOT/usr/bin/
cp taskbar.py $RPM_BUILD_ROOT/usr/lib/python2.7/site-packages/netspy2ban/
cp -r icons $RPM_BUILD_ROOT/usr/lib/python2.7/site-packages/netspy2ban/
cp netspy2ban.desktop $RPM_BUILD_ROOT/usr/share/applications/
cp netspy2ban.policy $RPM_BUILD_ROOT/usr/share/polkit-1/actions/
cp icons/netspy2ban.png $RPM_BUILD_ROOT/usr/share/pixmaps/
%clean 
rm -rf $RPM_BUILD_ROOT

%files
%doc README.md
%defattr(-,root,root,-)
%attr(0755,root,root,)/usr/bin/netspy2start
%attr(0744,root,root,)/usr/lib/python2.7/site-packages/netspy2ban/netspy2ban
%attr(0744,root,root,)/usr/lib/python2.7/site-packages/netspy2ban/*.py
%attr(0744,root,root,)/usr/lib/python2.7/site-packages/netspy2ban/icons/*
%attr(0644,root,root,)/usr/share/applications/netspy2ban.desktop
%attr(0644,root,root,)/usr/share/polkit-1/actions/netspy2ban.policy
%attr(0644,root,root,)/usr/share/pixmaps/netspy2ban.png

%post
systemctl start fail2ban
systemctl enable fail2ban

%postun
rm -rf /usr/lib/python2.7/site-packages/netspy2ban

%changelog
* Sun Jul 05 2015 Fotios Tsiadimos <ftsiadimos@gmail.com> 1.0-1
- Initial setup
