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
`adafruit_APDS9960`
====================================================

TODO(description)

* Author(s): Michael McWethy
"""
class APDS9960:

    UP = const(1)
    DOWN = const(2)
    RIGHT = const(3)
    LEFT = const(4)

    def __init__(self, i2c, interrupt_pin=None):
        self._i2c = i2c
        self._interrupt_pin = interrupt_pin
        self.enable_color = False
        self.enable_proximity = False
        self.enable_gesture = True


    ## GESTURE DETECTION
    @property
    def enable_gesture(self):
        return self._enable_gesture

    @enable_gesture.setter
    def enable_gesture(self, enable_flag):
        self._enable_gesture = enable_flag

    def gesture(self):
        pass

    ## COLOR DETECTION
    @property
    def enable_color(self):
        return self._enable_color

    @enable_color.setter
    def enable_color(self, enable_flag):
        self._enable_color = enable_flag

    @property
    def color_data_ready(self):
        return True

    @property
    def color_data(self):
        return [None, None, None, None]

    ### PROXIMITY
    @property
    def enable_proximity(self):
        return self._enable_proximity

    @enable_proximity.setter
    def enable_proximity(self, enable_flag):
        self._enable_proximity = enable_flag

    @property
    def proximity_interrupt_threshold(self):
        return self._proximity_interrupt_threshold

    @proximity_interrupt_threshold.setter
    def proximity_interrupt_threshold(self, setting_tuple):
        self._proximity_interrupt_threshold = setting_tuple

    @property
    def enable_proximity_interrupt(self):
        return _enable_proximity_interrupt

    @enable_proximity_interrupt.setter
    def enable_proximity_interrupt(self, enable_flag):
        self._enable_proximity_interrupt = enable_flag

    def proximity(self):
        return None

    def clear_interrupt(self):
        pass
