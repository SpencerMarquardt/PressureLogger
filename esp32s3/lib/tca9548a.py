# SPDX-FileCopyrightText: 2018 Carter Nelson for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
tca9548a.py

Adapted for MicroPython from original CircuitPython driver.
Supports TCA9548A and PCA9546A I2C multiplexers.
"""

_DEFAULT_ADDRESS = 0x70

class TCA9548AChannel:
    """I2C channel proxy for TCA9548A multiplexer."""

    def __init__(self, tca, channel):
        self.tca = tca
        self.channel_switch = bytearray([1 << channel])

    def _select_channel(self):
        self.tca.i2c.writeto(self.tca.address, self.channel_switch)

    def readfrom(self, address, nbytes, *args, **kwargs):
        self._select_channel()
        return self.tca.i2c.readfrom(address, nbytes, *args, **kwargs)

    def readfrom_into(self, address, buffer, *args, **kwargs):
        self._select_channel()
        return self.tca.i2c.readfrom_into(address, buffer, *args, **kwargs)

    def writeto(self, address, buffer, *args, **kwargs):
        self._select_channel()
        return self.tca.i2c.writeto(address, buffer, *args, **kwargs)

    def writeto_then_readfrom(self, address, buffer_out, buffer_in, *args, **kwargs):
        self._select_channel()
        self.tca.i2c.writeto(address, buffer_out, *args, **kwargs)
        return self.tca.i2c.readfrom_into(address, buffer_in, *args, **kwargs)

    def scan(self):
        self._select_channel()
        return self.tca.i2c.scan()


class TCA9548A:
    """Main controller for TCA9548A 8-channel multiplexer."""

    def __init__(self, i2c, address=_DEFAULT_ADDRESS):
        self.i2c = i2c
        self.address = address
        self.channels = [None] * 8

    def __len__(self):
        return 8

    def __getitem__(self, channel):
        if not 0 <= channel <= 7:
            raise IndexError("Channel must be 0-7.")
        if self.channels[channel] is None:
            self.channels[channel] = TCA9548AChannel(self, channel)
        return self.channels[channel]


class PCA9546A:
    """Main controller for PCA9546A 4-channel multiplexer."""

    def __init__(self, i2c, address=_DEFAULT_ADDRESS):
        self.i2c = i2c
        self.address = address
        self.channels = [None] * 4

    def __len__(self):
        return 4

    def __getitem__(self, channel):
        if not 0 <= channel <= 3:
            raise IndexError("Channel must be 0-3.")
        if self.channels[channel] is None:
            self.channels[channel] = TCA9548AChannel(self, channel)
        return self.channels[channel]
