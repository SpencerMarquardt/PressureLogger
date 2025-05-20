import machine
from lib import adafruit_MPRLS
import utime

i2c = machine.I2C(0, sda=machine.Pin(41), scl=machine.Pin(40))
print(f'\n\ni2c devices on bus: {i2c.scan()}\n\n')

mprls = adafruit_MPRLS.MPRLS.create_instance(i2c)

while True:
    p = mprls.pressure
    print(f'Pressure: {p} mbar')
    utime.sleep_ms(1000)