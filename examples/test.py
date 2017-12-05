import busio
import adafruit_apds9960 as apds9960
from board import SCL, SDA, A1
import digitalio

int_pin = digitalio.DigitalInOut(A1)

with busio.I2C(SCL, SDA) as i2c:

    apds = apds9960.APDS9960(i2c, interrupt_pin=int_pin)
    print(apds.UP)
    print(apds.DOWN)
    print(apds.RIGHT)
    print(apds.LEFT)
