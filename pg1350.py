#!/usr/bin/python3

from lib import *

pin_size = (2, 1.2)
top_pos = lambda y: (0, y - 5.9)
side_pos = lambda y: (5, y - 3.8)
def side_pos_rev(y):
    side = side_pos(y)
    return (-side[0], side[1])

text = lambda y: [
    Text(type='reference', text='REF**', at=[0, 0], layer='F.Fab', hide=True),
    Text(type='value', text=name, at=[0, y + 7], layer='F.Fab'),
]

core = lambda y: text(y) + rounded_rect(0, y, 15, 15, 1, 'Cmts.User') \
        + rounded_rect(0, y, 13.8, 13.8, 1, 'Cmts.User') \
        + [npth(0, y, 3.4), npth(-5.5, y, 1.7), npth(5.5, y, 1.7),
           RectLine(start=(2.5, y + 6.25), end=(-2.5, y + 3.15), layer='Dwgs.User')]

cap_variants = lambda y: [
    ("", (0, y, 18, 17)),
    ("S", (0, y, 18, 15)),
    ("SL", (-0.75, y, 16.5, 15)),
    ("SR", (0.75, y, 16.5, 15)),
]

trace_width = 0.254     # mm

normal_pins = lambda y, d: [pth(1, *top_pos(y), *pin_size, LAYERS_BTHT),
                            pth((3 if d else 2), *side_pos(y), *pin_size, LAYERS_BTHT)]
rev_pins = lambda y, d: [pth(1, *top_pos(y), *pin_size, LAYERS_THT),
                         pth((3 if d else 2), *side_pos(y), *pin_size, LAYERS_BTHT),
                         pth((3 if d else 2), *side_pos_rev(y), *pin_size, LAYERS_FTHT)]

diode_off = -4.5
def diode_pads(rev):
    typ = Pad.TYPE_THT if rev else Pad.TYPE_SMT
    layers = Pad.LAYERS_THT if rev else Pad.LAYERS_SMT
    drill = 0.4 if rev else 0
    core = [
        Pad(number=3, type=Pad.TYPE_SMT, shape=Pad.SHAPE_CUSTOM, at=side_pos(diode_off), size=(trace_width, trace_width),
            primitives=[Line(start=(0, 0), end=(-2, 2), width=trace_width),
                        Line(start=(-2, 2), end=(-2, 6.95), width=trace_width),
                        Line(start=(-2, 6.95), end=(-3.35, 8.3), width=trace_width)],
            layers=['F.Cu']),
        RectLine(start=(1.4, 0.9), end=(-1.4, -0.9), layer='F.Fab', width=0.12),
    ]
    silk = lambda layer: [
        Line(start=(-2.25, -1), end=(-2.25, 1), layer=layer),
        Line(start=(-2.25, 1), end=(1.65, 1), layer=layer),
        Line(start=(-2.25, -1), end=(1.65, -1), layer=layer),
    ]
    pads = [
        Pad(number=2, type=typ, shape=Pad.SHAPE_RECT, at=(-1.65, 0), size=(0.9, 1.2), drill=drill, layers=layers),
        Pad(number=3, type=typ, shape=Pad.SHAPE_RECT, at=(1.65, 0), size=(0.9, 1.2), drill=drill, layers=layers),
    ]
    line = [
        Pad(number=3, type=Pad.TYPE_SMT, shape=Pad.SHAPE_CUSTOM, at=side_pos_rev(diode_off), size=(0, 0),
            primitives=[Line(start=(0, 0), end=(side_pos(0)[0] * 2, 0), width=trace_width)],
            layers=['B.Cu'])
    ]
    return core + pads + silk('F.SilkS') + (silk('B.SilkS') if rev else []) + (line if rev else [])

for diode in [False, True]:
    for rev in [False, True]:
        off = diode_off if diode else 0
        for cap, outline in cap_variants(off):
            var = ("D" if diode else "") + ("R" if rev else "") + cap
            name = "pg1350" + ("-" + var if var else var)
            footprint("pg1350", name, diode, core(off) + (rev_pins if rev else normal_pins)(off, diode)
                            + cap_outline(outline)
                            + (diode_pads(rev) if diode else []))
