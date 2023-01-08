#!/usr/bin/python3

from typing import Tuple
from lib import *

pin_size = (2, 1.2)
top_pos = lambda y: (0, y - 5.9)
side_pos = lambda y: (5, y - 3.8)
hs_pad_size = 2.6
hs_dx = (9.55 - 5) / 2 + hs_pad_size / 2
def hs_top_pos(y):
    top = top_pos(y)
    return top[0] - hs_dx, top[1]
def hs_side_pos(y):
    side = side_pos(y)
    return side[0] + hs_dx, side[1]

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

def pins(y: float, rev: bool, diode: bool, hotswap: bool):
    def pin(pos: Tuple[float, float], layers, n=None):
        return pth(*pos, *pin_size, layers, n)
    def hole(pos: Tuple[float, float]):
        return npth(*pos, 3)
    def pad(pos: Tuple[float, float], layers, n=None):
        attrs = {"number": n} if n != None else {}
        return Pad(type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, at=pos, size=(hs_pad_size, hs_pad_size), layers=layers, **attrs)
    side_pin_num = None if diode else 2
    if hotswap:
        holes = [hole(top_pos(y)), hole(side_pos(y))]
        pads = [pad(hs_top_pos(y), LAYERS_BACK, n=1), pad(hs_side_pos(y), LAYERS_BACK, n=side_pin_num)]
        if rev:
            holes.append(hole(x_mir(side_pos(y))))
            return holes + pads + [pad(x_mir(hs_top_pos(y)), LAYERS_FRONT, n=1), pad(x_mir(hs_side_pos(y)), LAYERS_FRONT, n=side_pin_num)]
        else:
            return holes + pads
    else:
        if rev:
            return [pin(top_pos(y), LAYERS_THT, n=1),
                    pin(side_pos(y), LAYERS_BTHT, n=side_pin_num),
                    pin(x_mir(side_pos(y)), LAYERS_FTHT, n=side_pin_num)]
        else:
            return [pin(top_pos(y), LAYERS_BTHT, n=1),
                    pin(side_pos(y), LAYERS_BTHT, n=side_pin_num)]

diode_off = -4.5
def diode_pads(rev, hotswap):
    typ = Pad.TYPE_THT if rev else Pad.TYPE_SMT
    layers = Pad.LAYERS_THT if rev else Pad.LAYERS_SMT
    drill = 0.4 if rev else 0
    core = [
        Pad(type=Pad.TYPE_SMT, shape=Pad.SHAPE_CUSTOM, at=side_pos(diode_off), size=(trace_width, trace_width),
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
        Pad(type=typ, shape=Pad.SHAPE_RECT, at=(1.65, 0), size=(0.9, 1.2), drill=drill, layers=layers),
    ]
    line = [
        Pad(type=Pad.TYPE_SMT, shape=Pad.SHAPE_CUSTOM, at=x_mir(side_pos(diode_off)), size=(trace_width, trace_width),
            primitives=[Line(start=(0, 0), end=(side_pos(0)[0] * 2, 0), width=trace_width)],
            layers=['B.Cu'])
    ]
    return core + pads + silk('F.SilkS') + (silk('B.SilkS') if rev else []) + (line if rev else [])

for diode in [False, True]:
    for rev in [False, True]:
        for hotswap in [False, True]:
            off = diode_off if diode else 0
            for cap, outline in cap_variants(off):
                var = ("D" if diode else "") + ("R" if rev else "") + ("H" if hotswap else "") + cap
                name = "pg1350" + ("-" + var if var else var)
                footprint("pg1350", name, diode, core(off) + pins(off, rev, diode, hotswap)
                                + cap_outline(outline)
                                + (diode_pads(rev, hotswap) if diode else []))
