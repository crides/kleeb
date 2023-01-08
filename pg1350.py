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
           Rect(start=(2.5, y + 6.25), end=(-2.5, y + 3.15), layer='Dwgs.User')]

cap_variants = lambda y: [
    ("", (0, y, 18, 17)),
    ("S", (0, y, 18, 15)),
    ("SL", (-0.75, y, 16.5, 15)),
    ("SR", (0.75, y, 16.5, 15)),
]

trace_width = 0.254     # mm

def pins(y: float, rev: bool, diode: bool, hotswap: bool):
    def pin(n, pos: Tuple[float, float], layers):
        return pth(n, *pos, *pin_size, layers)
    def hole(pos: Tuple[float, float]):
        return npth(*pos, 3)
    def pad(n, pos: Tuple[float, float], layers):
        return Pad(number=n, type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, at=pos, size=(hs_pad_size, hs_pad_size), layers=layers)
    side_pin_num = 3 if diode else 2
    if hotswap:
        holes = [hole(top_pos(y)), hole(side_pos(y))]
        pads = [pad(1, hs_top_pos(y), LAYERS_BACK), pad(side_pin_num, hs_side_pos(y), LAYERS_BACK)]
        if rev:
            holes.append(hole(x_mir(side_pos(y))))
            return holes + pads + [pad(1, x_mir(hs_top_pos(y)), LAYERS_FRONT), pad(side_pin_num, x_mir(hs_side_pos(y)), LAYERS_FRONT)]
        else:
            return holes + pads
    else:
        if rev:
            return [pin(1, top_pos(y), LAYERS_THT),
                    pin(side_pin_num, side_pos(y), LAYERS_BTHT),
                    pin(side_pin_num, x_mir(side_pos(y)), LAYERS_FTHT)]
        else:
            return [pin(1, top_pos(y), LAYERS_BTHT),
                    pin(side_pin_num, side_pos(y), LAYERS_BTHT)]

diode_off = -4.5
def diode_pads(rev, hotswap):
    typ = Pad.TYPE_THT if rev else Pad.TYPE_SMT
    layers = Pad.LAYERS_THT if rev else Pad.LAYERS_SMT
    drill = 0.4 if rev else 0
    dpad_x = 1.65
    dpad_size = (0.9, 1.2)
    if hotswap:
        via = Pad(number=3, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE, at=(3, 0), size=(0.8, 0.8), drill=0.4, layers=['*.Cu'])
        route = [
            Pad(number=3, type=Pad.TYPE_SMT, shape=Pad.SHAPE_OVAL, at=((dpad_x + 3) / 2, 0), size=(3 - dpad_x + trace_width, trace_width), layers=['B.Cu' if rev else 'F.Cu']),
            line_pad(3, [(0, 0), (4.5, -4.5), (4.5, -8.3)], (3, 0), ['B.Cu'], trace_width),
        ]
        if not rev:
            route.append(via)
    else:
        route = line_pad(3, [(3.35, -8.3), (1.35, -6.3), (1.35, -1.35), (0, 0)], (dpad_x, 0), ['F.Cu'], trace_width),
    if hotswap:
        mir_line = lambda l: [x_mir(p) for p in l]
        top_line = [(0, 0), (1, 0), (2.5, -1.5)]
        bot_line = [(0, 0), (1.0, 0), (1.6, 0.6), (6.9, 0.6), (8, -0.5)]
        line = [
            line_pad(1, mir_line(top_line), (0, diode_off - 3.5), ['B.Cu'], trace_width),
            Pad(type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE, at=(0, diode_off-3.5), size=(0.8, 0.8), drill=0.4, layers=['*.Cu']),
            line_pad(1, top_line, (0, diode_off - 3.5), ['F.Cu'], trace_width),

            line_pad(3, mir_line(bot_line), (0, diode_off - 2.5), ['F.Cu'], trace_width),
            Pad(type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE, at=(0, diode_off-2.5), size=(0.8, 0.8), drill=0.4, layers=['*.Cu']),
            line_pad(3, bot_line, (0, diode_off - 2.5), ['B.Cu'], trace_width),
        ]
    else:
        line = [line_pad(3, [(0, 0), (side_pos(0)[0] * 2, 0)], x_mir(side_pos(diode_off)), ['B.Cu'], trace_width)]
    core = [*route, Rect(start=(1.4, 0.9), end=(-1.4, -0.9), layer='F.Fab', width=0.12)]
    silk = lambda layer: lines([(1.65, -1), (-2.25, -1), (-2.25, 1), (1.65, 1)], layer=layer)
    
    pads = [
        Pad(number=2, type=typ, shape=Pad.SHAPE_RECT, at=(-dpad_x, 0), size=dpad_size, drill=drill, layers=layers),
        Pad(number=3, type=typ, shape=Pad.SHAPE_RECT, at=(dpad_x, 0), size=dpad_size, drill=drill, layers=layers),
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
