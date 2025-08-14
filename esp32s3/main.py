import machine
import utime
import ujson
from lib import adafruit_MPRLS
from lib.tca9548a import PCA9546A

# Base I2C bus
i2c = machine.I2C(0, sda=machine.Pin(8), scl=machine.Pin(9))

# Init multiplexer
# mux = PCA9546A(i2c)

# Create sensor instances using channel 0 and 1
mprls0 = adafruit_MPRLS.MPRLS.create_instance(i2c)
# mprls1 = adafruit_MPRLS.MPRLS.create_instance(mux[3])

while True:
    try:
        p0 = mprls0.pressure
        # p1 = mprls1.pressure

        payload = {
            "CH0": p0,
            # "CH1": p1,
        }
        print(ujson.dumps(payload))

    except Exception as e:
        print(ujson.dumps({"error": str(e)}))
    utime.sleep(1)
