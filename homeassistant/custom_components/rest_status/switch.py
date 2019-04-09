import asyncio
import logging

import aiohttp
import async_timeout
import voluptuous as vol

from homeassistant.components.switch.rest import (RestSwitch, PLATFORM_SCHEMA)
from homeassistant.const import (
    CONF_HEADERS, CONF_NAME, CONF_RESOURCE, CONF_TIMEOUT, CONF_METHOD,
    CONF_USERNAME, CONF_PASSWORD, HTTP_OK)
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

CONF_BODY_OFF = 'body_off'
CONF_BODY_ON = 'body_on'
CONF_IS_ON_TEMPLATE = 'is_on_template'
CONF_SUCCESS = 'success_code'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_SUCCESS, default=HTTP_OK): cv.positive_int,
})


async def async_setup_platform(hass, config, async_add_entities,
                               discovery_info=None):
    """Set up the RESTful switch."""
    body_off = config.get(CONF_BODY_OFF)
    body_on = config.get(CONF_BODY_ON)
    is_on_template = config.get(CONF_IS_ON_TEMPLATE)
    success_code = config.get(CONF_SUCCESS)
    method = config.get(CONF_METHOD)
    headers = config.get(CONF_HEADERS)
    name = config.get(CONF_NAME)
    username = config.get(CONF_USERNAME)
    password = config.get(CONF_PASSWORD)
    resource = config.get(CONF_RESOURCE)

    auth = None
    if username:
        auth = aiohttp.BasicAuth(username, password=password)

    if is_on_template is not None:
        is_on_template.hass = hass
    if body_on is not None:
        body_on.hass = hass
    if body_off is not None:
        body_off.hass = hass
    timeout = config.get(CONF_TIMEOUT)

    try:
        switch = RestStatusSwitch(name, resource, method, headers, auth, body_on,
                            body_off, is_on_template, timeout, success_code)

        async_add_entities([switch])
    except (TypeError, ValueError) as e:
        _LOGGER.error(e)
        _LOGGER.error("Missing resource or schema in configuration. "
                      "Add http:// or https:// to your URL")
    except (asyncio.TimeoutError, aiohttp.ClientError):
        _LOGGER.error("No route to resource/endpoint: %s", resource)


class RestStatusSwitch(RestSwitch):
    """Representation of a switch that can be toggled using REST."""

    def __init__(self, name, resource, method, headers, auth, body_on,
                 body_off, is_on_template, timeout, success_code):
        """Initialize the REST switch."""
        self._state = None
        self._name = name
        self._resource = resource
        self._method = method
        self._headers = headers
        self._auth = auth
        self._body_on = body_on
        self._body_off = body_off
        self._is_on_template = is_on_template
        self._timeout = timeout
        self._success_code = success_code
        self._verify_ssl = False

    async def async_turn_on(self, **kwargs):
        """Turn the device on."""
        body_on_t = self._body_on.async_render()

        try:
            req = await self.set_device_state(body_on_t)

            if req.status == self._success_code:
                self._state = True
            else:
                _LOGGER.error(
                    "Can't turn on %s. Is resource/endpoint offline?",
                    self._resource)
        except (asyncio.TimeoutError, aiohttp.ClientError):
            _LOGGER.error("Error while switching on %s", self._resource)

    async def async_turn_off(self, **kwargs):
        """Turn the device off."""
        body_off_t = self._body_off.async_render()

        try:
            req = await self.set_device_state(body_off_t)
            if req.status == self._success_code:
                self._state = False
            else:
                _LOGGER.error(
                    "Can't turn off %s. Is resource/endpoint offline?",
                    self._resource)
        except (asyncio.TimeoutError, aiohttp.ClientError):
            _LOGGER.error("Error while switching off %s", self._resource)
