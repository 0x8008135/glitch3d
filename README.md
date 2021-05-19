# Glitch3d #
**THIS MODULE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND**

## Chip ##
This module creates an array of position which is used as an iterator to move around a defined area.

The module supports few algorithms which may be used by the user to discover areas of interests:

* Typewriter (`chip.lr = True`)
    Return to beginning after reching the line (`chip.vertical = False`) or column (`chip.vertical = True`)

* Random (`chip.random = True`)
    Shuffle the coordinates

* Vertical (`chip.vertical = True`)
    Iterates vertically rather than horizontally

* Reverse (`chip.reverse = True`)
    Flip the coordinates (start from furthest)

### Example code ##
```
from glitch3d import chip

target = chip()

# origin
target.offset_x = 0.0
target.offset_y = 0.0

# chip definition
target.x_max = 250.0
target.y_max = 250.0

# steps
target.steps = 10

target.lr = False
target.random = False
target.vertical = False
target.reverse = False

for position in target:
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
p.limits["min_x"] = 0.0
p.limits["max_x"] = 235.0
p.limits["min_y"] = 0.0
p.limits["max_y"] = 235.0
p.limits["min_z"] = 0.0
p.limits["max_z"] = 250.0
p.limits["min_s"] = 0.1
p.limits["max_s"] = 100.0

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
