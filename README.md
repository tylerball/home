# home

My home automation configuration.

## Home Assistant

[Home Assistant][hass] is the centre of my automation system. Here are some of the things it does:

- control lights: [Ikea Tradfri][tradfri] and [Lutron Caseta][lutron]
- control music: [See below](#music)
- display [TTC][ttc] bus arrival times via the [NextBus API][nextbus] and a [custom component][https://github.com/tylerball/home/blob/master/homeassistant/custom_components/sensor/ttc.py]
- and much more

## setting up the hub

1. Install Ubuntu on something and specify that you want it to be a docker host during installation.
1. Clone this repo and `cd` into it.
1. Fill in secrets in `homeassistant/secrets.yaml`, `traefik.env`, `librespot.env` (more automation for this later)
1. Run docker-compose.

        sudo docker-compose up -d

## music

More info soon.

[hass]:https://home-assistant.io/
[tradfri]:https://www.home-assistant.io/components/tradfri/
[lutron]:https://www.home-assistant.io/components/lutron_caseta/
[ttc]:http://www.ttc.ca
[nextbus]:https://gist.github.com/grantland/7cf4097dd9cdf0dfed14
