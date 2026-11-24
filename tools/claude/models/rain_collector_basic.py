"""Claude_rain_collector_basic - generator (creator: Claude).

An improvised rain-water butt: a muted green plastic tank (tucked base, crisp rim,
one moulded groove) raised on a rough stand of silvered pallet boards and fence posts,
one leg levelled on a concrete block and a diagonal brace added later on the open side.
A newer post at the back carries the galvanised inlet pipe from the gutter (connection
end at the top-back) which drops through a collar into the lid. A brass tap with a red
lever overhangs the front edge so a can fits underneath; a grey PVC overflow runs down
the camera-facing side to a shoe at the ground; a canvas ratchet strap lashes the tank.
Rust only at nails, the strap buckle and the pipe bracket.

Cell size 0.05 m. X right, Y front (+Y), Z up. The tank is a hollow shell.
"""
from voxkit import Grid

BASE_ID = "rain_collector_basic"
CATEGORY = "survival"
NAME = "Basic Rain Collector"
CELL = 0.05

CX, CY = 11.0, 10.0      # tank axis on a cell boundary -> true 16-cell circle
R = 8.0
DECK = 10                # deck board layer (top surface at 0.55 m)


def build():
    g = Grid(21, 21, 32)

    # ---------------- stand ------------------------------------------------------
    posts = [(2, 0), (18, 0), (2, 16), (18, 16)]
    for (px, py) in posts:
        g.box(px, py, 0, px + 1, py + 1, DECK - 1, "wgrey_mid")
        g.box(px, py, 0, px + 1, py + 1, 0, "wgrey_deep")       # wet end grain
    # front-left leg was cut short and is levelled on a concrete block
    g.clear(2, 16, 0, 3, 17, 3)
    g.box(1, 15, 0, 4, 18, 3, "concrete")
    g.paint(1, 15, 3, 4, 18, 3, "concrete_hi")
    g.set(1, 18, 3, 0)                                           # chipped corner
    g.set(4, 18, 0, "concrete_dark")
    g.set(1, 15, 0, "concrete_deep")
    # beams under the deck and a low rail
    g.box(2, 0, DECK - 2, 19, 0, DECK - 1, "wgrey_dark")
    g.box(2, 17, DECK - 2, 19, 17, DECK - 1, "wgrey")
    g.box(2, 2, 3, 2, 15, 4, "wgrey_dark")
    g.box(19, 2, 3, 19, 15, 4, "wgrey_dark")
    g.box(4, 0, 3, 17, 0, 4, "wgrey_deep")
    g.line((2, 3, 5), (2, 14, 8), "wgrey")                       # brace added later
    g.line((2, 3, 4), (2, 14, 7), "wgrey")
    # deck: pallet boards of uneven widths running front to back, one broken short
    boards = [((1, 3), "wgrey"), ((5, 7), "wgrey_hi"), ((8, 10), "wgrey_mid"),
              ((12, 14), "wgrey_warm"), ((15, 17), "wgrey_hi"), ((18, 20), "wgrey")]
    for (x0, x1), c in boards:
        g.box(x0, 0, DECK, x1, 17, DECK, c)
    g.clear(12, 15, DECK, 14, 17, DECK)                          # snapped board end
    g.paint(12, 14, DECK, 14, 14, DECK, "wgrey_dark")
    # nail heads bleeding rust where boards cross the beams
    for (x, y) in [(2, 17), (19, 17)]:
        g.set(x, y, DECK, "rust_deep")

    # ---------------- the newer post carrying the inlet pipe ---------------------
    g.box(10, 0, 0, 11, 1, 29, "pine_aged")
    g.box(10, 0, 0, 11, 1, 2, "pine_dark")

    # ---------------- tank ---------------------------------------------------------
    z0, z1 = DECK + 1, 28
    # radius 8 gives a clean 16-cell pixel circle; rings are face-connected outlines
    outer = g.ring_cells(CX, CY, R)
    inner = g.ring_cells(CX, CY, R - 1.0)
    gz = z1 - 4                                                  # moulded groove layer
    g.cyl_z(CX, CY, R - 1.0, z0, z0, "green")                    # base tucked in one cell
    for z in range(z0 + 1, z1):
        if z == gz:
            cells, c = inner, "green_dark"                       # recessed groove, in shadow
        elif z in (z0 + 1, gz - 1, gz + 1):
            cells, c = outer + inner, "green"                    # doubled wall joins the steps
        else:
            cells, c = outer, "green"
        for (i, j) in cells:
            g.set(i, j, z, c)
    g.cyl_z(CX, CY, R, z1, z1, "green")                          # closed top
    # grime at the base, sun-faded crown
    g.paint(0, 0, z0, 20, 20, z0 + 1, "green_dark")
    g.paint(0, 0, z0, 20, 20, z0, "algae_dark")
    g.paint(0, 0, z1, 20, 20, z1, "green_light")
    # screw lid with a leaf screen
    g.cyl_z(CX, CY, 4.0, z1 + 1, z1 + 1, "green_dark")
    # ratchet strap lashing the tank round the post
    sz = z0 + 6
    for (i, j) in g.disc_cells(CX, CY, R):
        if g.get(i, j, sz) and (i + 0.5 - CX) ** 2 + (j + 0.5 - CY) ** 2 > (R - 1) ** 2:
            g.set(i, j, sz, "olive_dark")
    g.box(9, 0, sz, 12, 1, sz, "olive")                          # round the back post
    g.set(9, 0, sz, "olive_dark")
    g.set(12, 0, sz, "olive_dark")
    g.box(2, 9, sz, 2, 10, sz, "steel")                          # ratchet buckle
    g.set(2, 9, sz + 1, "steel_dark")
    g.set(2, 11, sz, "rust_dark")

    # ---------------- inlet: galvanised 10 cm pipe from the gutter ---------------
    g.box(10, 0, 30, 11, 8, 31, "galv")                          # runs forward over the lid
    g.paint(10, 0, 31, 11, 8, 31, "galv_hi")
    g.box(10, 0, 30, 11, 0, 31, "galv_dark")                     # coupler: gutter end
    g.box(9, 2, 30, 9, 2, 31, "steel_dark")                      # bracket strap
    g.box(12, 2, 30, 12, 2, 31, "steel_dark")
    g.set(12, 2, 30, "rust_dark")
    g.box(10, 9, 29, 11, 10, 31, "galv")                         # elbow dropping into the lid
    g.paint(10, 9, 31, 11, 10, 31, "galv_hi")
    for (x, y) in [(9, 9), (9, 10), (12, 9), (12, 10), (10, 11), (11, 11), (10, 8), (11, 8)]:
        g.set(x, y, z1 + 1, "galv_dark")                         # collar on the lid

    # ---------------- outlet tap overhanging the front edge -----------------------
    g.set(10, 18, z0 + 2, "brass_dark")                          # nipple through the wall
    g.box(10, 19, z0 + 1, 10, 19, z0 + 2, "brass")               # valve body
    g.set(10, 19, z0, "brass_dark")                              # spout
    g.set(10, 19, z0 + 3, "brass")                               # stem
    g.box(9, 19, z0 + 4, 11, 19, z0 + 4, "red")                  # lever handle
    g.set(9, 19, z0 + 4, "red_dark")
    g.paint(9, 16, DECK, 11, 17, DECK, "wgrey_wet")              # splash-darkened boards

    # ---------------- overflow: grey PVC down the -X side ------------------------
    oz = z1 - 2
    g.box(1, 10, oz, 2, 10, oz, "concrete_hi")                   # spigot through the wall
    g.box(0, 10, 1, 0, 10, oz, "concrete_hi")                    # down-pipe
    g.set(0, 10, oz, "concrete")                                 # elbow
    g.box(0, 11, 0, 0, 12, 0, "concrete_hi")                     # shoe turned forward
    g.set(0, 10, 0, "concrete_hi")
    g.set(0, 9, DECK, "steel_dark")                              # clip to the deck edge
    g.set(0, 11, DECK, "steel_dark")

    return {"grid": g, "cell": CELL, "footprint_cells": ((1, 20), (0, 17)),
            "inlet_connection_cell": (11.0, 0.0, 31.0)}


META = {
    "story": ("Built from what was lying around: pallet boards and fence posts, one leg "
              "propped on a concrete block, a fresher post added later to carry the inlet "
              "pipe, a ratchet strap so the tank survives the wind."),
    "resolution_tier": "detail",
    "resolution_rationale": (
        "Built first at the suggested 0.10 m and rejected after review: the 0.8 m tank is "
        "only 8 cells across, so its stair-stepped circle and lid broke into a lumpy block, "
        "and the tap, collar and brackets became stacked 10 cm cubes that read as a "
        "placeholder beside the rest of the batch. At 0.05 m the tank is a clean 16-cell pixel "
        "circle. The plumbing is kept deliberately chunky (inlet pipe 2x2 cells = 10 cm), so "
        "nothing is too thin to render."),
    "pivot_note": "Bottom centre of the timber stand footprint (1.00 x 0.90 m); the overflow "
                  "pipe (-X) and the tap (+Y) protrude beyond it.",
    "front_note": "+Y is the tap / service side.",
    "notes": ["Deck surface at 0.55 m; tank rim 1.45 m; inlet pipe top 1.60 m.",
              "Tap spout 0.55 m above the ground, overhanging the deck so a can fits below.",
              "The tank is a closed hollow shell (no water volume modelled)."],
    "attachments": {"gutter_inlet": {
        "description": "Open rear end of the galvanised 10 cm inlet pipe; a downpipe from "
                       "the gutter connects here (toward -Y).",
        "diameter_m": 0.10}},
    "collision_hint": "Cylinder r=0.40 m, h=1.45 m on a 1.0 x 0.9 x 0.55 m box.",
}
