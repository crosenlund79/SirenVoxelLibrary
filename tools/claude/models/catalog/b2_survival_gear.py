"""Batch B2 - survival gear (creator: Claude).

X right, Y front (+Y), Z up; inclusive cell ranges.
Shared choices so the set reads as one household's kit: forest-green camping gear (lantern,
stove), olive military surplus (jerry can, backpack), faded red plastics (fuel can), cream
enamel and sage ceramics from the same kitchen as the pilot workbench's mug. Nothing glows:
lenses, globes and the candle are unlit, pale opaque colours.
"""
import math

import numpy as np

from catalog_registry import model
from voxkit import Grid, hash01


def _disc(g, cx, cy, r):
    return g.disc_cells(cx, cy, r)


def _ring(g, cx, cy, r):
    return g.ring_cells(cx, cy, r)


def _layer(g, cells, z, c):
    for (i, j) in cells:
        g.set(i, j, z, c)


# =====================================================================================
# Lights
# =====================================================================================
@model("flashlight",
       story="The big rubber flashlight from the hall cupboard, the one that always worked in "
             "power cuts. Its lanyard is still looped from the last time someone carried it "
             "down to check the basement.",
       details=["Ribbed black rubber grip between a mustard-yellow tail cap and head",
                "Flared head with a bright bezel and a pale, unlit lens",
                "Rubber switch cover on top", "Paracord lanyard loop lying behind it"],
       exclusions=["No emissive lens or light beam", "No brand marks"],
       notes=["Rubber-gripped flashlight with a flared head and pale lens (no emissive), a "
              "lanyard loop.",
              "Head is 8.75 cm across (7 cells): an odd cell count keeps the lens a clean "
              "circle; the reference's 10 cm is a coarse-cell size."],
       front_note="Lies on its side as it would rest on a table: lens points +Y, switch up, "
                  "lowest point on z = 0.",
       attachments={"grip": {"description": "Main hand around the ribbed rubber grip, thumb "
                                            "on the switch."}})
def flashlight():
    g = Grid(9, 26, 7)
    cx, cz = 4.5, 3.5
    Y0 = 4                                                       # tail cap starts here
    # tail cap, ribbed rubber body, neck flare, head, bezel and lens
    g.cyl_y(cx, cz, 2.5, Y0, Y0 + 1, "mustard_dark")
    g.cyl_y(cx, cz, 2.5, Y0 + 2, Y0 + 12, "charcoal")
    for y in range(Y0 + 3, Y0 + 12, 2):
        for (i, k) in g.ring_cells(cx, cz, 2.5):
            g.set(i, y, k, "black")                               # grip ribs
    g.cyl_y(cx, cz, 3.0, Y0 + 13, Y0 + 14, "mustard_dark")       # neck flare
    g.cyl_y(cx, cz, 3.5, Y0 + 15, Y0 + 19, "mustard_dark")       # head
    g.cyl_y(cx, cz, 3.5, Y0 + 15, Y0 + 15, "mustard_deep")       # seam
    g.cyl_y(cx, cz, 3.5, Y0 + 20, Y0 + 20, "steel_light")        # bezel
    g.cyl_y(cx, cz, 2.5, Y0 + 20, Y0 + 20, "glass_hi")           # pale lens
    g.set(4, Y0 + 20, 3, "mirror")
    # rubber switch cover on top of the body
    g.box(4, Y0 + 9, 6, 4, Y0 + 10, 6, "iron_edge")
    # scuffs on the head where it has been put down on concrete
    g.paint(1, Y0 + 16, 0, 7, Y0 + 19, 0, "mustard_deep")
    g.paint(2, Y0 + 17, 0, 6, Y0 + 18, 0, "ochre_dark")
    # lanyard: a paracord loop from the tail ring, lying on the floor behind
    g.box(4, Y0 - 1, 1, 4, Y0 - 1, 1, "steel_dark")              # split ring
    g.set(4, Y0 - 1, 0, "olive")
    for (x, y) in [(3, 0), (4, 0), (5, 0), (2, 1), (3, 1), (5, 1), (6, 1), (2, 2), (6, 2),
                   (2, 3), (3, 3), (4, 3), (5, 3), (6, 3)]:
        g.set(x, y, 0, "olive")                                   # face-connected cord loop
    return {"grid": g, "attachments": {"grip": (4, Y0 + 7, 3)},
            "footprint_cells": ((1, 7), (Y0, Y0 + 20))}


@model("battery_lantern",
       story="A forest-green camping lantern that lived in the garage with the tent. Since "
             "the power went it has stood on the kitchen table every night; the batteries "
             "are almost done and nobody has found more.",
       details=["Round green base with a rotary dial and a rubber foot ring",
                "Frosted globe (opaque, unlit) between four slim struts",
                "Vented top cap with a wire bail handle folded up",
                "Scuffs on the base rim where it is set down"],
       exclusions=["No emissive globe or glow", "No brand marks"],
       notes=["Camping lantern with folding handle, frosted globe (opaque), dark base and top "
              "cap.",
              "Base and cap are 0.175 m (radius-7 clean pixel circles); the bail pivots make "
              "it 0.2 m wide, a little under the reference."])
def battery_lantern():
    g = Grid(18, 18, 28)
    C = 9.0                                                      # axis on a cell boundary
    base, base_hi = "green_dark", "green"
    _layer(g, _disc(g, C, C, 6), 0, "black")                     # rubber foot ring
    for z in range(1, 7):
        _layer(g, _disc(g, C, C, 7), z, base)
    _layer(g, _disc(g, C, C, 7), 6, base_hi)                     # top band of the base
    for (i, j) in _ring(g, C, C, 7):
        if j >= 12 and 4 <= i <= 10:
            g.set(i, j, 1, "green_deep")                         # scuffed where it is set down
            if 6 <= i <= 8:
                g.set(i, j, 2, "green_deep")
    # rotary dial on the front of the base
    g.box(8, 16, 3, 9, 16, 4, "steel_light")
    g.set(9, 16, 4, "steel_hi")
    # frosted globe
    for z in range(7, 19):
        _layer(g, _disc(g, C, C, 6), z, "porcelain")
    for z in (7, 18):
        _layer(g, _disc(g, C, C, 6), z, "porcelain_mid")
    # four struts between base and cap
    for (x0, y0, x1, y1) in [(8, 2, 9, 2), (8, 15, 9, 15), (2, 8, 2, 9), (15, 8, 15, 9)]:
        g.box(x0, y0, 7, x1, y1, 18, base)
    # top cap, vents and the hanging hook
    for z in (19, 20):
        _layer(g, _disc(g, C, C, 7), z, base)
    _layer(g, _disc(g, C, C, 7), 20, base_hi)
    _layer(g, _disc(g, C, C, 5), 21, base)
    _layer(g, _disc(g, C, C, 3), 22, "charcoal")
    for (x, y) in [(5, 9), (12, 8), (8, 5), (9, 12)]:
        g.set(x, y, 21, "green_deep")                            # vent slots
    # wire bail handle, folded up over the cap
    for (i, k, a, d) in _arc(C, 20.0, 6.5, 7.6):
        g.set(i, 8, k, "steel")
        g.set(i, 9, k, "steel")
    for x in (2, 15):
        g.box(x, 8, 19, x, 9, 20, "steel_dark")                  # pivots
    return g


def _arc(cx, cz, r_in, r_out, a0=0, a1=180):
    """Upper half of a face-connected circle outline of radius r_out in a vertical plane:
    (i, k, angle, distance). r_in is unused (kept for call compatibility); the outline is the
    disc cells with any 8-neighbour outside the disc, so it never joins only diagonally."""
    def inside(i, k):
        return math.hypot(i + 0.5 - cx, k + 0.5 - cz) <= r_out
    out = []
    for i in range(int(cx - r_out) - 1, int(cx + r_out) + 2):
        for k in range(int(cz), int(cz + r_out) + 2):
            if not inside(i, k):
                continue
            if all(inside(i + di, k + dk) for di in (-1, 0, 1) for dk in (-1, 0, 1)):
                continue
            dx, dz = i + 0.5 - cx, k + 0.5 - cz
            a = math.degrees(math.atan2(dz, dx))
            if a0 <= a <= a1:
                out.append((i, k, a, math.hypot(dx, dz)))
    return out


@model("candle",
       story="An ivory pillar candle on a chipped sage saucer from the kitchen. It has been "
             "lit every evening since the outage and is burned halfway, wax spilled down one "
             "side; the spent match was dropped on the saucer.",
       details=["Pillar candle tunnelled at the top, one wall of wax left standing",
                "Curled black wick (unlit, no flame)",
                "Drips running down the camera side into a puddle on the saucer",
                "Sage glazed saucer with a chip showing the pale clay, a spent match"],
       exclusions=["No flame or glow", "No candle holder glass"],
       notes=["Pillar candle half burned with wax drips, on a chipped saucer."])
def candle():
    g = Grid(14, 14, 17)
    C = 7.0
    T = 13                                                       # top row of the pillar
    # saucer: foot ring, floor, raised rim
    _layer(g, _disc(g, C, C, 4.5), 0, "sage_dark")
    _layer(g, _disc(g, C, C, 6.5), 1, "sage")
    _layer(g, _ring(g, C, C, 7), 1, "sage")
    _layer(g, _ring(g, C, C, 7), 2, "sage_hi")
    # a chip out of the rim on the left side, pale clay showing
    for (i, j) in [(0, 5), (0, 6), (1, 4)]:
        g.set(i, j, 2, 0)
    for (i, j) in [(0, 5), (0, 6), (1, 4)]:
        g.set(i, j, 1, "porcelain_mid")
    g.set(0, 7, 2, "porcelain")
    g.set(1, 3, 2, "porcelain")
    # the candle: r = 3 pillar, z 2..11, tunnelled top with a standing wall on one side
    body = _disc(g, C, C, 3)
    for z in range(2, T + 1):
        _layer(g, body, z, "cream")
    rim = _ring(g, C, C, 3)
    inner = [c for c in body if c not in rim]
    _layer(g, inner, T, 0)
    _layer(g, inner, T - 1, "cream_mid")                         # pooled wax in the hollow
    _layer(g, rim, T, "cream_hi")                                # lip of the tunnel
    for (i, j) in [(8, 5), (9, 5), (9, 6), (8, 4)]:
        if (i, j) in rim:
            g.set(i, j, T + 1, "cream_hi")                       # a wall of wax left standing
    g.set(6, 6, T, "charcoal")                                   # wick (unlit)
    g.set(7, 7, T - 1, "cream_shadow")                           # soot round the wick
    # drips down the camera side (painted onto the surface) ending in a puddle
    for (i, j, z0) in [(4, 8, 2), (5, 9, 7), (4, 6, 9)]:
        for z in range(z0, T + 1):
            g.paint(i, j, z, i, j, z, "cream_hi")
    for (i, j) in [(3, 8), (3, 9), (4, 9), (4, 10)]:
        g.set(i, j, 2, "cream_hi")                               # wax puddle
    # spent match
    g.box(8, 10, 2, 10, 10, 2, "pine_hi")
    g.set(7, 10, 2, "char")
    return g


# =====================================================================================
# Cooking and fire
# =====================================================================================
@model("camping_stove",
       story="The family's green two-burner camp stove, lid propped up as a windshield on "
             "the back step. It runs off a small propane bottle on a rubber hose; one burner "
             "is crusted from a pot that boiled over.",
       details=["Green enamelled case, the lid up with its two side flaps folded forward",
                "Two burners under a wire grate, front control knobs",
                "Small propane bottle with a brass regulator and a hose to the side inlet",
                "Boil-over crust around the left burner"],
       exclusions=["No flames", "No brand or warning labels"],
       notes=["Two-burner suitcase camping stove, lid up as windshield, hose to a small gas "
              "cylinder.",
              "Wider and taller than the reference: two burners need ~0.18 m between centres "
              "and the raised lid is as tall as the case is deep; the bottle stands beside."],
       collision_hint="Box 0.35 x 0.25 x 0.08 m for the case; lid, flaps and bottle as "
                      "separate boxes if needed.")
def camping_stove():
    g = Grid(20, 12, 13)
    SX0, SX1, SY0, SY1 = 6, 19, 0, 9                             # case
    g.box(SX0, SY0, 0, SX1, SY1, 2, "green")
    g.paint(SX0, SY0, 0, SX1, SY1, 0, "green_dark")
    g.paint(SX0, SY1, 2, SX1, SY1, 2, "green_hi")                # catch-light on the front lip
    g.box(SX0 + 1, SY0 + 1, 2, SX1 - 1, SY1 - 1, 2, "steel_light")  # drip tray
    # burners and their crust
    for bx in (9, 16):
        g.box(bx - 1, 4, 3, bx + 1, 6, 3, "iron")
        g.set(bx, 5, 3, "black")
    for (x, y) in [(7, 4), (7, 5), (8, 7), (9, 7), (7, 6), (10, 7)]:
        g.paint(x, y, 2, x, y, 2, "card_deep")                   # boil-over crust
    # wire grate over both burners
    for y in (2, 8):
        g.box(SX0 + 1, y, 4, SX1 - 1, y, 4, "steel_dark")
    for x in (SX0 + 1, 12, 13, SX1 - 1):
        g.box(x, 2, 4, x, 8, 4, "steel_dark")
    for (x, y) in [(SX0 + 1, 2), (SX0 + 1, 8), (SX1 - 1, 2), (SX1 - 1, 8), (12, 2), (13, 8)]:
        g.set(x, y, 3, "steel_dark")                             # grate feet
    # front control knobs
    for kx in (9, 16):
        g.box(kx, SY1 + 1, 1, kx, SY1 + 1, 1, "black")
        g.set(kx, SY1 + 1, 2, "steel_light")
    # lid up at the back: green rim, stainless inside; side flaps folded forward
    g.box(SX0, SY0, 3, SX1, SY0, 12, "steel_light")
    g.paint(SX0, SY0, 3, SX0, SY0, 12, "green")
    g.paint(SX1, SY0, 3, SX1, SY0, 12, "green")
    g.paint(SX0, SY0, 12, SX1, SY0, 12, "green")
    g.paint(SX0 + 1, SY0, 4, SX1 - 1, SY0, 6, "steel")           # scorched low on the shield
    g.paint(SX0 + 3, SY0, 4, SX0 + 5, SY0, 5, "iron_edge")
    for fx in (SX0, SX1):
        g.box(fx, SY0 + 1, 3, fx, SY0 + 4, 9, "green")
        g.paint(fx, SY0 + 4, 3, fx, SY0 + 4, 9, "green_dark")
    g.set(SX0 + 2, SY0, 12, "green_dark")                        # lid latch
    g.set(SX1 - 2, SY0, 12, "green_dark")
    # propane bottle beside the -X end, regulator and hose to the side inlet
    pb = (2.5, 6.5)
    for z in range(0, 8):
        _layer(g, _disc(g, pb[0], pb[1], 2.5), z, "galv")
    _layer(g, _disc(g, pb[0], pb[1], 1.5), 8, "galv")
    _layer(g, _ring(g, pb[0], pb[1], 2.5), 0, "galv_dark")
    for z in (3, 4, 5):
        _layer(g, _ring(g, pb[0], pb[1], 2.5), z, "label_blue")  # plain label band
    g.box(2, 6, 9, 2, 6, 9, "brass")                             # valve
    g.box(3, 6, 9, 4, 6, 9, "brass_dark")                        # regulator
    hose = [(5, 6, 9), (5, 6, 8), (5, 7, 8), (5, 7, 7), (5, 8, 7), (5, 8, 6), (5, 8, 5),
            (5, 8, 4), (5, 8, 3), (5, 8, 2), (5, 8, 1), (5, 7, 1)]
    for (x, y, z) in hose:
        g.set(x, y, z, "black")
    g.set(5, 6, 1, "brass")                                      # inlet fitting
    return {"grid": g, "footprint_cells": ((SX0, SX1), (SY0, SY1))}


@model("improvised_forge",
       story="Built in the garage after the outage by a neighbour who used to weld: a car "
             "brake drum on a steel-pipe stand, a furnace blower on an extension lead and a "
             "sheet of scrap steel as a heat shield. A length of rail is the anvil.",
       details=["Brake drum firepot with a charcoal bed (unlit) in its own ash",
                "Tuyere pipe down through the table to a capped ash dump",
                "Salvaged squirrel-cage blower on the lower shelf, taped joint, cable",
                "Scorched scrap-steel heat shield at the back",
                "Rail-section anvil and long tongs on the table; charcoal sack below"],
       exclusions=["No glowing coals or fire", "No fantasy anvil or bellows"],
       notes=["Brake-drum forge welded onto a steel-pipe stand, an air pipe to a small blower, "
              "charcoal bed, tongs; workshop junk, not fantasy."])
def improvised_forge():
    g = Grid(22, 14, 23)
    TX0, TX1, TY0, TY1, TZ = 2, 19, 1, 12, 14
    # pipe legs, feet and rails
    for (lx, ly) in [(TX0, TY0), (TX1, TY0), (TX0, TY1), (TX1, TY1)]:
        g.box(lx, ly, 1, lx, ly, TZ - 1, "steel_dark")
        g.set(lx, ly, 0, "iron")
    for y in (TY0, TY1):
        g.box(TX0, y, 3, TX1, y, 3, "steel_dark")
    for x in (TX0, TX1):
        g.box(x, TY0, 3, x, TY1, 3, "steel_dark")
    g.box(TX0 + 1, TY0 + 1, 3, TX1 - 1, TY1 - 1, 3, "iron")     # lower shelf plate
    # table plate with a scaled zone round the drum
    g.box(TX0, TY0, TZ, TX1, TY1, TZ, "iron")
    g.paint(TX0, TY1, TZ, TX1, TY1, TZ, "iron_edge")              # front edge catch-light
    g.paint(4, 11, TZ, 6, 12, TZ, "iron")
    for (x, y) in [(4, 11), (5, 11), (6, 11), (5, 12), (4, 10)]:
        g.paint(x, y, TZ, x, y, TZ, "rust_deep")                 # scale knocked off the work
    # brake drum firepot (r 3.5 -> 7 cells), flange, ribs, charcoal bed in ash
    DC = (8.5, 6.5)
    _layer(g, _disc(g, DC[0], DC[1], 4.0), TZ + 1, "iron_warm")   # hub flange
    for z in range(TZ + 2, TZ + 5):
        _layer(g, _ring(g, DC[0], DC[1], 3.5), z, "rust_deep")
    _layer(g, _ring(g, DC[0], DC[1], 3.5), TZ + 2, "iron_warm")   # heat-scaled lower band
    for (i, j) in _ring(g, DC[0], DC[1], 3.5):
        if i <= 6 and j >= 6:
            g.set(i, j, TZ + 3, "rust_dark")                     # weather side rusting
    wall = _ring(g, DC[0], DC[1], 3.5)
    bed = [c for c in _disc(g, DC[0], DC[1], 3.5) if c not in wall]
    _layer(g, bed, TZ + 2, "ash_dark")
    for (i, j) in bed:
        h = hash01(i, j, seed=7)
        g.set(i, j, TZ + 3, "char" if h < 0.45 else ("coal" if h < 0.7 else "soot"))
    for (i, j) in [(8, 6), (8, 7), (9, 6)]:
        g.set(i, j, TZ + 4, "char")                              # heaped in the middle
    for (i, j) in _ring(g, DC[0], DC[1], 3.5):
        if j >= 8:
            g.set(i, j, TZ + 4, "soot")                          # sooted lip at the front
    # tuyere down through the table, tee, ash dump cap, air pipe to the blower
    g.box(8, 6, 8, 8, 6, TZ, "iron")
    g.box(8, 6, 6, 8, 6, 7, "steel_dark")                         # ash dump, capped
    g.set(8, 6, 5, "steel")
    g.box(5, 6, 9, 7, 6, 9, "iron")
    g.box(4, 6, 8, 4, 6, 9, "galv_hi")                            # taped joint
    # furnace blower on the shelf
    g.box(3, 4, 4, 5, 8, 7, "beige_dark")
    g.paint(3, 4, 7, 5, 8, 7, "beige")
    g.box(3, 8, 4, 5, 8, 6, "beige")
    g.box(4, 3, 5, 4, 3, 6, "charcoal")                           # motor at the back
    g.box(3, 4, 4, 3, 8, 4, "rust_deep")
    g.box(1, 5, 4, 2, 5, 4, "black")                              # cable off the shelf
    g.box(1, 5, 0, 1, 5, 3, "black")
    g.box(0, 5, 0, 0, 9, 0, "black")
    g.box(1, 9, 0, 3, 9, 0, "black")
    # charcoal sack on the shelf
    g.box(12, 4, 4, 16, 9, 8, "card")
    g.paint(12, 4, 8, 16, 9, 8, "card_hi")
    g.box(13, 5, 9, 15, 8, 9, "card_dark")                        # folded-over top
    g.paint(12, 9, 4, 16, 9, 5, "card_dark")
    g.paint(12, 9, 6, 16, 9, 6, "card_deep")                      # sagging fold
    # scrap steel heat shield across the back, scorched above the drum
    g.box(TX0, 0, TZ, TX1, 0, TZ + 7, "galv")
    for x in range(TX0, TX1 + 1, 2):
        g.paint(x, 0, TZ + 1, x, 0, TZ + 7, "galv_dark")         # corrugations
    g.paint(5, 0, TZ + 1, 11, 0, TZ + 4, "iron_warm")
    g.paint(6, 0, TZ + 1, 10, 0, TZ + 3, "soot")
    g.paint(7, 0, TZ + 5, 9, 0, TZ + 5, "iron_warm")
    g.paint(TX1, 0, TZ + 6, TX1, 0, TZ + 7, "rust_dark")
    # rail-section anvil and tongs
    g.box(14, 3, TZ + 1, 18, 7, TZ + 1, "iron")                   # rail foot
    g.box(14, 4, TZ + 2, 18, 6, TZ + 2, "iron")                   # web
    g.box(14, 4, TZ + 3, 18, 6, TZ + 3, "iron_edge")              # head
    g.paint(15, 4, TZ + 3, 17, 6, TZ + 3, "steel")                # hammered face
    g.box(11, 10, TZ + 1, 18, 10, TZ + 1, "iron")                 # tongs
    g.box(12, 11, TZ + 1, 18, 11, TZ + 1, "iron")
    g.box(10, 10, TZ + 1, 11, 11, TZ + 1, "steel_dark")           # jaws
    g.set(12, 10, TZ + 1, "steel_dark")                           # rivet
    return {"grid": g, "footprint_cells": ((TX0, TX1), (TY0, TY1))}


@model("cooking_pot",
       story="A thin aluminium stockpot that has cooked every meal over the backyard fire "
             "since the outage. The bottom is black with soot, a dent on one side from being "
             "dropped, and the lid sits slightly crooked.",
       details=["30 cm stockpot with a rolled rim and riveted ear handles",
                "Soot climbing irregularly from the bottom",
                "A dent on the camera side", "Lid with a black knob, slightly askew"],
       exclusions=["No food or steam", "No brand stamp"],
       notes=["Battered aluminium stockpot with lid and two side handles, dented, soot-black "
              "on the bottom."])
def cooking_pot():
    g = Grid(14, 12, 11)
    C = (7.0, 6.0)
    _layer(g, _disc(g, C[0], C[1], 5.5), 0, "soot")
    outer = _ring(g, C[0], C[1], 6)
    for z in range(1, 8):
        _layer(g, outer, z, "galv")
    _layer(g, _disc(g, C[0], C[1], 5.5), 1, "iron_dark")         # inside bottom (unseen)
    _layer(g, outer, 7, "galv_hi")                               # rolled rim
    # soot climbing unevenly from the fire
    for (i, j) in outer:
        h = hash01(i, j, seed=3)
        top = 1 if h < 0.35 else (2 if h < 0.85 else 3)
        for z in range(1, top + 1):
            g.set(i, j, z, "soot" if z < top or z == 1 else "iron")
    # dent on the front-left: the wall pushed in one cell
    for (i, j, z) in [(2, 9, 4), (2, 9, 5), (3, 10, 5), (3, 10, 4)]:
        g.set(i, j, z, 0)
    for (i, j, z) in [(3, 9, 4), (3, 9, 5), (4, 9, 5), (4, 9, 4)]:
        g.set(i, j, z, "galv_dark")
    # ear handles on both sides
    for x, xo in ((0, 1), (13, 12)):
        g.box(x, 4, 4, x, 7, 6, "galv_dark")
        g.box(x, 5, 5, x, 6, 5, 0)
        g.set(xo, 4, 5, "steel_dark")                            # rivets
        g.set(xo, 7, 5, "steel_dark")
    # lid, knocked a cell to the side so a sliver of the dark inside shows
    lid = _disc(g, C[0] + 1, C[1], 6)
    _layer(g, lid, 8, "galv")
    _layer(g, _ring(g, C[0] + 1, C[1], 6), 8, "galv_hi")
    _layer(g, _disc(g, C[0] + 1, C[1], 4), 9, "galv")            # the lid's low crown
    _layer(g, [c for c in _disc(g, C[0], C[1], 5.5) if c not in lid], 7, "iron_dark")
    g.box(7, 5, 10, 8, 6, 10, "black")                           # knob
    g.set(7, 6, 10, "charcoal")
    return {"grid": g, "footprint_cells": ((1, 12), (0, 11))}


# =====================================================================================
# Water and fuel
# =====================================================================================
@model("water_barrel",
       story="A 200-litre food drum scrounged from the bakery, set on two cinder blocks by "
             "the back door. Someone drilled in a brass garden tap; it drips, and the drum "
             "and the block beneath are green where it does. A tin mug lives on the lid.",
       details=["Blue-grey plastic drum with two moulded rolling grooves",
                "Tight-head top with chime and two screw bungs, sun-faded",
                "Retrofitted brass tap low on the front, algae streak under it",
                "Two cinder blocks laid on their sides, cores showing",
                "Enamel mug left on the lid"],
       exclusions=["No hoses or pumps", "No hazard or food labels"],
       notes=["200 L blue-grey plastic drum on two cinder blocks with screw bungs and a "
              "retrofitted brass tap.",
              "Taller than the reference: a real 200 L drum is ~0.85 m on its own and the "
              "blocks add 0.2 m."])
def water_barrel():
    g = Grid(12, 14, 22)
    C = (6.0, 6.0)
    # two cinder blocks under the drum, cores running along X
    for (bx0, bx1) in ((0, 3), (8, 11)):
        g.box(bx0, 2, 0, bx1, 9, 3, "concrete")
        for (cy0, cy1) in ((3, 4), (7, 8)):
            g.clear(bx0, cy0, 1, bx1, cy1, 2)
        g.paint(bx0, 2, 3, bx1, 9, 3, "concrete_hi")
        g.paint(bx0, 2, 0, bx1, 9, 0, "concrete_dark")
    g.set(0, 9, 3, 0)                                            # chipped corner
    g.set(0, 9, 2, "concrete_dark")
    g.paint(0, 2, 0, 0, 9, 1, "concrete_dark")
    # drum: ring wall, two moulded grooves, closed base and top with chime
    Z0, Z1 = 4, 20
    outer, inner = _ring(g, *C, 6), _ring(g, *C, 5)
    grooves = (9, 15)
    for z in range(Z0, Z1 + 1):
        if z in grooves:
            _layer(g, inner, z, "bluegrey_dark")
        elif z - 1 in grooves or z + 1 in grooves:
            _layer(g, outer + inner, z, "bluegrey")
        else:
            _layer(g, outer, z, "bluegrey")
    _layer(g, _disc(g, *C, 6), Z0, "bluegrey_dark")
    _layer(g, _disc(g, *C, 5.5), Z1 - 1, "bluegrey_hi")          # recessed top
    _layer(g, outer, Z1, "bluegrey_hi")                          # chime
    _layer(g, outer, Z1 - 1, "bluegrey_hi")
    for z in (Z1 - 2, Z1 - 3):
        for (i, j) in outer:
            if j <= 6:
                g.set(i, j, z, "bluegrey_hi")                    # sun-faded shoulder (back)
    # screw bungs
    g.box(2, 5, Z1, 3, 6, Z1, "bluegrey_dark")
    g.set(2, 5, Z1, "bluegrey_deep")
    g.box(9, 7, Z1, 9, 7, Z1, "bluegrey_dark")
    # brass tap low on the front, algae streak and wet block under it
    g.box(5, 12, 6, 6, 12, 6, "brass_dark")
    g.box(5, 13, 6, 5, 13, 6, "brass")
    g.set(5, 13, 5, "brass")                                     # spout
    g.box(5, 12, 7, 5, 13, 7, "brass_hi")                        # handle
    for (x, z, c) in [(5, 5, "algae"), (6, 5, "algae_dark"), (5, 4, "algae_dark"),
                      (4, 5, "teal_dark"), (6, 4, "algae")]:
        g.paint(x, 11, z, x, 11, z, c)
    g.paint(4, 9, 3, 6, 9, 3, "concrete_dark")
    g.paint(5, 9, 3, 5, 9, 2, "moss_dark")
    # enamel mug left on the lid (same kitchen as the workbench mug)
    g.box(7, 3, Z1, 8, 4, Z1 + 1, "cream")
    g.paint(7, 3, Z1 + 1, 8, 4, Z1 + 1, "blue_dark")
    g.set(9, 4, Z1, "cream_mid")
    return {"grid": g, "footprint_cells": ((0, 11), (0, 11))}


@model("jerry_can",
       story="An army-surplus jerry can bought for camping, now the household's petrol "
             "reserve. The olive paint is chipped at every corner it has been dropped on, "
             "the centre handle is rubbed to bare steel, and rust has started on the base seam.",
       details=["Pressed steel body with the recessed X on both faces and a side seam",
                "Three handles on top, the centre one worn bare",
                "Cam-lever spout cap at the corner",
                "Chips at corners and edges, rust along the bottom seam"],
       exclusions=["No stencilled text or markings", "No spout attachment"],
       notes=["Steel jerry can in olive drab with the three-handle top and X-pressing, chipped "
              "paint."])
def jerry_can():
    g = Grid(14, 7, 19)
    X1, Y1, Z1 = 13, 6, 16
    body, dark, chip = "olive_dark", "green_deep", "steel"
    g.box(0, 0, 0, X1, Y1, Z1, body)
    for (x, y) in [(0, 0), (X1, 0), (0, Y1), (X1, Y1)]:
        g.clear(x, y, 0, x, y, Z1)                               # rounded vertical edges
    g.clear(0, 0, Z1, X1, 0, Z1)                                 # rounded top edges
    g.clear(0, Y1, Z1, X1, Y1, Z1)
    g.clear(0, 0, 0, X1, 0, 0)
    g.clear(0, Y1, 0, X1, Y1, 0)
    # side seam around the middle of the depth
    g.paint(0, 3, 0, 0, 3, Z1, dark)
    g.paint(X1, 3, 0, X1, 3, Z1, dark)
    g.paint(0, 3, Z1, X1, 3, Z1, dark)
    # recessed X on both broad faces
    for yf, yb in ((Y1, Y1 - 1), (0, 1)):
        for t in range(0, 29):
            x = 1 + round(t * 11 / 28)
            z = 1 + round(t * 14 / 28)
            for (xx, zz) in ((x, z), (X1 - x, z)):
                g.clear(xx, yf, zz, xx, yf, zz)
                g.set(xx, yb, zz, dark)
        g.paint(1, yf, 1, X1 - 1, yf, 1, body)
    # handles: three openings along the top ridge, centre bar worn bare
    for px in (3, 6, 9, 12):
        g.box(px, 3, Z1 + 1, px, 3, Z1 + 1, body)
    g.box(3, 3, Z1 + 2, 12, 3, Z1 + 2, body)
    g.paint(7, 3, Z1 + 2, 8, 3, Z1 + 2, "steel_light")
    g.paint(6, 3, Z1 + 2, 9, 3, Z1 + 2, "steel")
    g.paint(7, 3, Z1 + 2, 8, 3, Z1 + 2, "steel_light")
    # spout with cam-lever cap at the -X corner
    g.box(0, 2, Z1 + 1, 1, 4, Z1 + 1, "steel_dark")
    g.box(0, 2, Z1 + 2, 1, 4, Z1 + 2, body)
    g.set(2, 3, Z1 + 2, "steel_dark")                            # cam lever
    # chipped paint at corners and edges, rust along the base seam
    chips = [(1, Y1, Z1), (X1 - 1, Y1, Z1), (0, 1, Z1 - 1), (0, Y1 - 1, 12), (X1, 1, 14),
             (1, Y1, 0 + 1), (X1 - 1, Y1, 1), (0, 2, 6), (X1, Y1 - 1, 9), (2, Y1, Z1 - 1)]
    for (x, y, z) in chips:
        g.paint(x, y, z, x, y, z, chip)
    for x in range(1, X1):
        if hash01(x, seed=11) < 0.55:
            g.paint(x, Y1, 1, x, Y1, 1, "rust_deep")
    g.paint(2, Y1, 1, 3, Y1, 1, "rust_dark")
    g.paint(1, 1, 0, X1 - 1, Y1 - 1, 0, "rust_deep")
    g.paint(0, 1, 1, 0, Y1 - 1, 1, "rust_dark")
    return g


@model("water_bottle",
       story="One of the last sealed bottles from the corner shop's stockroom, still full "
             "and unopened.",
       details=["Full 1.5 L bottle: water level just under the shoulder",
                "Ribbed waist, plain cream label band with one blue stripe",
                "Blue screw cap above a neck collar"],
       exclusions=["No brand text", "No transparency (opaque stylisation)"],
       notes=["1.5 L plastic bottle in pale blue-grey (opaque stylisation), cap, ribbed waist, "
              "plain label band.",
              "8.75 cm diameter (7 cells, a clean pixel circle) is the real size of a "
              "1.5 L bottle; the reference's 10 cm is a coarse-cell size."])
def water_bottle():
    g = Grid(7, 7, 23)
    C = (3.5, 3.5)
    prof = {0: 2.5}
    for z in range(1, 17):
        prof[z] = 3.5
    prof.update({6: 2.5, 8: 2.5, 17: 2.9, 18: 2.5, 19: 1.5, 20: 2.5, 21: 1.5, 22: 1.5})
    for z, r in prof.items():
        _layer(g, _disc(g, *C, r), z, "bottle")
    for z in range(10, 15):
        _layer(g, _disc(g, *C, 3.5), z, "label_cream")
    _layer(g, _disc(g, *C, 3.5), 12, "label_blue")
    for z in (16, 17, 18, 19, 20):
        _layer(g, _disc(g, *C, prof[z]), z, "bottle_hi")         # air above the water line
    for z in (6, 8):
        _layer(g, _disc(g, *C, 2.5), z, "bluegrey_hi")           # ribs read darker
    _layer(g, _disc(g, *C, 2.5), 0, "bluegrey")                  # base, petaloid feet
    _layer(g, _disc(g, *C, 1.5), 21, "bottle_cap")               # cap
    _layer(g, _disc(g, *C, 1.5), 22, "bottle_cap")
    g.set(3, 3, 22, "blue_hi")
    return g


@model("fuel_container",
       story="The plastic petrol can from the lawnmower shelf. The red has faded to salmon "
             "where the sun hit it through the garage window; the flexible spout is clipped "
             "to its side, and a dribble of fuel has stained the front under the neck.",
       details=["Moulded plastic body with a hand loop along the top",
                "Threaded neck with cap and a small vent plug",
                "Flexible corrugated spout clipped to the side",
                "Sun-faded upper surfaces, a fuel dribble stain, scuffed base"],
       exclusions=["No warning text or brand moulding"],
       notes=["Faded red plastic gas can with a flexible spout clipped on."])
def fuel_container():
    g = Grid(14, 8, 19)
    X0, X1, Y1, Z1 = 1, 13, 7, 15
    g.box(X0, 0, 0, X1, Y1, Z1, "red")
    for (x, y) in [(X0, 0), (X1, 0), (X0, Y1), (X1, Y1)]:
        g.clear(x, y, 0, x, y, Z1)
    g.clear(X0, 0, Z1, X1, 0, Z1)
    g.clear(X0, Y1, Z1, X1, Y1, Z1)
    g.clear(X0, 0, Z1, X0, Y1, Z1)
    g.clear(X1, 0, Z1, X1, Y1, Z1)
    g.paint(X0, 0, Z1 - 1, X1, Y1, Z1, "red_hi")                 # sun-faded top
    g.paint(X0, Y1, 10, X1, Y1, Z1 - 1, "red_hi")
    g.paint(X0, 0, 0, X1, Y1, 1, "red_dark")                     # scuffed base
    g.paint(X0 + 1, Y1, 0, X1 - 1, Y1, 0, "red_deep")
    # moulded hand loop along the top
    for px in (3, 9):
        g.box(px, 3, Z1 + 1, px, 4, Z1 + 2, "red_hi")
    g.box(3, 3, Z1 + 3, 9, 4, Z1 + 3, "red_hi")
    g.paint(5, 3, Z1 + 3, 7, 4, Z1 + 3, "red")                   # hand-worn grip
    # neck and cap at the +X front corner, vent plug at the back
    g.box(10, 4, Z1 + 1, 12, 6, Z1 + 1, "red")
    g.box(10, 4, Z1 + 2, 12, 6, Z1 + 2, "charcoal")
    g.set(11, 5, Z1 + 2, "iron")
    g.set(2, 1, Z1, "charcoal")
    # fuel dribble down the front under the neck
    for z in range(8, Z1):
        g.paint(11, Y1, z, 11, Y1, z, "red_dark")
    g.paint(12, Y1, 11, 12, Y1, 13, "red_dark")
    # flexible spout clipped along the -X side
    for z in range(3, 13):
        g.set(0, 3, z, "charcoal" if z % 2 else "iron")
    g.box(0, 3, 13, 0, 3, 14, "iron")                            # nozzle
    g.box(0, 2, 1, 0, 4, 2, "black")                             # coupling nut
    for z in (5, 10):
        g.box(0, 2, z, 0, 2, z, "red_dark")                      # moulded clips
        g.box(0, 4, z, 0, 4, z, "red_dark")
    return {"grid": g, "footprint_cells": ((X0, X1), (0, Y1))}


# =====================================================================================
# Carry and power
# =====================================================================================
@model("backpack",
       story="An olive canvas pack, the same as the one the player carries: a foam sleeping "
             "mat strapped beneath it, a bottle in the side pocket, and the base scuffed grey "
             "from being dropped on gravel.",
       details=["Rounded canvas body with a top lid flap and two buckled straps",
                "Front pocket with a zip line", "Side mesh pocket with a water bottle",
                "Rolled foam mat strapped under the base", "Padded shoulder straps on the back"],
       exclusions=["No patches, logos or text", "No hanging gear clutter"],
       notes=["Olive canvas backpack (matches the player), rolled mat strapped on, side "
              "bottle pocket, scuffed base."],
       front_note="+Y is the outer face (pockets); the shoulder straps are on -Y.")
def backpack():
    g = Grid(17, 10, 22)
    BX0, BX1, BY0, BY1, BZ0, BZ1 = 1, 15, 1, 7, 5, 19
    canvas, dark, hi = "olive", "olive_dark", "olive_hi"
    # rolled foam mat under the base, along X, wider than the pack
    for x in range(0, 17):
        for (j, k) in g.disc_cells(4.5, 2.5, 2.5):
            g.set(x, j, k, "teal")
    for x in (0, 16):
        for (j, k) in g.ring_cells(4.5, 2.5, 2.5):
            g.set(x, j, k, "teal_dark")                           # rolled ends
        g.set(x, 4, 2, "teal_deep")
    g.paint(0, 0, 0, 16, 9, 0, "teal_dark")                      # dirty underside
    for sx in (3, 13):                                            # webbing straps round it
        for (j, k) in g.ring_cells(4.5, 2.5, 2.5):
            g.set(sx, j, k, "charcoal")
    # body: vertical sides, rounded corners, one soft crown
    g.box(BX0, BY0, BZ0, BX1, BY1, BZ1, canvas)
    for (x, y) in [(BX0, BY0), (BX1, BY0), (BX0, BY1), (BX1, BY1)]:
        g.clear(x, y, BZ0, x, y, BZ1)
    g.box(BX0 + 1, BY0 + 1, BZ1 + 1, BX1 - 1, BY1 - 1, BZ1 + 1, canvas)
    g.clear(BX0 + 1, BY0 + 1, BZ1 + 1, BX0 + 1, BY0 + 1, BZ1 + 1)
    g.clear(BX1 - 1, BY0 + 1, BZ1 + 1, BX1 - 1, BY0 + 1, BZ1 + 1)
    g.paint(BX0, BY0, BZ0, BX1, BY1, BZ0 + 1, dark)               # scuffed base
    for (x, z) in [(2, 5), (3, 5), (12, 5), (14, 6), (13, 5)]:
        g.paint(x, BY1, z, x, BY1, z, "khaki_dark")
    # lid flap over the top, hanging down the front, two buckled straps
    g.paint(BX0, BY0, BZ1, BX1, BY1, BZ1 + 1, hi)
    g.box(BX0 + 1, BY1 + 1, 15, BX1 - 1, BY1 + 1, BZ1, dark)
    g.paint(BX0 + 1, BY1 + 1, BZ1, BX1 - 1, BY1 + 1, BZ1, canvas)
    for sx in (4, 12):
        g.box(sx, BY1 + 2, 11, sx, BY1 + 2, 15, "charcoal")
        g.set(sx, BY1 + 2, 12, "iron")                            # buckle
    # front pocket with a zip line
    g.box(3, BY1 + 1, 6, 13, BY1 + 1, 13, canvas)
    g.paint(3, BY1 + 1, 6, 13, BY1 + 1, 6, dark)
    g.paint(3, BY1 + 1, 12, 13, BY1 + 1, 12, "charcoal")          # zip
    g.set(10, BY1 + 2, 12, "steel_light")                         # zip pull
    g.paint(3, BY1 + 1, 7, 3, BY1 + 1, 11, dark)
    g.paint(13, BY1 + 1, 7, 13, BY1 + 1, 11, dark)
    # side mesh pocket on -X with a bottle in it
    g.box(0, 2, 6, 0, 6, 11, dark)
    g.box(0, 3, 12, 0, 5, 14, "bottle")
    g.box(0, 4, 15, 0, 4, 15, "bottle_cap")
    g.paint(0, 2, 11, 0, 6, 11, "khaki_dark")                     # elastic hem
    # shoulder straps on the back and a grab loop
    for sx in (4, 11):
        g.box(sx, 0, 8, sx + 1, 0, 18, dark)
        g.set(sx, 0, 8, "iron")
    g.box(7, 2, BZ1 + 2, 9, 2, BZ1 + 2, "charcoal")
    return {"grid": g, "footprint_cells": ((BX0, BX1), (BY0, BY1))}


@model("basic_generator",
       story="A small open-frame petrol generator bought for camping trips. It now runs a "
             "few hours each evening for the fridge and lights; the tank paint is stained "
             "under the filler, the muffler has rusted, and oil has blackened the engine base.",
       details=["Black tube frame with carry loops at both ends",
                "Mustard fuel tank on top with filler cap and gauge",
                "Finned engine with the recoil pull-start on the camera side",
                "Alternator drum and an outlet panel with two sockets and a switch",
                "Rusted muffler, oily grime at the engine base"],
       exclusions=["No brand or warning stickers", "No fuel hose or extension leads"],
       notes=["Open-frame portable generator: tube frame, fuel tank on top, engine block, "
              "outlet panel, pull-start."])
def basic_generator():
    g = Grid(32, 22, 25)
    FX0, FX1, FY0, FY1, FZ = 1, 30, 1, 20, 23
    frame = "charcoal"
    # tube frame: base rails, end loops rising to carry bars
    for y in (FY0, FY1):
        g.box(FX0, y, 0, FX1, y, 0, frame)
    for x in (FX0, FX1):
        g.box(x, FY0, 0, x, FY1, 0, frame)
        for y in (FY0, FY1):
            g.box(x, y, 1, x, y, FZ - 1, frame)
        g.box(x, FY0 + 1, FZ, x, FY1 - 1, FZ, frame)
        g.set(x, FY0 + 1, FZ - 1, frame)                          # rounded bends
        g.set(x, FY1 - 1, FZ - 1, frame)
        g.paint(x, FY0 + 6, FZ, x, FY1 - 6, FZ, "iron_edge")      # rubbed carry grip
    g.box(FX0, FY0, 12, FX1, FY0, 12, frame)                      # side rails
    g.box(FX0, FY1, 12, FX1, FY1, 12, frame)
    for x in (8, 22):
        g.box(x, FY0, 0, x, FY1, 0, frame)                        # cross members
    for (x, y, z1) in [(8, 6, 1), (8, 15, 1), (22, 9, 2), (22, 12, 2)]:
        g.box(x, y, 1, x, y, z1, "black")                         # rubber mounts
    # engine block, cylinder head with fins, recoil starter on -X
    g.box(4, 5, 2, 14, 16, 10, "steel_dark")
    g.paint(4, 5, 2, 14, 16, 3, "soot")                           # oily base
    g.paint(4, 16, 4, 6, 16, 5, "iron")
    for z in range(11, 17):
        x0 = 6 + (z - 11) // 2
        g.box(x0, 7, z, 12, 14, z, "steel" if z % 2 else "iron")  # finned head
    g.cyl_x(10.5, 7.5, 3.5, 2, 3, "iron")                         # recoil housing
    g.cyl_x(10.5, 7.5, 2.5, 2, 2, "steel_dark")
    g.box(1, 10, 8, 1, 11, 8, "black")                            # T-handle at the frame
    g.box(1, 9, 9, 1, 12, 9, "black")
    g.set(2, 10, 8, "steel_light")                                # rope
    g.box(5, 15, 10, 9, 17, 13, "charcoal")                       # air filter box
    g.paint(5, 17, 11, 9, 17, 12, "iron")
    g.box(6, 17, 6, 7, 18, 7, "black")                            # choke lever
    # alternator drum and its end cap
    g.cyl_x(10.5, 8.5, 5.5, 15, 25, "steel")
    g.cyl_x(10.5, 8.5, 5.5, 25, 26, "steel_dark")
    for x in (17, 19, 21, 23):
        for (j, k) in g.ring_cells(10.5, 8.5, 5.5):
            if k >= 10:
                g.set(x, j, k, "steel_dark")                      # vent slots
    # outlet panel facing +Y
    g.box(15, 16, 3, 26, 19, 12, "iron")
    g.paint(15, 19, 3, 26, 19, 12, "charcoal")
    for ox in (16, 20):
        g.box(ox, 19, 5, ox + 2, 19, 8, "porcelain_shadow")       # sockets
        g.box(ox + 1, 19, 6, ox + 1, 19, 7, "black")
    g.box(24, 19, 9, 25, 19, 10, "black")                         # switch
    g.set(24, 19, 6, "steel_light")                               # breaker
    g.box(15, 19, 12, 26, 19, 12, "iron_edge")
    # muffler, rusted, at the back right
    g.box(19, 2, 13, 28, 5, 16, "rust_dark")
    for x in range(20, 28, 2):
        g.paint(x, 2, 14, x, 2, 15, "rust_deep")
    g.box(29, 3, 14, 29, 4, 15, "soot")                           # outlet
    # fuel tank on top: rounded, filler cap, gauge, stain under the filler
    g.box(5, 3, 17, 27, 18, 21, "mustard")
    for (x, y) in [(5, 3), (27, 3), (5, 18), (27, 18)]:
        g.clear(x, y, 17, x, y, 21)
    g.box(6, 4, 22, 26, 17, 22, "mustard")
    g.paint(5, 3, 17, 27, 18, 17, "mustard_dark")                 # lower seam
    g.paint(6, 4, 22, 26, 17, 22, "mustard_hi")
    g.box(9, 9, 23, 11, 11, 23, "black")                          # filler cap
    g.set(10, 10, 24, "charcoal")
    g.box(20, 10, 23, 21, 11, 23, "glass_dark")                   # fuel gauge
    g.set(20, 11, 23, "steel_light")
    for (x, y, z) in [(8, 9, 22), (8, 10, 22), (12, 11, 22), (9, 12, 22), (8, 11, 22)]:
        g.paint(x, y, z, x, y, z, "mustard_dark")                 # fuel spill stain
    g.paint(5, 7, 18, 5, 9, 21, "mustard_dark")
    g.paint(5, 8, 19, 5, 8, 20, "mustard_deep")
    return {"grid": g, "footprint_cells": ((FX0, FX1), (FY0, FY1))}


@model("portable_battery",
       story="A portable power station a neighbour bought for camping and lent out after "
             "the outage. It charges from the generator and runs a lamp and the radio; a "
             "phone cable is still plugged into the front.",
       details=["Dark case with lighter vented end panels and catch-lit edges",
                "Rigid carry handle with a rubber grip",
                "Front panel: small dark display, two AC sockets, USB ports, power button",
                "A pale phone cable plugged in and trailing onto the floor"],
       exclusions=["No glowing display or LEDs", "No brand or text"],
       notes=["Portable power station: dark case, carry handle, outlet panel and a small dark "
              "display.",
              "Depth includes the phone cable trailing onto the floor; the case is 0.19 m."])
def portable_battery():
    g = Grid(26, 18, 19)
    X1, Y1, Z1 = 25, 14, 15
    g.box(0, 0, 0, X1, Y1, Z1, "charcoal")
    for (x, y) in [(0, 0), (X1, 0), (0, Y1), (X1, Y1)]:
        g.clear(x, y, 0, x, y, Z1)
    g.clear(0, 0, Z1, X1, 0, Z1)
    g.clear(0, Y1, Z1, X1, Y1, Z1)
    # lighter end panels with vent slots
    for x0, x1 in ((0, 1), (X1 - 1, X1)):
        g.paint(x0, 0, 0, x1, Y1, Z1, "steel_dark")
        xs = x0 if x0 == 0 else x1
        for z in (4, 6, 8, 10):
            g.paint(xs, 3, z, xs, Y1 - 3, z, "black")
    # catch-lit top edges
    g.paint(2, 1, Z1, X1 - 2, 1, Z1, "iron_edge")
    g.paint(2, Y1 - 1, Z1, X1 - 2, Y1 - 1, Z1, "iron_edge")
    g.paint(2, Y1, Z1 - 1, X1 - 2, Y1, Z1 - 1, "iron_edge")
    # front panel
    g.paint(3, Y1, 2, X1 - 3, Y1, 12, "black")
    g.box(4, Y1, 8, 9, Y1, 11, "screen")                          # display
    g.paint(4, Y1, 11, 6, Y1, 11, "screen_sheen")
    g.set(4, Y1, 10, "screen_sheen")
    for ox in (12, 17):                                           # AC sockets
        g.box(ox, Y1, 4, ox + 3, Y1, 9, "steel")
        g.box(ox + 1, Y1, 6, ox + 1, Y1, 7, "black")
        g.box(ox + 2, Y1, 6, ox + 2, Y1, 7, "black")
    for uz in (3, 5):                                             # USB ports
        g.box(5, Y1, uz, 6, Y1, uz, "steel_dark")
        g.box(8, Y1, uz, 9, Y1, uz, "steel_dark")
    g.box(X1 - 4, Y1 + 1, 10, X1 - 3, Y1 + 1, 11, "steel_light")  # power button
    # rubber feet
    for (x, y) in [(3, 2), (X1 - 3, 2), (3, Y1 - 2), (X1 - 3, Y1 - 2)]:
        g.set(x, y, 0, "black")
    # rigid carry handle
    for hx in (4, X1 - 4):
        g.box(hx, 6, Z1 + 1, hx + 1, 8, 17, "charcoal")
    g.box(4, 6, 18, X1 - 3, 8, 18, "charcoal")
    g.paint(8, 6, 18, X1 - 7, 8, 18, "black")                     # rubber grip
    g.paint(4, 8, 18, X1 - 3, 8, 18, "iron_edge")
    # phone cable from a USB port down to the floor and away
    cable = [(5, Y1 + 1, 3), (5, Y1 + 2, 3), (5, Y1 + 2, 2), (5, Y1 + 2, 1), (5, Y1 + 2, 0),
             (4, Y1 + 2, 0), (3, Y1 + 2, 0), (3, Y1 + 3, 0), (2, Y1 + 3, 0), (1, Y1 + 3, 0),
             (1, Y1 + 2, 0), (0, Y1 + 2, 0)]
    for (x, y, z) in cable:
        g.set(x, y, z, "porcelain_mid")
    g.set(5, Y1 + 1, 3, "porcelain_deep")                         # plug
    return {"grid": g, "footprint_cells": ((0, X1), (0, Y1))}


@model("first_aid_box",
       story="The white first-aid box from the school corridor wall, its door hanging open "
             "after someone took the painkillers and most of the dressings in a hurry. A "
             "bandage roll, a bottle of iodine and a few gauze packs are left.",
       details=["White steel box, flat back for the wall, door hinged on the right",
                "Door ajar showing its muted red cross", "Shelf with leftover supplies; the "
                "right side cleared out", "Thumb-greyed catch on the free edge"],
       exclusions=["No text, brand or pharmacy marks", "No glowing or bright red"],
       notes=["Wall-mounted white steel first-aid box with a red cross, door ajar; wall-mount "
              "pivot.",
              "Depth includes the door swung ~20 degrees open."],
       front_note="+Y faces into the room; the back face is flat for the wall.",
       pivot_note="Bottom centre of the back (wall) face.",
       mount={"type": "wall", "recommended_bottom_height_m": 1.3},
       collision_hint="Box 0.375 x 0.11 x 0.225 m against the wall; the open door is an "
                      "overhang.")
def first_aid_box():
    W, D, H = 30, 9, 18
    g = Grid(W, 22, H)
    X1, F, Z1 = W - 1, D - 1, H - 1
    white, shade = "paint_white", "paint_white_shadow"
    g.box(0, 0, 0, X1, F, Z1, white)
    g.clear(1, 1, 1, X1 - 1, F, Z1 - 1)                           # open front
    g.paint(1, 0, 1, X1 - 1, 0, Z1 - 1, "porcelain_shadow")       # back inside
    g.paint(0, 0, 0, X1, F, 0, shade)
    g.box(1, 1, 8, X1 - 1, F - 1, 8, "porcelain_mid")             # shelf
    # leftovers on the left of the shelf, the right side emptied
    g.box(2, 3, 9, 5, 6, 12, "cream")                             # bandage roll
    g.paint(2, 3, 12, 5, 6, 12, "cream_hi")
    g.paint(3, 4, 12, 4, 5, 12, "cream_shadow")
    g.box(7, 3, 9, 8, 4, 14, "rust_deep")                         # iodine bottle
    g.box(7, 3, 15, 8, 4, 15, "charcoal")
    g.box(10, 2, 9, 13, 6, 9, "paper")                            # gauze packs
    g.box(10, 2, 10, 13, 6, 10, "porcelain")
    g.box(2, 2, 1, 7, 6, 2, "paper")                              # a box of plasters
    g.paint(2, 6, 1, 7, 6, 2, "label_blue")
    g.box(9, 3, 1, 10, 4, 4, "porcelain")                         # a tube
    g.box(13, 6, 1, 17, 6, 1, "steel")                            # scissors on the floor
    g.box(12, 5, 1, 12, 7, 1, "charcoal")
    # catch on the free (left) edge, greyed by thumbs
    g.box(0, F, 8, 0, F, 10, "steel_light")
    g.paint(0, F - 2, 7, 0, F, 11, shade)
    # door: hinged on the right edge, swung ~20 degrees open toward the room
    th = math.radians(20)
    hx, hy = X1 + 0.5, F + 0.5
    for t10 in range(0, (W) * 10 + 1, 2):
        t = t10 / 10
        for w in (0.0, 0.7):
            x = hx - t * math.cos(th) - w * math.sin(th)
            y = hy + t * math.sin(th) - w * math.cos(th)
            i, j = int(math.floor(x)), int(math.floor(y))
            if 0 <= i <= X1:
                g.box(i, j, 0, i, j, Z1, white)
    # muted red cross on the outer face, centred on the door
    door = {}
    for (i, j, k) in zip(*np.nonzero(g.v)):
        if j > F:
            door.setdefault(i, []).append(j)
    for i, js in door.items():
        t = (hx - (i + 0.5)) / math.cos(th)
        jmax = max(js)
        for k in range(0, H):
            in_v = abs(t - W / 2) <= 2.2 and 3 <= k <= 14
            in_h = abs(t - W / 2) <= 6.2 and 7 <= k <= 10
            if in_v or in_h:
                for j in js:
                    g.set(i, j, k, "signal_red_dark")
    g.paint(X1, F, 0, X1, 21, Z1, "steel_light")                  # hinge line
    g.paint(0, 0, 0, X1, 21, 0, shade)
    return {"grid": g, "pivot_cells": (W / 2, 0, 0)}
