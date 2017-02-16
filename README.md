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

1. Run ansible to copy the configs to the hub.

        ansible-playbook site.yml

[hass]:https://home-assistant.io/
[hassbian]:https://home-assistant.io/getting-started/hassbian-installation/
[hassbian-scripts]:https://github.com/home-assistant/hassbian-scripts
