# Kleeb

This is a collection of the Kicad symbols, footprints and 3D models useful in keyboard creation other than normal mechanical switches and the ones included in Kicad's standard library, all in 6.0 format. I didn't create all of them, and some come from either other people on Discord, or from other online resources that isn't in a Git tree. Putting them in a centralized place means it's easier for people to use, distribute*, and compare, and changes can be made in a clearer way. I'll try to list the sources down below, but due to the nature of the sources they maybe incorrect/missing. If you have a problem with how I'm using/distributing them please let me know.

## License

Those directly created by me is licensed under MIT. Those came from Discord are technically in a grey zone, as they are shared without a (explicit) license. For those that came from other sources, the original license should be used. I do not intend to claim ownership over them, and they are here so they can be easily included in future projects.

## Symbols

### `ic`

- `MCP23S08`: From @petejohanson, converted to 6.0. 8-bit SPI bidirectional I/O expander, missing from Kicad libray
- `MT25QL128ABA1ESE`: created by me. 128Mib/16MiB QSPI NOR flash

### `display`

- `eink-128x80`: created by me. [128x80 Eink from waveshare](https://www.waveshare.com/product/displays/1.02inch-e-paper-module.htm)
- `ILI9341`: created by me. ILI9341 module
- `LCD2.2"`: created by me. [2.2 in TFT LCD module from Adafruit](https://www.adafruit.com/product/1480)
- `OLED-128x32`: created by me. Classic 128x32 OLED module [Example](https://www.littlekeyboards.com/collections/oled-screens/products/oled-screen)
- `OLED-128x64`: created by me. 128x64 OLED module [Example](https://www.littlekeyboards.com/collections/oled-screens/products/128x64-oled-screen)
- `adafruit-sharp-memory-display`: created by me. [Adafruit 1.3in SHARP memory display module](https://www.adafruit.com/product/3502)
- `adafruit-sharp-memory-display-no-useless`: created by me. Same as above but without non-necessary pins
- `TM022HDH26`: created by me. [2.2in raw SPI TFT LCD module](https://www.aliexpress.com/item/32417585937.html)

### `switch`

- `SKRHA`: created by me. [5-way joystick from Alps](https://www.mouser.com/ProductDetail/Alps-Alpine/SKRHAAE010?qs=6EGMNY9ZYDQQG43X8RE8sg%3D%3D)

### `mcu`

- `holyiot-18010`: From someone else on Discord, but modified by me. [Holyiot 18010 nRF52840 BLE module](https://www.aliexpress.com/i/32868002366.html)
- `holyiot-18010-no-underside`: Same as above, but without underside pads
- `xiao`: created by me, merged from the `xiao` repo. The [Xiao controller](https://www.seeedstudio.com/Seeeduino-XIAO-Arduino-Microcontroller-SAMD21-Cortex-M0+-p-4426.html) from Seeed Studio.
- `xiao-ble`: Same as above. The [Xiao BLE controller](https://www.seeedstudio.com/Seeed-XIAO-BLE-nRF52840-p-5201.html) from Seeed Studio.

## Footprints

### `display`

- `LCD2.2in`: created by me.
- `OLED-128x32`: created by me.
- `OLED-128x32-cutout`: Same as above, but show the display area. Data came from `@rain` on Discord
- `OLED-128x32-double-sided`: Same as above, but has jumpers on both sides allowing the OLED to be installed on both sides. The jumpers on the reverse side of the display are to be soldered.
- `OLED-128x64`: created by me.
- `TM022HDH26`: created by me. Holes follow the positions on datasheet, pads are measured data
- `TM022HDH26_back`: Same as above, but pads are on the different side of PCB
- `adafruit-sharp-memory-display-1.3in`: From someone on Discord, modified by me
- `adafruit-sharp-memory-display-1.3in-no-mounting`: Same as above
- `adafruit-sharp-memory-display-1.3in-no-mounting-no-useless`: Same as above

### `mcu`

- `holyiot-18010`: Probably from someone on Discord, modified by me. [Holyiot 18010 nRF52840 BLE module](https://www.aliexpress.com/i/32868002366.html)
- `holyiot-18010-no-underside`: Same as above
- `xiao-smd`: created by me, merged from the `xiao` repo. The Xiao controller with SMD pads, with throughole pads for the 4 underside pads.
- `xiao-tht`: Same as above. The Xiao controller with THT pads, with throughole pads for the 4 underside pads.
- `xiao-ble-smd`: Same as above. The Xiao BLE controller with SMD pads, with throughole pads for the 4 pads under USB-C connector, 2 battery pads, and 2 NFC pads.
- `xiao-ble-tht`: Same as above. The Xiao BLE controller with THT pads, with throughole pads for the 4 pads under USB-C connector, 2 battery pads, and 2 NFC pads.
- `xiao-ble-tht-cutout`: Same as above. The Xiao BLE controller with THT pads, with throughole pads for the 4 pads under USB-C connector, 2 battery pads, and 2 NFC pads, except there are cutouts around the underside pads, so that one can cut around the pads making it easier to solder those pads.

### `misc`

- `BA1AAAPC`: [From Digikey](https://www.digikey.com/en/products/detail/mpd-memory-protection-devices/BA1AAAPC/8119216). Low profile AAA battery holder
- `auklet-cover-mount`: created by me. Cover mounting positions for the Auklet steno board
- `auklet-mount`: created by me. Bottom screw hole mounting positions for the Auklet steno board
- `batwings`: created by me. The original batwings logo converted from some picture on the web
- `crides-pos`: created by me. The logo for `crides`
- `crides-neg`: Same as above, but inverted
- `debug-port`: created by me. For use with pogo pin clamp for SWD debug
- `debug-port-single-side`: Same as above, but only top side has solder mask
- `embedded`: created by me. The embedded steno logo
- `hirose-df30fb-20ds-0.4v(82)`: probably from Digikey

### `switch`

- `SKRHA-boss`: created by me, following datasheet from Alps
- `SKRHA-no-boss`: same as above
- `switch-MSK-12C02-smd`: Not sure where from

## Models

- `adafruit-sharp-memory-display`: Obtained from @petejohanson on Discord, not sure of creator
- `adafruit-sharp-memory-display-no-mounting`: As above, but edited to cut off mounting screw holes
- `BA1AAAPC`: [From Digikey](https://www.digikey.com/en/products/detail/mpd-memory-protection-devices/BA1AAAPC/8119216). Low profile AAA battery holder
- `holyiot-18010`: From `@darryldh` on Discord
- `hro-type-c-31-m-12`: Not sure of source; I probably got it on Discord
- `MBK-1u`: [From `@darryldh` on Thingiverse](https://www.thingiverse.com/thing:4564253)
- `SKRHAD`: [From Alps](https://tech.alpsalpine.com/prod/e/html/multicontrol/switch/skrh/skrhace010.html)
- `OLED-128x32`: Not sure from where. Model for the 128x32 OLED displays
- `TF31-12S-0.5SH`: Not sure from where exactly, should be a manufactorer model. 0.5mm pitched 12pin FPC ZIF socket
- `JST-PH-S2B-R`: [From SnapEDA on Digikey](https://www.digikey.com/short/p1d9b87m). JST PH SMD 2pin connector, commonly used for batteries. [Product on Adafruit](https://www.adafruit.com/product/1769)
