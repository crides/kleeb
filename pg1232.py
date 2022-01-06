#!/usr/bin/python3

from lib import *
import os

pin_size = (1.6, 1.1)
top_pos = lambda y: (2, y + 5.4)
side_pos = lambda y: (-4.58, y + 5.1)
stab_pos = lambda y: (5.3, y - 4.75)
def x_mir(p):
    return (-p[0], p[1])

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
        + [RectLine(start=(6.75, y + 6.25), end=(-6.75, y - 6.25), layer='Cmts.User'),
           RectLine(start=(2.8, y - 3.25), end=(-2.8, y - 5.45), layer='Dwgs.User'),
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
]

trace_width = 0.254     # mm

def pins(y: float, rev: bool, diode: bool):
    normal = [pth(1, *top_pos(y), *pin_size, LAYERS_BTHT), pth((3 if diode else 2), *side_pos(y), *pin_size, LAYERS_BTHT)]
    reved = [pth(1, *x_mir(top_pos(y)), *pin_size, LAYERS_FTHT), pth((3 if diode else 2), *x_mir(side_pos(y)), *pin_size, LAYERS_FTHT)]
    stab_layer = LAYERS_THT if rev else LAYERS_BTHT
    stabs = [pth((5 if diode else 3), *stab_pos(y), *pin_size, stab_layer), pth(4, *x_mir(stab_pos(y)), *pin_size, stab_layer)]
    return normal + (reved if rev else []) + stabs

diode_off = 4.35
def diode_pads(rev):
    typ = Pad.TYPE_THT if rev else Pad.TYPE_SMT
    layers = Pad.LAYERS_THT if rev else Pad.LAYERS_SMT
    drill = 0.4 if rev else 0
    left_pad = (-1.65, 0)
    pad_size = (0.9, 1.2)
    core = [
        Pad(number=3, type=Pad.TYPE_SMT, shape=Pad.SHAPE_CUSTOM, at=left_pad, size=(trace_width, trace_width),
            primitives=[Line(start=(-4.75, 7.63), end=(-2.93, 9.45), width=trace_width),
                        Line(start=(0, 0), end=(-1.3, 0), width=trace_width),
                        Line(start=(-1.3, 0), end=(-2.25, 0.95), width=trace_width),
                        Line(start=(-4.75, 1.25), end=(-4.75, 7.63), width=trace_width),
                        Line(start=(-2.25, 0.95), end=(-4.45, 0.95), width=trace_width),
                        Line(start=(-4.45, 0.95), end=(-4.75, 1.25), width=trace_width)],
            layers=['F.Cu']),
        RectLine(start=(1.4, 0.9), end=(-1.4, -0.9), layer='F.Fab', width=0.12),
    ]
    silk = lambda layer: [
        Line(start=(2.25, -1), end=(2.25, 1), layer=layer),
        Line(start=(2.25, 1), end=(-1.65, 1), layer=layer),
        Line(start=(2.25, -1), end=(-1.65, -1), layer=layer),
    ]
    pads = [
        Pad(number=3, type=typ, shape=Pad.SHAPE_RECT, at=left_pad, size=pad_size, drill=drill, layers=layers),
        Pad(number=2, type=typ, shape=Pad.SHAPE_RECT, at=x_mir(left_pad), size=pad_size, drill=drill, layers=layers),
    ]
    return core + pads + silk('F.SilkS') + (silk('B.SilkS') if rev else [])

for diode in [False, True]:
    for rev in [False, True]:
        off = diode_off if diode else 0
        for cap, outline in cap_variants(off):
            var = ("D" if diode else "") + ("R" if rev else "") + cap
            name = "pg1232" + ("-" + var if var else var)
            model_path = os.path.normpath(os.path.dirname(__file__) + "/models/pg1232.step")
            footprint("pg1232", name, diode, core(off) + pins(off, rev, diode)
                            + cap_outline(outline)
                            + (diode_pads(rev) if diode else [])
                            + [Model(filename=model_path, at=(0, -0.1712598425, 0))])
