#!/usr/bin/python3

from KicadModTree import Footprint, Pad, Text, Line, KicadFileHandler, Arc, Polygon, RectLine
import math

LAYERS_BACK = Pad.LAYERS_CONNECT_BACK
LAYERS_FRONT = Pad.LAYERS_CONNECT_FRONT
LAYERS_THT = Pad.LAYERS_THT
LAYERS_FTHT = ['*.Cu', 'F.Mask']
LAYERS_BTHT = ['*.Cu', 'B.Mask']
LAYERS_SMT_BOTH = ['*.Cu', '*.Mask', '*.Paste']

def footprint(name: str, entities: list):
    fp = Footprint(name)
    fp.extend(entities)
    KicadFileHandler(fp).writeFile(f"{name}.kicad_mod")

def vecadd(a, b):
    return (a[0] + b[0], a[1] + b[1])

def rounded_rect(x: float, y: float, w: float, h: float, r: float, layer: str):
    # start from top right
    centers = [
        (x + w/2 - r, y - h/2 + r),
        (x + w/2 - r, y + h/2 - r),
        (x - w/2 + r, y + h/2 - r),
        (x - w/2 + r, y - h/2 + r),
    ]
    points = [
        vecadd(centers[0], (0, -r)),
        vecadd(centers[0], (r, 0)),
        vecadd(centers[1], (r, 0)),
        vecadd(centers[1], (0, r)),
        vecadd(centers[2], (0, r)),
        vecadd(centers[2], (-r, 0)),
        vecadd(centers[3], (-r, 0)),
        vecadd(centers[3], (0, -r)),
    ]
    entities = []
    for i in range(4):
        entities += [
            Arc(start=points[i*2], end=points[i*2+1], center=centers[i], layer=layer),
            Line(start=points[i*2-1], end=points[i*2], layer=layer),
        ]
    return entities

def npth(x, y, r):
    return Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE, at=(x, y), size=(r, r), drill=r, layers=Pad.LAYERS_THT)

def pth(n, x, y, p, r, layers):
    return Pad(number=n, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE, at=(x, y), size=(p, p), drill=r, layers=layers)

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
        + [npth(0, y, 3.4), npth(-5.5, y, 1.7), npth(5.5, y, 1.7),
           RectLine(start=(2.5, y + 6.25), end=(-2.5, y + 3.15), layer='Dwgs.User')]

cap_variants = lambda y: [
    ("", (0, y, 17.5, 16.5)),
    ("S", (0, y, 17.5, 14.5)),
    ("SL", (-0.75, y, 16, 14.5)),
    ("SR", (0.75, y, 16, 14.5)),
]

trace_width = 0.254     # mm

normal_pins = lambda y: [pth(1, *top_pos(y), *pin_size, LAYERS_BTHT), pth(2, *side_pos(y), *pin_size, LAYERS_BTHT)]
rev_pins = lambda y: [pth(1, *top_pos(y), *pin_size, LAYERS_THT),
                      pth(2, *side_pos(y), *pin_size, LAYERS_BTHT),
                      pth(2, *side_pos_rev(y), *pin_size, LAYERS_FTHT)]

diode_off = -4.5
def diode_pads(rev):
    typ = Pad.TYPE_THT if rev else Pad.TYPE_SMT
    layers = Pad.LAYERS_THT if rev else Pad.LAYERS_SMT
    drill = 0.4 if rev else 0
    core = [
        Pad(number=3, type=Pad.TYPE_SMT, shape=Pad.SHAPE_CUSTOM, at=side_pos(diode_off), size=(0, 0),
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
            footprint(name, core(off) + (rev_pins if rev else normal_pins)(off)
                            + rounded_rect(*outline, 1, 'Dwgs.User')
                            + (diode_pads(rev) if diode else []))
