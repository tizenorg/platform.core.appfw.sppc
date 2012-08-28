Name:       push
Summary:    Push services and client library.
Version:    0.2.20
Release:    1
Group:      TO_BE_FILLED
License:    TO_BE_FILLED
Source0:    %{name}-%{version}.tar.gz
Source1:    push.init

%description
Push services and client library.

%package -n libpush
Summary:    Push service client library
Group:      TO_BE_FILLED
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
Group:      TO_BE_FILLED

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

%build

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}/etc/init.d
install -m 0755 %{SOURCE1} %{buildroot}/etc/init.d/pushd
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_libdir}/pkgconfig
mkdir -p %{buildroot}%{_includedir}
mkdir -p %{buildroot}/usr/share/push

%ifarch %{arm}
#libpush
cp -a arm/lib/libpush.so.* %{buildroot}%{_libdir}
#libpush-devel
cp -a arm/include/push.h %{buildroot}%{_includedir}
cp -a arm/lib/pkgconfig/push.pc %{buildroot}%{_libdir}/pkgconfig/push.pc
cp -a arm/lib/libpush.so %{buildroot}%{_libdir}
#push-bin
cp -a arm/bin/pushd %{buildroot}%{_bindir}
cp -a arm/share/PushServerTrust.cer %{buildroot}/usr/share/push/PushServerTrust.cer
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
cp -a x86/share/PushServerTrust.cer %{buildroot}/usr/share/push/PushServerTrust.cer
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
ln -s /etc/init.d/pushd /etc/rc.d/rc3.d/S90pushd
ln -s /etc/init.d/pushd /etc/rc.d/rc5.d/S90pushd


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

vconftool unset file/private/push-bin/devtk

%post -n libpush
/sbin/ldconfig

%postun -p /sbin/ldconfig


%files -n libpush
%attr(644,-,-) %{_libdir}/libpush.so.*

%files -n libpush-devel
%{_includedir}/*.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libpush.so

%files bin
%{_bindir}/pushd
/etc/init.d/pushd
/usr/share/push/*.cer

%files tool
%{_bindir}/push_tool
