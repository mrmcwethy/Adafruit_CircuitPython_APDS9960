
Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-APDS9960/badge/?version=latest

    :target: https://circuitpython.readthedocs.io/projects/apds/en/latest/

    :alt: Documentation Status

.. image :: https://img.shields.io/discord/327254708534116352.svg
    :target: https://discord.gg/nBQh6qu
    :alt: Discord

The APDS9960 is a specialize chip that detects hand gestures, proximity detection
and ambient light color over I2C. Its available on
`Adafruit as a breakout <https://www.adafruit.com/product/3595>`_.


Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://github.com/adafruit/Adafruit_CircuitPython_Bundle>`_.

Usage Example
=============

Hardware Set-up
---------------

Connect Vin to 3.3 V or 5 V power source, GND to ground, SCL and SDA to the appropriate pins.

Basics
------

Of course, you must import i2c bus device, board pins, and the library:

.. code:: python


  from board import SCL, SDA
  import adafruit_apds9960 as apds
  from adafruit_bus_device import I2CDevice

To set-up the device to gather data, initialize the I2CDevice using SCL
and SDA pins.   Then initialize the libary.  Optionally provide an interrupt
pin for proximity detection.

.. code:: python

  interrupt_pin = digitalio.DigitalInOutput(board.D2)
  i2c = I2CDevice(SCL, SDA, interrupt_pin=interrupt_pin)
  apds.APDS9960(i2c)

Gestures
--------

To get a gesture, see if a gesture is available first, then get the gesture Code

.. code:: python

  gesture = apds.gesture()
  if gesture == apds.UP:
    print("up")
  if gesture == apds.DOWN:
    print("down")
  if gesture == apds.RIGHT:
    print("right")
  if gesture == apds.LEFT:
    print("left")

Color Measurement
-----------------

To get a color measure, enable color measures, wait for color data,
then get the color data.

.. code:: python

  apds.enable_color = True

  while not apds.color_data_ready:
      time.sleep(0.005)

  r, g, b, c = apds.color_data
  print("r: {}, g: {}, b: {}, c: {}".format(r, g, b, c))

Proximity Detection
---------------------

To check for a object in proximity, see if a gesture is available first, then get the gesture Code

.. code:: python

  apds.enable_proximity = True

  # set the interrupt threshold to fire when proximity reading goes above 175
  apds.proximity_interrupt_threshold = (0, 175)

  # enable the proximity interrupt
  apds.enable_proximity_interrupt = True

  while not interrupt_pin.value:
    print(apds.proximity)

    # clear the interrupt
    apds.clear_interrupt()


API Reference
=============

.. toctree::
   :maxdepth: 2

   api

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_APDS9960/blob/master/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

Building locally
================

To build this library locally you'll need to install the
`circuitpython-travis-build-tools <https://github.com/adafruit/circuitpython-build-tools>`_ package.

.. code-block::shell

    python3 -m venv .env
    source .env/bin/activate
    pip install -r requirements.txt

Once installed, make sure you are in the virtual environment:

.. code-block::shell

    source .env/bin/activate

Then run the build:

.. code-block::shell

    circuitpython-build-bundles --filename_prefix adafruit-circuitpython-apds --library_location .
