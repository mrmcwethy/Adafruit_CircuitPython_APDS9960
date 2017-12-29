# The MIT License (MIT)
#
# Copyright (c) 2017 Michael McWethy for Adafruit Inc
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`APDS9960`
====================================================

Driver class for the APDS9960 board.  Supports gesture, proximity, and color
detection.

* Author(s): Michael McWethy
"""
import time
import digitalio
from adafruit_register.i2c_bits import RWBits
from adafruit_register.i2c_bit import RWBit
from adafruit_bus_device.i2c_device import I2CDevice
from micropython import const


# ADDRESS_DEF = const(0x39)
# INTEGRATION_TIME_DEF = const(0x01)
# GAIN_DEF = const(0x01)

#pylint: disable-msg=bad-whitespace
#APDS9960_RAM        = const(0x00)
APDS9960_ENABLE     = const(0x80)
APDS9960_ATIME      = const(0x81)
#APDS9960_WTIME      = const(0x83)
#APDS9960_AILTIL     = const(0x84)
# APDS9960_AILTH      = const(0x85)
# APDS9960_AIHTL      = const(0x86)
# APDS9960_AIHTH      = const(0x87)
APDS9960_PILT       = const(0x89)
APDS9960_PIHT       = const(0x8B)
APDS9960_PERS       = const(0x8C)
# APDS9960_CONFIG1    = const(0x8D)
# APDS9960_PPULSE     = const(0x8E)
APDS9960_CONTROL    = const(0x8F)
# APDS9960_CONFIG2    = const(0x90)
APDS9960_ID         = const(0x92)
APDS9960_STATUS     = const(0x93)
APDS9960_CDATAL     = const(0x94)
# APDS9960_CDATAH     = const(0x95)
# APDS9960_RDATAL     = const(0x96)
# APDS9960_RDATAH     = const(0x97)
# APDS9960_GDATAL     = const(0x98)
# APDS9960_GDATAH     = const(0x99)
# APDS9960_BDATAL     = const(0x9A)
# APDS9960_BDATAH     = const(0x9B)
APDS9960_PDATA      = const(0x9C)
# APDS9960_POFFSET_UR = const(0x9D)
# APDS9960_POFFSET_DL = const(0x9E)
# APDS9960_CONFIG3    = const(0x9F)
APDS9960_GPENTH     = const(0xA0)
# APDS9960_GEXTH      = const(0xA1)
APDS9960_GCONF1     = const(0xA2)
APDS9960_GCONF2     = const(0xA3)
# APDS9960_GOFFSET_U  = const(0xA4)
# APDS9960_GOFFSET_D  = const(0xA5)
# APDS9960_GOFFSET_L  = const(0xA7)
# APDS9960_GOFFSET_R  = const(0xA9)
APDS9960_GPULSE     = const(0xA6)
APDS9960_GCONF3     = const(0xAA)
APDS9960_GCONF4     = const(0xAB)
# APDS9960_GFLVL      = const(0xAE)
APDS9960_GSTATUS    = const(0xAF)
# APDS9960_IFORCE     = const(0xE4)
# APDS9960_PICLEAR    = const(0xE5)
# APDS9960_CICLEAR    = const(0xE6)
APDS9960_AICLEAR    = const(0xE7)
APDS9960_GFIFO_U    = const(0xFC)
# APDS9960_GFIFO_D    = const(0xFD)
# APDS9960_GFIFO_L    = const(0xFE)
# APDS9960_GFIFO_R    = const(0xFF)
#pylint: enable-msg=bad-whitespace


#pylint: disable-msg=too-many-instance-attributes
class APDS9960:
    """
    APDS9900 provide basic driver services for the ASDS9960 breakout board
    """

    _enable = RWBit(APDS9960_ENABLE, 0)
    _color_enable = RWBit(APDS9960_ENABLE, 1)
    _proximity_enable = RWBit(APDS9960_ENABLE, 2)
    _gesture_enable = RWBit(APDS9960_ENABLE, 6)
    _gesture_fifo_threshold = RWBits(2, APDS9960_GCONF1, 6)
    _gesture_gain = RWBits(2, APDS9960_GCONF2, 5)
    _color_gain = RWBits(2, APDS9960_CONTROL, 0)
    _gesture_valid = RWBit(APDS9960_GSTATUS, 0)
    _gesture_mode = RWBit(APDS9960_GCONF4, 0)
    _proximity_persistance = RWBits(4, APDS9960_PERS, 4)
    _proximity_enable_interrupt = RWBit(APDS9960_ENABLE, 5)

    def __init__(self,
                 i2c, *,
                 interrupt_pin=None,
                 address=0x39,
                 integration_time=0x01,
                 gain=0x01):

        self.i2c_device = I2CDevice(i2c, address)
        self._interrupt_pin = interrupt_pin
        if interrupt_pin:
            self._interrupt_pin.switch_to_input(pull=digitalio.Pull.UP)

        if self.read8(APDS9960_ID) != 0xAB:
            raise RuntimeError()

        self.enable_gesture = False
        self.enable_proximity = False
        self.enable_color = False
        self._enable_proximity_interrupt = False
        self.enable_color_interrupt = False
        self.proximity_interrupt = False
        self.clear_interrupt()

        self.enable = False
        time.sleep(0.010)
        self.enable = True
        time.sleep(0.010)

        self._color_gain = gain
        self.integration_time = integration_time
        self.gesture_dimensions = 0x00 # all
        self.gesture_fifo_threshold = 0x01 # fifo 4
        self.gesture_gain = 0x02 # gain 4
        self.gesture_proximity_threshold = 50
        self._reset_counts()

        # gesture pulse length=0x2 pulse count=0x3
        self.write8(APDS9960_GPULSE, (0x2 << 6) | 0x3)


    ## BOARD
    @property
    def enable(self):
        """Set or get board enable.  True to enable, False to disable"""
        return self._enable

    @enable.setter
    def enable(self, enable_flag):
        self._enable = enable_flag

    def _reset_counts(self):
        """Gesture detection internal counts"""
        self._saw_down_start = 0
        self._saw_up_start = 0
        self._saw_left_start = 0
        self._saw_right_start = 0

    ## GESTURE DETECTION
    @property
    def enable_gesture(self):
        """Set ot get gesture detection enable flag
            Note that when disabled, the gesture mode is turned off"""
        return self._gesture_mode, self._gesture_enable

    @enable_gesture.setter
    def enable_gesture(self, enable_flag):
        if not enable_flag:
            self._gesture_mode = False
        self._gesture_enable = enable_flag

    def gesture(self): #pylint: disable-msg=too-many-branches
        """Return a gesture code if detected. =0 if no gesture
        =1 if an UP, =2 if a DOWN, =3 if an LEFT, =4 if a RIGHT
        """
        # buffer to read of contents of device FIFO buffer
        buffer = bytearray(129)
        buffer[0] = APDS9960_GFIFO_U
        if not self._gesture_valid:
            return 0

        time_mark = 0
        gesture_received = 0
        while True:

            up_down_diff = 0
            left_right_diff = 0
            gesture_received = 0

            time.sleep(0.030) # 30 ms

            with self.i2c_device as i2c:
                i2c.write(buffer, end=1, stop=False)
                i2c.readinto(buffer, start=1)
            upp, down, left, right = buffer[1:5]

            if abs(upp - down) > 13:
                up_down_diff = upp - down

            if abs(left - right) > 13:
                left_right_diff = left - right

            if up_down_diff != 0:
                if up_down_diff < 0:
                    # either leading edge of down movement
                    # or trailing edge of up movement
                    if self._saw_up_start:
                        gesture_received = 0x01 # up
                    else:
                        self._saw_down_start += 1
                elif up_down_diff > 0:
                    # either leading edge of up movement
                    # or trailing edge of down movement
                    if self._saw_down_start:
                        gesture_received = 0x02 # down
                    else:
                        self._saw_up_start += 1

            if left_right_diff != 0:
                if left_right_diff < 0:
                    # either leading edge of right movement
                    # trailing edge of left movement
                    if self._saw_left_start:
                        gesture_received = 0x03 # left
                    else:
                        self._saw_right_start += 1
                elif left_right_diff > 0:
                    # either leading edge of left movement
                    # trailing edge of right movement
                    if self._saw_right_start:
                        gesture_received = 0x04 #right
                    else:
                        self._saw_left_start += 1

            # saw a leading or trailing edge; start timer
            if up_down_diff != 0 or left_right_diff != 0:
                time_mark = time.monotonic()

            # finished when a gesture is detected or ran out of time (300ms)
            if gesture_received or time.monotonic() - time_mark > 0.300:
                self._reset_counts()
                break

        return gesture_received


    @property
    def gesture_dimensions(self):
        """Set of get gesture dimension value: range 0-3"""
        return self.read8(APDS9960_GCONF3)

    @gesture_dimensions.setter
    def gesture_dimensions(self, dims):
        self.write8(APDS9960_GCONF3, dims & 0x03)

    @property
    def gesture_fifo_threshold(self):
        """Set or get gesture fifo threshold value: range 0-3"""
        return self._gesture_fifo_threshold

    @gesture_fifo_threshold.setter
    def gesture_fifo_threshold(self, thresh):
        self._gesture_fifo_threshold = thresh & 0x03

    @property
    def gesture_gain(self):
        """Set or get gesture gain value: range 0-3"""
        return self._gesture_gain

    @gesture_gain.setter
    def gesture_gain(self, gain):
        self._gesture_gain = gain


    ## COLOR DETECTION
    @property
    def enable_color(self):
        """Set of get color detection enable flag.
            True when color detection is enabled, else False"""
        return self._color_enable

    @enable_color.setter
    def enable_color(self, enable_flag):
        self._color_enable = enable_flag

    @property
    def color_data_ready(self):
        """Get color data ready flag.  zero if not ready, 1 is ready"""
        return self.read8(APDS9960_STATUS) & 0x01

    @property
    def color_data(self):
        """Returns tuple containing r, g, b, c values"""
        return self._color_data16(APDS9960_CDATAL + 2), \
               self._color_data16(APDS9960_CDATAL + 4), \
               self._color_data16(APDS9960_CDATAL + 6), \
               self._color_data16(APDS9960_CDATAL)
    ### PROXIMITY
    @property
    def enable_proximity(self):
        """Returns or sets the enablement of proximity mode"""
        return self._proximity_enable

    @enable_proximity.setter
    def enable_proximity(self, enable_flag):
        self._proximity_enable = enable_flag

    @property
    def proximity_interrupt_threshold(self):
        """Returns a tuple containing low and high threshold
        followed by the proximity interrupt persistance.
        Set the proximity interrupt threshold values using a tuple of zero to
        three values: low threshold, high threshold, persistance.
        persistance defaults to 4 if not provided"""
        return self.read8(APDS9960_PILT), \
               self.read8(APDS9960_PIHT), \
               self._proximity_persistance

    @proximity_interrupt_threshold.setter
    def proximity_interrupt_threshold(self, setting_tuple):
        if setting_tuple:
            self.write8(APDS9960_PILT, setting_tuple[0])
        if len(setting_tuple) > 1:
            self.write8(APDS9960_PIHT, setting_tuple[1])
        persist = 4 # default 4
        if len(setting_tuple) > 2:
            persist = min(setting_tuple[2], 7)
        self._proximity_persistance = persist


    @property
    def enable_proximity_interrupt(self):
        """Set or get proximity interrupt enable flag.  True if enabled,
            False to disable"""
        return self._proximity_enable_interrupt

    @enable_proximity_interrupt.setter
    def enable_proximity_interrupt(self, enable_flag):
        self._proximity_enable_interrupt = enable_flag

    @property
    def gesture_proximity_threshold(self):
        """Set or get proximity threshold value: range 0-255"""
        return self.read8(APDS9960_GPENTH)

    @gesture_proximity_threshold.setter
    def gesture_proximity_threshold(self, thresh):
        self.write8(APDS9960_GPENTH, thresh & 0xff)

    def proximity(self):
        """Set or get proximity value: range 0-255"""
        return self.read8(APDS9960_PDATA)

    def clear_interrupt(self):
        """Clear all interrupts"""
        self.writecmdonly(APDS9960_AICLEAR)

    @property
    def integration_time(self):
        """Set or get the proximity integration time: range 0-255"""
        return self.read8(APDS9960_ATIME)

    @integration_time.setter
    def integration_time(self, int_time):
        self.write8(APDS9960_ATIME, int_time & 0xff)

    # method for reading and writing to I2C
    def write8(self, command, abyte):
        """Write a command and 1 byte of data to the I2C device"""
        buf = bytearray(2)
        buf[0] = command
        buf[1] = abyte
        with self.i2c_device as i2c:
            i2c.write(buf)

    def writecmdonly(self, command):
        """Writes a command and 0 bytes of data to the I2C device"""
        buf = bytearray(1)
        buf[0] = command
        with self.i2c_device as i2c:
            i2c.write(buf)

    def read8(self, command):
        """Sends a command and reads 1 byte of data from the I2C device"""
        buf = bytearray(1)
        buf[0] = command
        with self.i2c_device as i2c:
            i2c.write(buf)
            i2c.readinto(buf)
        return buf[0]

    def _color_data16(self, command):
        """Sends a command and reads 2 byte of data from the I2C device
            The returned data is low byte first followed by high byte"""
        buf = bytearray(2)
        buf[0] = command
        with self.i2c_device as i2c:
            i2c.write(buf, end=1, stop=False)
            i2c.readinto(buf)
        return buf[1] << 8 | buf[0]
