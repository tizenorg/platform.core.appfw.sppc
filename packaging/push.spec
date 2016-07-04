%global _support_weblog 0

Name:       push
Summary:    Push services and client library
Version:    0.4.39
Release:    1
Group:      Application Framework/Service
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1:    pushd.service
Requires(post): /sbin/ldconfig
Requires(post): /usr/bin/sqlite3
Requires(postun): /sbin/ldconfig

%if %{_support_weblog}
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(json-glib-1.0)
%endif

%description
Push services and client library.

%package -n libpush
Summary:    Push service client library
Group:      Application Framework/Libraries
Requires:   %{name}-bin = %{version}-%{release}
Provides:   libpush.so.0

%description -n libpush
Push service client library

%package -n libpush-devel
Summary:    Push service client library (DEV)
Group:      Development/Libraries
Requires:   libpush = %{version}-%{release}
Requires:   capi-appfw-application-devel

%description -n libpush-devel
Push service client library (DEV)

%package bin
Summary:    Push service daemon
Group:      Application Framework/Service
Requires(post): telephony-daemon

%description bin
Push service daemon

%package tool
Summary:    Push service tool
Group:      Development/Tools
Requires:   libpush = %{version}-%{release}
Requires:   %{name}-bin = %{version}-%{release}

%description tool
Push service tool

%prep
%setup -q

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_unitdir_user}/default.target.wants
install -m 0644 %{SOURCE1} %{buildroot}%{_unitdir_user}/pushd.service
ln -s ../pushd.service %{buildroot}%{_unitdir_user}/default.target.wants/pushd.service

mkdir -p %{buildroot}/usr/share/license
cp -f LICENSE %{buildroot}/usr/share/license/%{name}

%if %{_support_weblog}
cp -a share/push/push_sslkey.pem %{buildroot}/usr/share/push/
cp -a share/push/prd-dl-key.pem %{buildroot}/usr/share/push/
%endif

mkdir -p %{buildroot}%{_includedir}
cp -a include/push-service.h %{buildroot}%{_includedir}
cp -a include/push.h %{buildroot}%{_includedir}
%if %{_support_weblog}
	include/pushlog.h %{buildroot}%{_includedir}
%endif

mkdir -p %{buildroot}%{_libdir}/pkgconfig
cp -a push.pc %{buildroot}%{_libdir}/pkgconfig/

mkdir -p %{buildroot}/usr/share/push/
mkdir -p %{buildroot}%{_bindir}

%ifarch %{arm}

#libpush
cp -a arm/lib/libpush.so.* %{buildroot}%{_libdir}
#libpus-devel
cp -a arm/lib/libpush.so %{buildroot}%{_libdir}
#push-bin
cp -a arm/bin/pushd %{buildroot}%{_bindir}
cp -a arm/bin/push_tool %{buildroot}%{_bindir}
cp -a arm/share/push/*.cer %{buildroot}/usr/share/push/
%if %{_support_weblog}
	arm/bin/pushlog_tool
%endif

%if "%{profile}" == "tv"
#libpush
cp -a arm_tv/lib/libpush.so.* %{buildroot}%{_libdir}
#libpus-devel
cp -a arm_tv/lib/libpush.so %{buildroot}%{_libdir}
#push-bin
cp -a arm_tv/bin/pushd %{buildroot}%{_bindir}
cp -a arm_tv/bin/push_tool %{buildroot}%{_bindir}
cp -a arm_tv/share/push/*.cer %{buildroot}/usr/share/push/
%if %{_support_weblog}
	arm_tv/bin/pushlog_tool
%endif
%endif

%if "%{profile}" == "wearable"
#libpush
cp -a arm_wearable/lib/libpush.so.* %{buildroot}%{_libdir}
#libpus-devel
cp -a arm_wearable/lib/libpush.so %{buildroot}%{_libdir}
#push-bin
cp -a arm_wearable/bin/pushd %{buildroot}%{_bindir}
cp -a arm_wearable/bin/push_tool %{buildroot}%{_bindir}
cp -a arm_wearable/share/push/*.cer %{buildroot}/usr/share/push/
%if %{_support_weblog}
	arm_wearable/bin/pushlog_tool
%endif
%endif
%endif


%ifarch aarch64
#libpush
cp -a aarch64/lib64/libpush.so.* %{buildroot}%{_libdir}
#libpush-devel
cp -a aarch64/lib64/libpush.so %{buildroot}%{_libdir}
#push-bin
cp -a aarch64/bin/pushd %{buildroot}%{_bindir}
cp -a aarch64/bin/push_tool %{buildroot}%{_bindir}
cp -a aarch64/share/push/*.cer %{buildroot}/usr/share/push/
%if %{_support_weblog}
	aarch64/bin/pushlog_tool
%endif
%endif


%ifarch %{ix86}

#libpush
cp -a x86/lib/libpush.so.* %{buildroot}%{_libdir}
#libpus-devel
cp -a x86/lib/libpush.so %{buildroot}%{_libdir}
#push-bin
cp -a x86/bin/pushd %{buildroot}%{_bindir}
cp -a x86/bin/push_tool %{buildroot}%{_bindir}
cp -a x86/share/push/*.cer %{buildroot}/usr/share/push/
%if %{_support_weblog}
	x86/bin/pushlog_tool
%endif

%if "%{profile}" == "tv"
#libpush
cp -a x86_tv/lib/libpush.so.* %{buildroot}%{_libdir}
#libpus-devel
cp -a x86_tv/lib/libpush.so %{buildroot}%{_libdir}
#push-bin
cp -a x86_tv/bin/pushd %{buildroot}%{_bindir}
cp -a x86_tv/bin/push_tool %{buildroot}%{_bindir}
cp -a x86_tv/share/push/*.cer %{buildroot}/usr/share/push/
%if %{_support_weblog}
	x86_tv/bin/pushlog_tool
%endif
%endif

%if "%{profile}" == "wearable"
#libpush
cp -a x86_wearable/lib/libpush.so.* %{buildroot}%{_libdir}
#libpus-devel
cp -a x86_wearable/lib/libpush.so %{buildroot}%{_libdir}
#push-bin
cp -a x86_wearable/bin/pushd %{buildroot}%{_bindir}
cp -a x86_wearable/bin/push_tool %{buildroot}%{_bindir}
cp -a x86_wearable/share/push/*.cer %{buildroot}/usr/share/push/
%if %{_support_weblog}
	x86_wearable/bin/pushlog_tool
%endif
%endif

%endif


%ifarch x86_64
#libpush
cp -a x86_64/lib64/libpush.so.* %{buildroot}%{_libdir}
#libpus-devel
cp -a x86_64/lib64/libpush.so %{buildroot}%{_libdir}
#push-bin
cp -a x86_64/bin/pushd %{buildroot}%{_bindir}
cp -a x86_64/bin/push_tool %{buildroot}%{_bindir}
cp -a x86_64/share/push/*.cer %{buildroot}/usr/share/push/
%if %{_support_weblog}
	x86_64/bin/pushlog_tool
%endif
%endif


%post bin
#mkdir -p /usr/dbspace
#sqlite3 /usr/dbspace/.push.db "PRAGMA journal_mode = PERSIST; create table a(a); drop table a;" > /dev/null
#chown system:system /usr/dbspace/.push.db
#chown system:system /usr/dbspace/.push.db-journal
#chmod 660 /usr/dbspace/.push.db
#chmod 660 /usr/dbspace/.push.db-journal

%post -n libpush
/sbin/ldconfig

%postun -n libpush -p /sbin/ldconfig

%files -n libpush
%manifest libpush.manifest
%attr(644,system,system)%{_libdir}/libpush.so.*

%files -n libpush-devel
%{_includedir}/*.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libpush.so

%files bin
%manifest push-bin.manifest
%{_bindir}/pushd
%attr(644,system,system)/usr/share/push/*.cer
%attr(644,system,system)/usr/share/license/%{name}

# This is a certificate file to access to logging server by HTTPS.
%if %{_support_weblog}
%attr(644,system,system)/usr/share/push/push_sslkey.pem
%attr(644,system,system)/usr/share/push/prd-dl-key.pem
%endif

%{_unitdir_user}/pushd.service
%{_unitdir_user}/default.target.wants/pushd.service

%files tool
%manifest push-tool.manifest
%{_bindir}/push_tool

%if %{_support_weblog}
	%{_bindir}/pushlog_tool
%endif

%changelog
* Sat Nov 3 2012 Jooseok Park <jooseok.park@samsung.com> - 0.2.26
- Prevent bug fixed(out-of bounds read, dead code,..)
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

