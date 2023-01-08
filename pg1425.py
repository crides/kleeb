#!/usr/bin/python3

from lib import *

pin_size = (1.6, 1.1)
top_pos = lambda y: (3.4, y - 2)
bot_pos = lambda y: (3.4, y + 2.9)
stab_poses = lambda y: [(5.5, y + 5.5), (-5.5, y - 5.5)]
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

hole_w, hole_h, hole_r = 5.1, 4.1, 1.05
core = lambda y: text(y) \
        + [Rect(start=(7.4, y + 7), end=(-7.4, y - 7), layer='Cmts.User'),
           Rect(start=(2.5, y - 2.9), end=(-2.5, y - 2.9 - 3.6), layer='Dwgs.User'),
           Pad(at=(0, y + 0.1), size=(hole_w, hole_r * 2), drill=(hole_w, hole_r * 2), **mid_hole_param),
           Pad(at=(0, y - 1.9), size=(hole_w, hole_r * 2), drill=(hole_w, hole_r * 2), **mid_hole_param),
           Pad(at=(-1.5, y - 0.9), size=(hole_r * 2, hole_h), drill=(hole_r * 2, hole_h), **mid_hole_param),
           Pad(at=(1.5, y - 0.9), size=(hole_r * 2, hole_h), drill=(hole_r * 2, hole_h), **mid_hole_param)]

cap_variants = lambda y: [
    ("", (0, y, 18, 17)),
]

trace_width = 0.254     # mm

def pins(y: float, rev: bool, diode: bool):
    top_pin_num = 3 if diode else 2
    normal = [pth(top_pin_num, *top_pos(y), *pin_size, LAYERS_BTHT), pth(1, *bot_pos(y), *pin_size, LAYERS_BTHT)]
    reved = [pth(top_pin_num, *x_mir(top_pos(y)), *pin_size, LAYERS_FTHT), pth(1, *x_mir(bot_pos(y)), *pin_size, LAYERS_FTHT)]
    stabs = [npth(*p, 1.3) for p in stab_poses(y)]
    return normal + (reved if rev else []) + stabs

diode_off = 2.9 + 3.6 / 2
def diode_pads(rev):
    typ = Pad.TYPE_THT if rev else Pad.TYPE_SMT
    layers = Pad.LAYERS_THT if rev else Pad.LAYERS_SMT
    drill = 0.4 if rev else 0
    right_pad = (1.65, 0)
    pad_size = (0.9, 1.2)
    tr_pin = top_pos(diode_off)
    dx, dy = tr_pin[0] - right_pad[0], tr_pin[1]
    rev_diode_route = lines([(-2 * tr_pin[0] + dx, dy), (-2 * tr_pin[0] + dx * 2, dy - dx), (0, dy - dx)], width=trace_width)
    core = [
        Pad(number=3, type=Pad.TYPE_SMT, shape=Pad.SHAPE_CUSTOM, at=right_pad, size=(trace_width, trace_width),
            primitives=lines([(0, 0), (0, dy - dx), (dx, dy)], width=trace_width) + (rev_diode_route if rev else []),
            layers=['F.Cu']),
        Rect(start=(1.4, 0.9), end=(-1.4, -0.9), layer='F.Fab', width=0.12),
    ]
    silk = lambda layer: lines([(1.65, -1), (-2.25, -1), (-2.25, 1), (1.65, 1)], layer=layer)
    pads = [
        Pad(number=2, type=typ, shape=Pad.SHAPE_RECT, at=x_mir(right_pad), size=pad_size, drill=drill, layers=layers),
        Pad(number=3, type=typ, shape=Pad.SHAPE_RECT, at=right_pad, size=pad_size, drill=drill, layers=layers),
    ]
    return core + pads + silk('F.SilkS') + (silk('B.SilkS') if rev else [])

for diode in [False, True]:
    for rev in [False, True]:
        off = diode_off if diode else 0
        for cap, outline in cap_variants(off):
            var = ("D" if diode else "") + ("R" if rev else "") + cap
            name = "pg1425" + ("-" + var if var else var)
            footprint("pg1425", name, diode, core(off) + pins(off, rev, diode)
                            + cap_outline(outline)
                            + (diode_pads(rev) if diode else []))
