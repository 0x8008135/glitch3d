# Glitch3d #
**THIS MODULE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND**

## Chip ##
This module creates an array of position which is used as an iterator to move around a defined area.

The area is defined by a home point and an end point. once these coordinates have been set, calling the various functions will iterate over the whole area by `chip.steps` steps.

The module supports few algorithms which may be used by the user to discover areas of interests:

* `hozizontal()` scans the area from the home position to the end position by iterating over the X axis first

* `vertical()` scans the whole area by iterating ofer the Y axis first.

* `random()` will randomly scan the whole area.


### Example code ##
```
from glitch3d import chip

target = chip()

# origin
target.set_home(0,0)

# chip definition
target.set_end(250,250)

# steps
target.steps = 10

for position in target.horizontal():
    print(position)

```

A jupyter notebook is available to play around and visualize the chosen algorithm movements.


## Printer ##
This module offers basic functions to drive a 3D Marlin compatible printer through USB (e.g. to perform FI attacks).

The master branch will be kept as generic as possible and has been tested on the following models successfully:
- Creality Ender3
- Creality 6 SE

## Example code for CR-6 SE ##
```
from glitch3d import printer

# Define Serial port settings
serial_port = "/dev/ttyUSB0" # or set to None for automatic detection
serial_baud = 115200
serial_timeout = 1

# Establish connection with the printer
p = printer(port=serial_port,baudrate=serial_baud, timeout=serial_timeout)

# Define printer bed limits (mm)
p.load_settings("cr6s.ini")

# Enter Manual mode
p.manual()

```

## Manual mode ##
In Manual mode, the following keystrokes are supported:

* `up` Move probe forward / Y + step
* `down` Move probe forward / Y - step
* `right` Move probe right / X + step
* `left` Move probe left / X - step 
* `u` Raise probe / Z + step
* `d` Lower probe / Z - step
* `+` Increase step (0.1,1,10,100)
* `-` Decrease step (100,10,1,0.1)
* `s` Manual step definition
* `h` Home on XY !!! WARNING printer dependant
* `z` Home on XYZ 

For safety reasons, a small routine was added to raise the probe of 20.0 mm before homing.
