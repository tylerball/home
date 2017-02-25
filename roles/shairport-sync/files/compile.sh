#!/bin/bash
set -e
set -o pipefail

cd /usr/src/shairport-sync
autoreconf -i -f
./configure --sysconfdir=/etc --with-alsa --with-avahi --with-ssl=openssl --with-metadata --with-systemd
make
make install

