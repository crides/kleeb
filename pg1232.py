#!/usr/bin/python3

from typing import Tuple
from lib import *
import os

pin_size = (1.6, 1.1)
top_pos = lambda y: (2, y + 5.4)
side_pos = lambda y: (-4.58, y + 5.1)
stab_pos = lambda y: (5.3, y - 4.75)
text = lambda y: [
    Text(type='reference', text='REF**', at=[0, 0], layer='F.Fab', hide=True),
    Text(type='value', text=name, at=[0, y + 9], layer='F.Fab'),
]

mid_hole_param = {
    "type": Pad.TYPE_NPTH,
    "shape": Pad.SHAPE_OVAL,
    "layers": Pad.LAYERS_NPTH,
}

core = lambda y: text(y) \
        + [Rect(start=(6.75, y + 6.25), end=(-6.75, y - 6.25), layer='Cmts.User'),
           Rect(start=(2.8, y - 3.25), end=(-2.8, y - 5.45), layer='Dwgs.User'),
           Pad(at=(-5.7, y), rotation=90, size=(5.8, 0.3), drill=(5.8, 0.3), **mid_hole_param),
           Pad(at=(4.85, y), size=(2, 5.8), drill=(2, 5.8), **mid_hole_param),
           Pad(at=(0, y + 3.3), size=(4.5, 1), drill=(4.5, 1), **mid_hole_param),
           Pad(at=(-4.85, y), size=(2, 5.8), drill=(2, 5.8), **mid_hole_param),
           Pad(at=(0, y + 3.65), size=(4.5, 0.3), drill=(4.5, 0.3), **mid_hole_param),
           Pad(at=(0, y + 2.75), size=(11.7, 0.3), drill=(11.7, 0.3), **mid_hole_param),
           Pad(at=(2.1, y + 3.25), rotation=90, size=(1.1, 0.3), drill=(1.1, 0.3), **mid_hole_param),
           Pad(at=(5.7, y), rotation=90, size=(5.8, 0.3), drill=(5.8, 0.3), **mid_hole_param),
           Pad(at=(-2.1, y + 3.25), rotation=90, size=(1.1, 0.3), drill=(1.1, 0.3), **mid_hole_param),
           Pad(at=(0, y + -2.75), size=(11.7, 0.3), drill=(11.7, 0.3), **mid_hole_param),
           Pad(at=(0, y), size=(11.7, 5.8), drill=(11.7, 5.8), **mid_hole_param)]

cap_variants = lambda y: [
    ("", (0, y, 18, 17)),
    ("S", (0, y, 18, 15)),
    ("SL", (-0.875, y, 16.25, 15)),
    ("SR", (0.875, y, 16.25, 15)),
    ("SS", (0, y, 18, 13.5)),
    ("SSN", (0, y, 14.5, 13.5)),
    ("SSL", (-0.875, y, 16.25, 13.5)),
    ("SSR", (0.875, y, 16.25, 13.5)),
    ("C", (0, y, 18, 12.5)),
    ("CN", (0, y, 14.5, 12.5)),
    ("CL", (-0.875, y, 16.25, 12.5)),
    ("CR", (0.875, y, 16.25, 12.5)),
]

trace_width = 0.254     # mm

def pins(y: float, rev: bool, diode: bool, hotswap: bool):
    def oval(n, pos, layers):
        return Pad(number=n, type=Pad.TYPE_THT, shape=Pad.SHAPE_OVAL, at=pos, size=(2, 1.5), drill=(1, 0.5), layers=layers)
    def oval_vert(n, pos, layers):
        pad = oval(n, pos, layers)
        pad.rotation = 90
        return pad
    def circle(n, pos: Tuple[float, float], layers):
        return pth(n, *pos, *pin_size, layers)
    vert = oval_vert if hotswap else circle
    horiz = oval if hotswap else circle
    side_pin_num = 3 if diode else 2
    normal = [horiz(1, top_pos(y), LAYERS_BTHT), vert(side_pin_num, side_pos(y), LAYERS_BTHT)]
    reved = [horiz(1, x_mir(top_pos(y)), LAYERS_FTHT), vert(side_pin_num, x_mir(side_pos(y)), LAYERS_FTHT)]
    stab_layer = LAYERS_THT if rev else LAYERS_BTHT
    stabs = [vert(4, stab_pos(y), stab_layer), vert(5, x_mir(stab_pos(y)), stab_layer)]
    return normal + (reved if rev else []) + stabs

diode_off = 4.35
def diode_pads(rev):
    typ = Pad.TYPE_THT if rev else Pad.TYPE_SMT
    layers = Pad.LAYERS_THT if rev else Pad.LAYERS_SMT
    drill = 0.4 if rev else 0
    left_pad = (-1.65, 0)
    pad_size = (0.9, 1.2)
    core = [
        line_pad(3, [(0, 0), (-1.3, 0), (-2.25, 0.95), (-4.45, 0.95), (-4.75, 1.25), (-4.75, 7.63), (-2.93, 9.45)], left_pad, ['F.Cu'], trace_width),
        Rect(start=(1.4, 0.9), end=(-1.4, -0.9), layer='F.Fab', width=0.12),
    ]
    silk = lambda layer: lines([(-1.65, -1), (2.25, -1), (2.25, 1), (-1.65, 1)], layer=layer)
    pads = [
        Pad(number=3, type=typ, shape=Pad.SHAPE_RECT, at=left_pad, size=pad_size, drill=drill, layers=layers),
        Pad(number=2, type=typ, shape=Pad.SHAPE_RECT, at=x_mir(left_pad), size=pad_size, drill=drill, layers=layers),
    ]
    return core + pads + silk('F.SilkS') + (silk('B.SilkS') if rev else [])

for diode in [False, True]:
    for rev in [False, True]:
        for hotswap in [False, True]:
            off = diode_off if diode else 0
            for cap, outline in cap_variants(off):
                var = ("D" if diode else "") + ("R" if rev else "") + ("H" if hotswap else "") + cap
                name = "pg1232" + ("-" + var if var else var)
                model_path = os.path.normpath(os.path.dirname(__file__) + "/models/pg1232.step")
                footprint("pg1232", name, diode, core(off) + pins(off, rev, diode, hotswap)
                                + cap_outline(outline)
                                + (diode_pads(rev) if diode else [])
                                + [Model(filename=model_path, at=(0, (-diode_off / 25.4 if diode else 0), 0))])
