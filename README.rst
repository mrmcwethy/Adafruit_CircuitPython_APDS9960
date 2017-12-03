
Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-APDS9960/badge/?version=latest

    :target: https://circuitpython.readthedocs.io/projects/apds9960/en/latest/

    :alt: Documentation Status

.. image :: https://img.shields.io/discord/327254708534116352.svg
    :target: https://discord.gg/nBQh6qu
    :alt: Discord

TODO

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
  import adafruit_apds9960
  from adafruit_bus_device import I2CDevice

Now initialize the I2CDevice using SCL and SDA pins.  Then initialize the libary.

.. code:: python

  i2c = I2CDevice(SCL, SDA)
  apds9960 = adafruit_apds9960(i2c)

To get a gesture, see if a gesture is available first, then get the gesture Code

.. code:: python

  gesture = apds9960.get_gesture()
  if gesture == apds9960.UP:
    print("up")
  if gesture == apds9960.DOWN
    print("down")
  if gesture == apds9960.RIGHT
    print("right")
  if gesture == apds9960.LEFT
    print("left")

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

    circuitpython-build-bundles --filename_prefix adafruit-circuitpython-apds9960 --library_location .
