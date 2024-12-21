"""binance_ticker_sensor"""

import logging
from datetime import timedelta
import decimal
import requests
from requests import RequestException
from homeassistant.helpers.entity import Entity
from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.const import (
    STATE_UNKNOWN
)


logger = logging.getLogger(__name__)



class BinanceTickerSensor(Entity):
    def __init__(self, symbol, decimals, update_interval):
        self._attr_device_class = SensorDeviceClass.MONETARY
        self._name = "Binance Ticker "+symbol.upper()
        self._symbol = symbol
        self._decimals = decimals
        self._update_interval = update_interval
        self._state = STATE_UNKNOWN
        self._data = {}

    @property
    def name(self):
        return self._name

    @property
    def symbol(self):
        return self._symbol

    @property
    def decimals(self):
        return self._decimals

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return self._data

    async def async_added_to_hass(self):
        self.hass.helpers.event.async_track_time_interval(
            self.update, timedelta(seconds=self._update_interval)
        )

    # For usage with a AWTRIX clock
    def pretty_format_number(value: float) -> str:
        """
        Format a number to exactly 6 characters according to its magnitude.
        Examples:
            0 → "0.0000"
            0.005432 → "0.0054"
            0.054321 → "0.0543"
            0.543210 → "0.5432"
            5.43210 → "5.4321"
            54.3210 → "54.321"
            543.210 → "543.21"
            5432.10 → "5.43k "  # Note the space to make it 6 chars
            54321.0 → "54.3k "  # Note the space to make it 6 chars
        Args:
            value (float): The number to format
        Returns:
            str: Formatted number string with exactly 6 characters
        """
        if value == 0:
            return "0.0000"
        elif value < 0.01:
            return f"{value:.4f}"
        elif value < 0.1:
            return f"{value:.4f}"
        elif value < 1:
            return f"{value:.4f}"
        elif value < 10:
            return f"{value:.4f}"
        elif value < 100:
            return f"{value:.3f}"
        elif value < 1000:
            return f"{value:.2f}"
        elif value < 10000:
            return f"{value/1000:.2f}k"
        else:
            return f"{value/1000:.1f}k"

    def update(self, *args):
        logger.debug("Updating %s - args", self._name, args)
        
        url = "https://api.binance.com/api/v3/ticker?symbol="+self._symbol
        
        try:
            response = requests.request("GET", url, headers={}, data={}, timeout=5)
            
            response.raise_for_status()  # This handles non-200 status codes

            data = response.json()

            lastPrice = round(decimal.Decimal(data['lastPrice']), self._decimals)
            print(lastPrice)
            formatted_lastPrice = self.pretty_format_number(lastPrice)
            print(formatted_lastPrice)
            data["formatted_lastPrice"] = formatted_lastPrice
            print(data)

            self._data = data
            self._state = lastPrice
            
        except RequestException as request_exception:
            logger.error("Error updating %s - %s", self._name, request_exception)