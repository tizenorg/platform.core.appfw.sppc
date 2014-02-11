#!/bin/sh

source /etc/tizen-platform.conf

mkdir -p $TZ_SYS_DB
sqlite3 $TZ_SYS_DB/.push.db "PRAGMA journal_mode = PERSIST; create table a(a); drop table a;" > /dev/null
chown root:$TZ_SYS_USER_GROUP $TZ_SYS_DB/.push.db
chown root:$TZ_SYS_USER_GROUP $TZ_SYS_DB/.push.db-journal
chmod 660 $TZ_SYS_DB/.push.db
chmod 660 $TZ_SYS_DB/.push.db-journal

#chsmack -a 'push-service::db' /opt/dbspace/.push.db
#chsmack -a 'push-service::db' /opt/dbspace/.push.db-journal

users_gid=$(getent group $TZ_SYS_USER_GROUP | cut -f3 -d':')

_VER="1"
_DEV_TYPE="00000000"
_DEV_INFO="device.model=ssltest"
_IP_PV="gld.push.samsungosp.com"
_PORT_PV=5223
#ping interval {120,240,480,960,1920}
_PING_INT=480
_GRP="-g $users_gid"

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
