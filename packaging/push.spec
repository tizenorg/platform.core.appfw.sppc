Name:       push
Summary:    Push services and client library
Version:    0.2.42
Release:    3
Group:      Application Framwork/Service
License:    Flora
Source0:    %{name}-%{version}.tar.gz
Source1001: %{name}.manifest


%description
Push services and client library.

%package -n libpush
Summary:    Push service client library
Group:      Application Framwork/Libraries
Provides:   libpush.so.0

%description -n libpush
Push service client library


%package -n libpush-devel
Summary:    Push service client library (DEV)
Group:      devel
Requires:   libpush = %{version}-%{release}
Requires:   capi-appfw-application-devel

%description -n libpush-devel
Push service client library (DEV)


%package bin
Summary:    Push service daemon
Group:      Application Framwork/Service
Requires:   badge

%description bin
Push service daemon


%package tool
Summary:    Push service tool
Group:      devel
Requires:   libpush = %{version}-%{release}
Requires:   %{name}-bin = %{version}-%{release}

%description tool
Push service tool



%prep
%setup -q
cp %{SOURCE1001} .

%build

%install
rm -rf %{buildroot}


mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_libdir}/pkgconfig
mkdir -p %{buildroot}%{_includedir}
mkdir -p %{buildroot}/usr/share/push
mkdir -p %{buildroot}%{_sysconfdir}/init.d
mkdir -p %{buildroot}%{_sysconfdir}/rc.d/{rc3.d,rc5.d}
mkdir -p %{buildroot}/usr/lib/systemd/user/tizen-middleware.target.wants


%ifarch %{arm}
#libpush
cp -a arm/lib/libpush.so.* %{buildroot}%{_libdir}
#libpush-devel
cp -a arm/include/push.h %{buildroot}%{_includedir}
cp -a arm/lib/pkgconfig/push.pc %{buildroot}%{_libdir}/pkgconfig/push.pc
cp -a arm/lib/libpush.so %{buildroot}%{_libdir}
#push-bin
cp -a arm/bin/pushd %{buildroot}%{_bindir}
cp -a arm/share/push/PushServerTrust.cer %{buildroot}/usr/share/push/PushServerTrust.cer
cp -a arm/etc/init.d/pushd %{buildroot}%{_sysconfdir}/init.d/pushd
cp -a arm/etc/rc.d/rc3.d/S90pushd %{buildroot}%{_sysconfdir}/rc.d/rc3.d/S90pushd
cp -a arm/etc/rc.d/rc5.d/S90pushd %{buildroot}%{_sysconfdir}/rc.d/rc5.d/S90pushd
cp -a arm/lib/systemd/user/pushd.service %{buildroot}%{_libdir}/systemd/user/pushd.service
cp -a arm/lib/systemd/user/tizen-middleware.target.wants/pushd.service \
    %{buildroot}%{_libdir}/systemd/user/tizen-middleware.target.wants/pushd.service
#push-tool
cp -a arm/bin/push_tool %{buildroot}%{_bindir}
%else
#libpush
cp -a x86/lib/libpush.so.* %{buildroot}%{_libdir}
#libpush-devel
cp -a x86/include/push.h %{buildroot}%{_includedir}
cp -a x86/lib/pkgconfig/push.pc %{buildroot}%{_libdir}/pkgconfig/push.pc
cp -a x86/lib/libpush.so %{buildroot}%{_libdir}
#push-bin
cp -a x86/bin/pushd %{buildroot}%{_bindir}
cp -a x86/share/push/PushServerTrust.cer %{buildroot}/usr/share/push/PushServerTrust.cer
cp -a x86/etc/init.d/pushd %{buildroot}%{_sysconfdir}/init.d/pushd
cp -a x86/etc/rc.d/rc3.d/S90pushd %{buildroot}%{_sysconfdir}/rc.d/rc3.d/S90pushd
cp -a x86/etc/rc.d/rc5.d/S90pushd %{buildroot}%{_sysconfdir}/rc.d/rc5.d/S90pushd
cp -a x86/lib/systemd/user/pushd.service %{buildroot}/usr/lib/systemd/user/pushd.service
cp -a x86/lib/systemd/user/tizen-middleware.target.wants/pushd.service \
    %{buildroot}/usr/lib/systemd/user/tizen-middleware.target.wants/pushd.service
#push-tool
cp -a x86/bin/push_tool %{buildroot}%{_bindir}
%endif

%post bin
mkdir -p /opt/dbspace
sqlite3 /opt/dbspace/.push.db "PRAGMA journal_mode = PERSIST; create table a(a); drop table a;" > /dev/null
chown root:5000 /opt/dbspace/.push.db
chown root:5000 /opt/dbspace/.push.db-journal
chmod 660 /opt/dbspace/.push.db
chmod 660 /opt/dbspace/.push.db-journal


_VER="1"
_DEV_TYPE="00000000"
_DEV_INFO="device.model=ssltest"
_IP_PV="gld.push.samsungosp.com"
_PORT_PV=5223
#ping interval {120,240,480,960,1920}
_PING_INT=480
_GRP="-g 5000"

vconftool set -t string file/private/push-bin/version ${_VER} ${_GRP} -f
vconftool set -t string file/private/push-bin/dev_type ${_DEV_TYPE} ${_GRP} -f
vconftool set -t string file/private/push-bin/dev_info ${_DEV_INFO} ${_GRP} -f
vconftool set -t string file/private/push-bin/ip_pv ${_IP_PV} ${_GRP} -f
vconftool set -t int    file/private/push-bin/port_pv ${_PORT_PV} ${_GRP} -f
vconftool set -t int    file/private/push-bin/ping_int ${_PING_INT} ${_GRP} -f
vconftool set -t string file/private/push-bin/devtk "" ${_GRP} -f
vconftool set -t string file/private/push-bin/ip_pri "" ${_GRP} -f
vconftool set -t int    file/private/push-bin/port_pri -1 ${_GRP} -f
vconftool set -t string file/private/push-bin/ip_sec "" ${_GRP} -f
vconftool set -t int    file/private/push-bin/port_sec -1 ${_GRP} -f

#vconftool unset file/private/push-bin/devtk

%post -n libpush
/sbin/ldconfig

%postun -n libpush -p /sbin/ldconfig


%files -n libpush
%manifest %{name}.manifest
%attr(644,-,-) %{_libdir}/libpush.so.*

%files -n libpush-devel
%manifest %{name}.manifest
%attr(644,-,-) %{_includedir}/*.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libpush.so

%files bin
%manifest %{name}.manifest
%{_bindir}/pushd
/usr/share/push/*.cer
/etc/init.d/pushd
/etc/rc.d/rc3.d/S90pushd
/etc/rc.d/rc5.d/S90pushd
/usr/lib/systemd/user/pushd.service
/usr/lib/systemd/user/tizen-middleware.target.wants/pushd.service

%files tool
%manifest %{name}.manifest
%{_bindir}/push_tool

%changelog
* Mon Oct 22 2012 Jooseok Park <jooseok.park@samsung.com> - 0.2.25
- bundle null check added & protobuf null check added
* Wed Sep 19 2012 Jooseok Park <jooseok.park@samsung.com> - 0.2.24
- when pkg is uninstlled, db process is added
* Fri Sep 7 2012 Jooseok Park <jooseok.park@samsung.com> - 0.2.23
- emul check logic is changed(using capi-system-info)
* Tue Sep 4 2012 Jooseok Park <jooseok.park@samsung.com> - 0.2.22
- decoding of message with space character which is urlencoded to "+"
* Wed Aug 29 2012 Jooseok Park <jooseok.park@samsung.com> - 0.2.21
- package uninstalled event added
* Fri Aug 17 2012 Jooseok Park <jooseok.park@samsung.com> - 0.2.20
- debug msg added & some internal function name changed
* Wed Aug 8 2012 Jooseok Park <jooseok.park@samsung.com> - 0.2.19
- push noti default action is silent, and old key is deleted
* Wed Aug 8 2012 Jooseok Park <jooseok.park@samsung.com> - 0.2.18
- tapi imei api is changed for new tapi
* Tue Aug 7 2012 Jooseok Park <jooseok.park@samsung.com> - 0.2.17
- emulator check func is added
* Wed Jul 25 2012 Jooseok Park <jooseok.park@samsung.com> - 0.2.16
- OSP Push noti support(alertMessage,..)

