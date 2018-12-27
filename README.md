# home

all my home automation configs, based on [home assistant][hass].

## setting up the hub

1. Install Ubuntu on something and specify that you want it to be a docker host during installation.
1. Edit `hosts.cfg` to target said machine.
1. On the machine, Create docker networks:

        sudo docker network create traefik_proxy
        docker network create \
            -d macvlan \
            --subnet=192.168.1.0/24 \
            --gateway=192.168.1.1 \
            -o parent=enp2s0 \
            mylan

1. Run ansible to copy the configs to the hub and install necessary software,
   including [homebridge][homebridge].

        ansible-playbook site.yml -l hub

## speaker nodes

One major goal for my home automation project was having music in more rooms in
my home. After thinking about Sonos and other more expensive solutions I decided
to go with an Airplay-based solution as I already have an Apple TV plugged into
a receiver in the Living Room. I also don't give a shit about streaming music
and would prefer to rely on my music library.

Also, I have other older stereo systems that I've accumulated over the years
that I'd like to integrate, including a Bose/Pioneer system older than me that
still sounds great. It would be a shame for these to be obsoleted by a system
with integrated speakers like a Sonos.

To add Airplay connectivity to these older systems I've purchased
[HiFiBerry][hifiberry] D/A converters and connected them to Raspberry PIs
running [shairport-sync][shairport]. Now I can stream music from any source on
my iPhone, iTunes or from music on my server running [forked-daapd][daapd].

To get this running:

1. Download and install [Raspbian lite][raspbian].
1. Run `sudo raspi-config` and enable SSH.
1. Set a hostname by editing `/etc/hostname`.
1. Run ansible to install shairport-sync.

        ansible-playbook site.yml -l speaker

## itunes/daapd server

The other component of the music solution is a Raspberry PI running
[forked-daapd][daapd] to serve music throughout the house. I have it connected
to a big harddrive and use a cron job to copy music from my FreeNAS server.
Originally I tried running forked-daapd in a jail on the server itself but it
appears mDNS/avahi doesn't work properly in a jail.

To install it I run:

    ansible-playbook site.yml -l itunes

Then ssh in and compile forked-daapd.

    cd forked-daapd
    autoreconf -i
    ./configure --prefix=/usr --sysconfdir=/etc --localstatedir=/var --enable-itunes
    make
    sudo make install

[hass]:https://home-assistant.io/
[hassbian]:https://home-assistant.io/getting-started/hassbian-installation/
[hassbian-scripts]:https://github.com/home-assistant/hassbian-scripts
[homebridge]:https://github.com/nfarina/homebridge
[hifiberry]:https://www.hifiberry.com/
[shairport]:https://github.com/mikebrady/shairport-sync
[daapd]:https://github.com/ejurgensen/forked-daapd
[raspbian]:https://www.raspberrypi.org/downloads/raspbian/
