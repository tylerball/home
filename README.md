# home

all my home automation configs, based on [home assistant][hass].

## setting up the hub

1. Download and install [Hassbian][hassbian]. I run it on a Raspberry Pi 3.
1. Clone a fresh copy of [hassbian-scripts][hassbian-scripts] and run the
   scripts for installing homeassistant and zwave.

        ./hassbian-scripts/install_homeassitant.sh
        ./hassbian-scripts/install_openzwave.sh

1. Be sure to set a NetworkKey in
   `/srv/homeassistant/src/python-openzwave/openzwave/config/options.xml`, which
   you can generate with:

        cat /dev/urandom | tr -dc '0-9A-F' | fold -w 32 | head -n 1 | sed -e 's/\(..\)/0x\1, /g'

1. Install node

        curl -sL https://deb.nodesource.com/setup_7.x | sudo -E bash -
        sudo apt-get install node

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

[hass]:https://home-assistant.io/
[hassbian]:https://home-assistant.io/getting-started/hassbian-installation/
[hassbian-scripts]:https://github.com/home-assistant/hassbian-scripts
[homebridge]:https://github.com/nfarina/homebridge
[hifiberry]:https://www.hifiberry.com/
[shairport]:https://github.com/mikebrady/shairport-sync
[daapd]:https://github.com/ejurgensen/forked-daapd
[raspbian]:https://www.raspberrypi.org/downloads/raspbian/
