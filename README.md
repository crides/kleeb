# PG1350 Kicad symbols & footprints

PG1350 symbols and footprints heavily inspired by [@PJE66](https://github.com/PJE66). 

## Symbol

Includes the diode in the symbols. Taken from [@PJE66](https://github.com/PJE66), but with some of the pins hidden as they are not needed for external connections. A switch without diode can be just represented with a normal push button.

![symbol](https://i.imgur.com/xBtscyL.png)

## Footprints

The outline on `User.Comments` is the outline of the side tabs, and the one on `User.Drawings` is the outline of the *keycap*, **thus in the normal footprint it draws the actual keycap size (16.5x17.5mm) instead of choc spacing (17x18mm)!**

All of the footprints are auto generated now. Different letters signify different variations.
- `D`: includes diode in the footprint. It uses choc LED hole for (optional) SOD-123 diode placement, and the internal connections are already made. The center of the footprint is placed on the center of the diode to help with PCBA, and it's meant to be used with the custom symbol signifying that it has a builtin diode; 
- `R`: footprint is reversible. Througholes are included for both sides, another pad is used to connect the duplicated hole, and vias are used inside of the diode pads to connect the diodes on both sides, and silkscreens are duplicated on both sides;
- `S`: shorter spacing, only affects the cap outline. To be used with 15x18 spacing;
- `L` & `R`: only when used with `S`; off centered spacing for use with same finger double column (e.g. most commonly the 2 columns for index finger, or columns for pinky).

(the screenshots may deviate from the actual footprint in terms of keycap outline)

![pg1350](https://i.imgur.com/LoxXtPg.png)

![pg1350 no diode](https://i.imgur.com/XlnosgR.png)

![pg1350 reversible](https://i.imgur.com/kvwp4sg.png)

![pg1350 reversible no diode](https://i.imgur.com/dxx7FFw.png)
