
"""
`mprls`
====================================================

MicroPython library to support Honeywell MPRLS digital pressure sensors

"""

import time
from machine import Pin

_MPRLS_DEFAULT_ADDR = const(0x18)

class MPRLS:
    """
    Driver base for the MPRLS pressure sensor

    :param machine.I2C i2c_bus: The I2C bus the MPRLS is connected to
    :param int addr: The I2C device address. Defaults to :const:`0x18`
    :param machine.Pin reset_pin: Optional Pin for hardware resetting
    :param machine.Pin eoc_pin: Optional Pin for getting End Of Conversion signal
    :param float psi_min: The minimum pressure in PSI, defaults to :const:`0`
    :param float psi_max: The maximum pressure in PSI, defaults to :const:`25`
    """

    def __init__(
        self,
        i2c_bus,
        *,
        addr=_MPRLS_DEFAULT_ADDR,
        reset_pin=None,
        eoc_pin=None,
        psi_min=0,
        psi_max=25
    ):
        self._i2c = i2c_bus
        self.address = addr
        self._buffer = bytearray(4)

        # Optional hardware reset pin
        if reset_pin is not None:
            reset_pin.init(Pin.OUT)
            reset_pin.value(1)
            reset_pin.value(0)
            time.sleep(0.01)
            reset_pin.value(1)
        time.sleep(0.005)  # Start up timing

        # Optional end-of-conversion pin
        self._eoc = eoc_pin
        if eoc_pin is not None:
            self._eoc.init(Pin.IN)

        if psi_min >= psi_max:
            raise ValueError("Min PSI must be < max!")
        self._psimax = psi_max
        self._psimin = psi_min

    @property
    def pressure(self):
        """The measured pressure, in hPa"""
        return self._read_data()

    def _read_data(self):
        """Read the status & 24-bit data reading"""
        self._buffer[0] = 0xAA
        self._buffer[1] = 0
        self._buffer[2] = 0
        self._i2c.writeto(self.address, self._buffer[0:3])
        while True:
            if self._eoc is not None:
                if self._eoc.value():
                    break
            temp = self._i2c.readfrom(self.address, 1)
            self._buffer[0] = temp[0]
            if not self._buffer[0] & 0x20:
                break
        temp = self._i2c.readfrom(self.address, 4)
        for i in range(4):
            self._buffer[i] = temp[i]
        if self._buffer[0] & 0x01:
            raise RuntimeError("Internal math saturation")
        # if self._buffer[0] & 0x04:
        #     pass
            # raise RuntimeError("Integrity failure")

        # All is good, calculate the PSI and convert to hPA
        raw_psi = (self._buffer[1] << 16) | (self._buffer[2] << 8) | self._buffer[3]
        # use the 10-90 calibration curve
        psi = (raw_psi - 0x19999A) * (self._psimax - self._psimin)
        psi /= 0xE66666 - 0x19999A
        psi += self._psimin
        # convert PSI to hPA
        return psi * 68.947572932

    @classmethod
    def create_instance(cls, i2c_bus, *, addr=_MPRLS_DEFAULT_ADDR, reset_pin=None, eoc_pin=None, psi_min=0, psi_max=25):
        """
        Factory method to create an instance of MPRLS. Returns False on failure.

        :param machine.I2C i2c_bus: The I2C bus the MPRLS is connected to
        :param int addr: The I2C device address. Defaults to :const:`0x18`
        :param machine.Pin reset_pin: Optional Pin for hardware resetting
        :param machine.Pin eoc_pin: Optional Pin for getting End Of Conversion signal
        :param float psi_min: The minimum pressure in PSI, defaults to :const:`0`
        :param float psi_max: The maximum pressure in PSI, defaults to :const:`25`
        """
        try:
            return cls(i2c_bus, addr=addr, reset_pin=reset_pin, eoc_pin=eoc_pin, psi_min=psi_min, psi_max=psi_max)
        except (OSError, RuntimeError) as e:
            if isinstance(e, OSError) and e.errno == 19:
                print(f"Error, could not find MPRLS sensor on {i2c_bus}: {e}")
            else:
                print(e)
            return False
