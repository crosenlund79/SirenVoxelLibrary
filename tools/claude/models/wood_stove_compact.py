"""Claude_wood_stove_compact - generator (creator: Claude).

A compact cast-iron box stove: splayed cast feet, plinth and top plates that overhang
the body, recessed cast side panels, a raised door with a soot-smoked window showing a
low bed of embers, hinge knuckles, a coil-spring latch handle, an ash-pan air slider,
a pot-polished hob ring and a hollow flue collar ready for a 15 cm pipe.

Cell size 0.05 m. X right, Y front (+Y), Z up. Interior is a real hollow firebox.
"""
from voxkit import Grid

BASE_ID = "wood_stove_compact"
CATEGORY = "survival"
NAME = "Compact Wood Stove"
CELL = 0.05


def build():
    g = Grid(16, 15, 20)

    # ---------------- feet: 15 cm cast legs, splayed at the floor ----------------
    for (lx, ly, ox, oy) in [(1, 1, -1, -1), (13, 1, 1, -1), (1, 10, -1, 1), (13, 10, 1, 1)]:
        g.box(lx, ly, 1, lx + 1, ly + 1, 2, "iron")
        fx0, fx1 = (lx + min(ox, 0), lx + 1 + max(ox, 0))
        fy0, fy1 = (ly + min(oy, 0), ly + 1 + max(oy, 0))
        g.box(fx0, fy0, 0, fx1, fy1, 0, "iron_dark")
        g.set(lx + (0 if ox < 0 else 1) + ox, ly + (0 if oy < 0 else 1) + oy, 0, 0)  # round toe
        g.set(lx + (0 if ox < 0 else 1), ly + (0 if oy < 0 else 1), 0, "rust_deep")

    # ---------------- plinth and top plates (overhang the body by 5 cm) ----------
    for z in (3, 16):
        g.box(0, 0, z, 15, 12, z, "iron")
        for (cx, cy) in [(0, 0), (15, 0), (0, 12), (15, 12)]:
            g.set(cx, cy, z, 0)                       # chamfered corners
    # catch-light along the plate edges
    for z in (3, 16):
        g.paint(1, 12, z, 14, 12, z, "iron_edge")
        g.paint(0, 1, z, 0, 11, z, "iron_edge")
    g.paint(1, 0, 16, 14, 0, 16, "iron_edge")
    g.paint(15, 1, 16, 15, 11, 16, "iron_edge")
    # raised round cooking lid on the front half of the top plate, rim polished by pots
    for y in range(6, 12):
        x0, x1 = (6, 9) if y in (6, 11) else (5, 10)
        g.box(x0, y, 17, x1, y, 17, "iron")
    g.set(7, 8, 17, "iron_deep")                     # lift-tool notch
    g.set(8, 8, 17, "iron_deep")

    # ---------------- body shell z 4..15 ----------------------------------------
    g.box(1, 1, 4, 14, 11, 15, "iron")
    g.clear(3, 2, 4, 12, 10, 15)                     # hollow firebox
    # recessed cast side panels: outer frame at x=1 / x=14, panel set back one cell
    for x_out in (1, 14):
        g.clear(x_out, 3, 6, x_out, 9, 13)
    g.paint(2, 3, 6, 2, 9, 13, "iron_dark")
    g.paint(13, 3, 6, 13, 9, 13, "iron_dark")
    # heat-tempered bronze tint and soot streak above the door
    g.paint(5, 11, 15, 10, 11, 15, "iron_warm")
    g.paint(7, 11, 15, 8, 11, 15, "soot")

    # ---------------- door: raised panel with smoked window ----------------------
    g.box(3, 12, 6, 12, 12, 14, "iron")
    g.paint(3, 12, 14, 12, 12, 14, "iron_edge")      # top edge catches light
    g.paint(12, 12, 6, 12, 12, 14, "iron_edge")
    g.clear(5, 12, 8, 10, 12, 12)                    # window opening
    g.box(5, 11, 8, 10, 11, 12, "iron_warm")         # soot-smoked glass (opaque)
    g.box(5, 11, 11, 10, 11, 12, "soot")
    g.box(5, 11, 8, 10, 11, 8, "ember_dark")         # ember bed glimpsed through glass
    g.set(7, 11, 8, "ember")
    g.set(8, 11, 8, "ember_hot")
    g.set(6, 11, 9, "ember_dark")
    g.set(8, 11, 9, "coal")
    # hinge knuckles on the +X side, latch + coil-spring handle on the -X side
    for z0 in (7, 12):
        g.box(13, 12, z0, 13, 12, z0 + 1, "steel_dark")
    g.set(2, 12, 10, "iron_edge")
    g.set(2, 13, 10, "steel")
    g.box(2, 14, 9, 2, 14, 11, "steel_hi")

    # ---------------- ash pan door with primary air slider ----------------------
    g.box(4, 12, 4, 11, 12, 5, "iron")
    g.clear(5, 12, 5, 6, 12, 5)
    g.clear(9, 12, 5, 10, 12, 5)
    g.paint(5, 11, 5, 6, 11, 5, "soot")
    g.paint(9, 11, 5, 10, 11, 5, "soot")
    g.box(7, 13, 4, 8, 13, 4, "steel")               # slider lever
    g.set(4, 12, 4, "rust_deep")                     # damp floor rust at the base
    g.set(11, 12, 3, "rust_deep")

    # ---------------- flue collar (15 cm pipe), hollow -------------------------
    # square bolted flange with a rounded pipe socket above it
    for z in (17, 18, 19):
        g.box(6, 1, z, 9, 4, z, "iron_dark")
        for (cx, cy) in [(6, 1), (9, 1), (6, 4), (9, 4)]:
            g.set(cx, cy, z, "steel_dark" if z == 17 else 0)       # bolt heads on the flange
        g.clear(7, 2, z, 8, 3, z)
    g.paint(6, 1, 19, 9, 4, 19, "iron_edge")         # machined rim
    g.clear(7, 2, 16, 8, 3, 16)                      # throat opens into the firebox
    g.set(6, 2, 17, "rust_deep")

    return {"grid": g, "cell": CELL, "footprint_cells": ((0, 15), (0, 12)),
            "flue_outlet_cell": (8.0, 3.0, 20.0)}


META = {
    "story": ("A squat cast-iron box stove in daily use: pot-polished lid, heat-bronzed iron "
              "and a soot streak above the door, a low bed of embers behind smoked glass, damp "
              "rust only where the feet meet the floor."),
    "resolution_tier": "detail",
    "resolution_rationale": (
        "0.05 m (detail tier) is essential here, as the brief allows. Every functional "
        "feature the brief lists is 2-5 cm in reality: hinge knuckles, latch handle, air "
        "slider slots, 15 cm feet and the 5 cm plate overhangs that give a cast stove its "
        "silhouette. At 0.10 m the 0.8 m body is only 8 cells wide and those features become "
        "whole 10 cm cubes, i.e. a generic furnace block. The firebox is genuinely hollow, so "
        "the count stays about 1.3k voxels."),
    "pivot_note": "Bottom centre of the plinth/top-plate footprint (0.80 x 0.65 m); the latch "
                  "handle and slider lever protrude a further 0.10 m at the front.",
    "front_note": "+Y is the loading door / interaction side.",
    "notes": ["Body (top plate) at 0.85 m, raised cooking lid to 0.90 m, flue collar rim at 1.00 m.",
              "Smoked window is opaque by design (no transparency needed); embers are the only "
              "warm accent.",
              "The firebox is a real hollow cavity reachable through the flue collar."],
    "attachments": {"flue_outlet": {
        "description": "Centre of the open top of the 15 cm flue collar; a vertical pipe "
                       "attaches here.",
        "diameter_m": 0.15}},
    "collision_hint": "Box 0.80 x 0.65 x 0.90 m at the pivot plus a 0.2 m cylinder for the collar.",
}
