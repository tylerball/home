import requests
from datetime import timedelta
from homeassistant.const import ATTR_TIME
from homeassistant.helpers.entity import Entity

PREDICTIONS_URL = 'http://webservices.nextbus.com/service/publicJSONFeed'

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Setup the sensor platform."""
    add_entities([TTCSensor(config.get('route'), config.get('tag'))])

class TTCSensor(Entity):
    """Representation of a Sensor."""

    def __init__(self, route, tag):
        """Initialize the sensor."""
        self._route = route
        self._tag = tag
        self._state = None
        self._attributes = {}

    @property
    def unique_id(self):
        """Return unique ID of entity."""
        return 'ttc-{}-{}'.format(self._route, self._tag)

    @property
    def name(self):
        """Return the name of the sensor."""
        if 'routeTitle' in self._attributes:
            return self._attributes['routeTitle']
        else:
            return 'TTC {}'.format(self._route)

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return ATTR_TIME

    @property
    def device_state_attributes(self):
        """Show Device Attributes."""
        return self._attributes

    def update(self):
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        payload = {'command':'predictions', 'a':'ttc', 'r': self._route, 's': self._tag}
        r = requests.get(PREDICTIONS_URL, params=payload)
        resp = r.json()['predictions']
        self._attributes = resp
        if 'dirTitleBecauseNoPredictions' in resp:
            self._state = False
        else:
            prediction = resp['direction']['prediction']
            if isinstance(prediction, list):
                state = prediction[0]
            else:
                state = prediction
            self._state = timedelta(seconds=int(state['seconds']))
