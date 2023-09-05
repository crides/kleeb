#!/usr/bin/python3

from typing import Tuple
from lib import *
from enum import Enum, auto

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

def core(y: float, compact: bool, both: bool):
    top_hole = Rect(start=(2.5, y - 6.25), end=(-2.5, y - 3.15), layer='Dwgs.User')
    l = [
        Text(type='reference', text='REF**', at=[0, 0], layer='F.Fab', hide=True),
        Text(type='value', text=name, at=[0, y + 7], layer='F.Fab'),
    ] + rounded_rect(0, y, 13.8, 13.8, 1, 'Cmts.User') \
        + [npth(0, y, 3.4), npth(-5.5, y, 1.7), npth(5.5, y, 1.7),
           Rect(start=(2.5, y + 6.25), end=(-2.5, y + 3.15), layer='Dwgs.User')]
    if not compact:
        l += rounded_rect(0, y, 15, 15, 1, 'Cmts.User')
    return (l + [top_hole]) if both else l

cap_variants = lambda y: [
    ("", (0, y, 18, 17)),
    ("S", (0, y, 18, 15)),
    ("SN", (0, y, 15, 15)),
    ("SL", (-0.75, y, 16.5, 15)),
    ("SR", (0.75, y, 16.5, 15)),
    ("C", (0, y, 18, 14)),
    ("CN", (0, y, 15, 14)),
    ("CL", (-0.75, y, 16.5, 14)),
    ("CR", (0.75, y, 16.5, 14)),
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

class DiodeRevVariants(Enum):
    NONE = auto()
    REV = auto()
    BETTER_REV = auto()

diode_off = -4.5
def diode_pads(rev: DiodeRevVariants, hotswap: bool):
    def side_trace(right: int, layer: str) -> Pad:
        return Pad(number=3, type=Pad.TYPE_SMT, shape=Pad.SHAPE_OVAL, at=(right * (dpad_x + 3) / 2, 0), size=(3 - dpad_x + trace_width, trace_width), layers=[layer])
    def side_via(right: int) -> Pad:
        return Pad(number=3, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE, at=(right * 3, 0), size=(0.8, 0.8), drill=0.4, layers=['*.Cu'])
    rev_not_none = rev != DiodeRevVariants.NONE
    if rev == DiodeRevVariants.REV:
        typ = Pad.TYPE_THT
        layers = Pad.LAYERS_THT
    elif rev == DiodeRevVariants.NONE:
        typ = Pad.TYPE_SMT
        layers = ['*.Cu', '*.Mask', '*.Paste']      # Easy way to get pads on both sides
    elif rev == DiodeRevVariants.BETTER_REV:
        typ = Pad.TYPE_SMT
        layers = Pad.LAYERS_THT
    drill = 0.4 if rev else 0
    dpad_x = 1.65
    dpad_size = (0.9, 1.2)
    if hotswap:
        route = [
            side_trace(1, 'B.Cu' if rev_not_none else 'F.Cu'),
            line_pad(3, [(0, 0), (4.5, -4.5), (4.5, -8.3)], (3, 0), ['B.Cu'], trace_width),
        ]
        if rev == DiodeRevVariants.NONE:
            route.append(side_via(1))
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
        sp = side_pos(diode_off)
        better = rev == DiodeRevVariants.BETTER_REV
        mid = 3
        start = mid if better else dpad_x
        route_raw = [sp, (mid, sp[1] + 2), (mid, dpad_x - mid), (start, 0)]
        route = [line_pad(3, [(x - start, y) for x, y in route_raw], (start, 0), ['F.Cu'], trace_width)]
        line = [line_pad(3, [(0, 0), (sp[0] * 2, 0)], x_mir(side_pos(diode_off)), ['B.Cu'], trace_width)]
        if better:
            route.extend([
                side_trace(1, 'B.Cu'), side_trace(1, 'F.Cu'),
                side_trace(-1, 'B.Cu'), side_trace(-1, 'F.Cu'),
                side_via(1), side_via(-1),
            ])
    core = [*route, Rect(start=(1.4, 0.9), end=(-1.4, -0.9), layer='F.Fab', width=0.12)]
    silk = lambda layer: lines([(1.65, -1), (-2.25, -1), (-2.25, 1), (1.65, 1)], layer=layer)
    
    pads = [
        Pad(number=2, type=typ, shape=Pad.SHAPE_RECT, at=(-dpad_x, 0), size=dpad_size, drill=drill, layers=layers),
        Pad(number=3, type=typ, shape=Pad.SHAPE_RECT, at=(dpad_x, 0), size=dpad_size, drill=drill, layers=layers),
    ]
    return core + pads + silk('F.SilkS') + (silk('B.SilkS') if rev_not_none else []) + (line if rev_not_none else [])

for diode in [False, True]:
    for rev in DiodeRevVariants.__members__.values():
        if rev == DiodeRevVariants.BETTER_REV and not diode:
            continue
        for hotswap in [False, True]:
            off = diode_off if diode else 0
            for cap, outline in cap_variants(off):
                rev_marker = "R" if rev == DiodeRevVariants.REV else "" if rev == DiodeRevVariants.NONE else "R1"
                var = ("D" if diode else "") + rev_marker + ("H" if hotswap else "") + cap
                name = "pg1350" + ("-" + var if var else var)
                reverse = rev != DiodeRevVariants.NONE
                compact = "C" in var
                footprint("pg1350", name, diode, core(off, compact, False) + pins(off, reverse, diode, hotswap)
                                + cap_outline(outline)
                                + (diode_pads(rev, hotswap) if diode else []))
                if not diode and hotswap:
                    name = "pg1350-" + ("R" if reverse else "") + "B" + cap
                    normal_pads, hotswap_pads = pins(0, reverse, False, False), pins(0, reverse, False, True)
                    pads = normal_pads + [p.rotate(180) for p in hotswap_pads]
                    footprint("pg1350", name, False, core(0, compact, True) + pads + cap_outline(outline))
