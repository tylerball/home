#!/bin/bash

if [ -n "$PUID" -a "$(id -u daapd)" != "$PUID" ]; then usermod -o -u "$PUID" daapd ; fi

mkdir -p /cache/forked-daapd
chown -R daapd /cache/forked-daapd
chmod -R u+rw /cache/forked-daapd

sed -i -e "s/admin_password = \"placeholder\"/admin_password = \"${ADMIN_PASSWORD:-}\"/" /etc/forked-daapd.conf
sed -i -e "s/password = \"placeholder\"/password = \"${LIBRARY_PASSWORD:-}\"/" /etc/forked-daapd.conf

[ -d "/var/run" ] && rm -rf /var/run/*
mkdir -p /var/run/dbus
/usr/bin/dbus-daemon --system
/usr/sbin/avahi-daemon --no-chroot -D
/usr/sbin/forked-daapd -f -c /etc/forked-daapd.conf
/usr/sbin/avahi-daemon -k
killall dbus-daemon
