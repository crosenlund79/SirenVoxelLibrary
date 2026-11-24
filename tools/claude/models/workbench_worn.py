"""Claude_workbench_worn - generator (creator: Claude).

A home-built garage workbench: dark, grimy construction-pine frame under a thick
laminated plank top that has been polished pale along the front edge by forearms.
A painted cast-iron vise sits on the front-left corner (the user's right hand), a
hand saw hangs on that end, a sagging drawer is left half open, a hammer and a
forgotten enamel mug lie on top, and the lower shelf holds a red toolbox, a paint
tin and offcuts, one poking out past the end.

Cell size 0.05 m. Coordinates: X right, Y front (+Y), Z up; inclusive cell ranges.
"""
from voxkit import Grid

BASE_ID = "workbench_worn"
CATEGORY = "furniture"
NAME = "Worn Workbench"
CELL = 0.05

TOP0, TOP1 = 16, 17          # 10 cm laminated top; working surface at 0.90 m


def build():
    g = Grid(36, 18, 23)

    # ---------------- legs: 2x2 (10 x 10 cm) construction timber ----------------
    legs = [(2, 1), (30, 1), (2, 11), (30, 11)]
    for (lx, ly) in legs:
        g.box(lx, ly, 0, lx + 1, ly + 1, TOP0 - 1, "pine_dark")
        g.box(lx, ly, 0, lx + 1, ly + 1, 1, "wood_stain")       # floor grime
    # outer arris of the front legs rubbed lighter by knees and boots
    g.paint(2, 12, 4, 2, 12, 10, "pine_aged")
    g.paint(31, 12, 4, 31, 12, 8, "pine_aged")

    # ---------------- aprons (z 13..15), set back under the top -----------------
    g.box(4, 12, 13, 29, 12, 15, "pine_dark")    # front
    g.box(4, 1, 13, 29, 1, 15, "wood_stain")     # back
    g.box(2, 3, 13, 2, 10, 15, "pine_dark")      # left end
    g.box(31, 3, 13, 31, 10, 15, "pine_dark")    # right end
    for bx in (4, 29):                           # carriage-bolt heads (flush)
        g.set(bx, 12, 14, "steel_dark")

    # ---------------- lower shelf: rails z 2..3, boards z 4 ----------------------
    g.box(4, 12, 2, 29, 12, 3, "pine_dark")
    g.box(4, 1, 2, 29, 1, 3, "wood_stain")
    g.box(2, 3, 2, 2, 10, 3, "pine_dark")
    g.box(31, 3, 2, 31, 10, 3, "pine_dark")
    for (y0, y1), c in [((1, 3), "pine_aged"), ((5, 8), "pine_mid"), ((10, 12), "pine_aged")]:
        g.box(2, y0, 4, 31, y1, 4, c)
    for (lx, ly) in legs:                        # boards notched around the legs
        g.box(lx, ly, 4, lx + 1, ly + 1, 4, "pine_dark")

    # ---------------- back diagonal brace (2x4 on edge) --------------------------
    g.line((4, 1, 5), (29, 1, 11), "wood_stain")
    g.line((4, 1, 6), (29, 1, 12), "wood_stain")

    # ---------------- top: five laminated planks running along X ----------------
    planks = [((0, 2), "pine_mid"), ((3, 5), "pine_light"), ((6, 8), "pine_mid"),
              ((9, 10), "pine_light"), ((11, 13), "pine_light")]
    for (y0, y1), c in planks:
        g.box(0, y0, TOP0, 33, y1, TOP1, c)
    g.paint(0, 0, TOP0, 33, 13, TOP0, "pine_aged")       # underside / lower lamination
    g.paint(0, 0, TOP0, 0, 13, TOP1, "pine_aged")        # end grain reads darker
    g.paint(33, 0, TOP0, 33, 13, TOP1, "pine_aged")
    # front arris polished pale by forearms across the working zone
    g.paint(4, 13, TOP1, 29, 13, TOP1, "pine_hi")
    g.paint(4, 13, TOP0, 29, 13, TOP0, "pine_light")
    g.paint(9, 12, TOP1, 24, 12, TOP1, "pine_hi")
    # one broad grimy work zone around the vise (oil, filings, hand grime)
    for (sx, sy, c) in [(6, 9, "pine_mid"), (7, 9, "pine_mid"), (6, 10, "pine_mid"),
                        (7, 10, "pine_aged"), (8, 10, "pine_mid"), (6, 11, "pine_aged"),
                        (7, 11, "wood_stain"), (8, 11, "pine_aged"), (9, 11, "pine_mid"),
                        (7, 12, "pine_aged"), (8, 12, "pine_mid"), (5, 8, "pine_mid")]:
        g.set(sx, sy, TOP1, c)
    # two chips knocked out of the front edge
    for cx in (14, 25):
        g.set(cx, 13, TOP1, 0)

    # ---------------- back stop board -------------------------------------------
    g.box(5, 0, 18, 28, 0, 19, "pine_aged")
    g.paint(5, 0, 19, 28, 0, 19, "pine_mid")

    # ---------------- vise (front-left corner, overhanging the front edge) -------
    g.box(1, 8, 18, 5, 12, 18, "charcoal")       # swivel base, rounded
    for (cx, cy) in [(1, 8), (5, 8), (1, 12), (5, 12)]:
        g.set(cx, cy, 18, 0)
    g.set(1, 10, 18, "steel_hi")                # bolt heads
    g.set(5, 10, 18, "steel_hi")
    g.box(2, 9, 19, 4, 12, 20, "bluegrey")      # body + fixed jaw
    g.box(2, 9, 21, 4, 10, 21, "steel_dark")     # anvil pad
    g.box(2, 12, 20, 4, 12, 21, "steel_light")   # hardened jaw plate
    g.box(2, 13, 19, 4, 13, 19, "bluegrey_dark")  # slide beam under the jaw gap
    g.box(2, 14, 19, 4, 15, 21, "bluegrey")      # moving jaw
    g.box(2, 14, 20, 4, 14, 21, "steel_light")
    g.box(3, 16, 19, 3, 16, 20, "charcoal")      # screw boss
    g.box(3, 17, 20, 7, 17, 20, "steel_hi")      # T-handle slid to one side
    g.set(2, 17, 20, "charcoal")
    g.set(8, 17, 20, "charcoal")
    for (cx, cy, cz, c) in [(4, 15, 21, "steel_dark"), (2, 14, 19, "steel_dark"),
                            (4, 9, 19, "steel_dark"), (3, 16, 19, "rust_dark")]:
        g.set(cx, cy, cz, c)                      # chipped paint, a little rust

    # ---------------- hand saw hanging on the left-end apron ---------------------
    g.set(1, 6, 15, "steel_dark")                 # nail
    # D-handle (wood) with a hand hole
    g.box(1, 5, 12, 1, 7, 14, "red_dark")
    g.set(1, 6, 13, 0)
    # blade: straight back edge at y = 7..8, teeth edge tapering toward the tip
    for z in range(4, 12):
        y_lo = 4 + max(0, (11 - z) // 3)          # tapers from 4 cells to 2 cells wide
        g.box(1, y_lo, z, 1, 7, z, "steel_light")
        g.set(1, y_lo, z, "steel")                # tooth line
    g.set(1, 7, 11, "steel_hi")

    # ---------------- sagging drawer, pulled out ---------------------------------
    g.clear(19, 12, 13, 26, 12, 14)              # opening in the front apron
    for x in range(19, 27):
        sag = 1 if x >= 24 else 0                # broken runner: right end has dropped
        g.box(x, 14, 13 - sag, x, 14, 14 - sag, "pine_mid")
        g.box(x, 6, 13 - sag, x, 13, 13 - sag, "pine_aged")   # drawer bottom
    for side_x in (19, 26):
        sag = 1 if side_x >= 24 else 0
        g.box(side_x, 6, 14 - sag, side_x, 13, 14 - sag, "pine_aged")
    g.box(21, 15, 14, 23, 15, 14, "steel")       # pull
    g.set(19, 14, 14, "pine_light")              # worn corner

    # ---------------- claw hammer on the top -------------------------------------
    g.box(17, 11, 18, 22, 11, 18, "sawdust")     # hickory handle
    g.box(21, 11, 18, 22, 11, 18, "pine_aged")   # grimy grip end
    g.set(16, 10, 18, "charcoal")                # claw
    g.set(16, 11, 18, "charcoal")
    g.set(16, 12, 18, "steel_light")             # striking face

    # ---------------- enamel mug, left behind ------------------------------------
    g.box(27, 4, 18, 28, 5, 19, "cream")
    g.box(27, 4, 19, 28, 5, 19, "blue_dark")     # dark rim band
    g.box(29, 5, 18, 29, 5, 19, "cream_mid")     # handle

    # ---------------- shelf contents ---------------------------------------------
    g.box(6, 4, 5, 14, 8, 8, "red")              # red steel toolbox
    g.box(6, 4, 7, 14, 8, 7, "red_dark")         # lid seam
    g.box(6, 4, 8, 14, 8, 8, "red_hi")           # lid
    g.box(9, 6, 9, 11, 6, 9, "steel")            # handle
    g.set(8, 6, 9, "steel_dark")
    g.set(12, 6, 9, "steel_dark")
    g.set(7, 8, 7, "steel_hi")                   # latches
    g.set(13, 8, 7, "steel_hi")
    for (cx, cy, cz) in [(14, 8, 8), (6, 8, 5), (14, 4, 8)]:
        g.set(cx, cy, cz, "rust_dark")           # chipped corners
    # paint tin, 15 cm (a 4-cell "round" tin reads as a plus sign at this size)
    g.box(17, 6, 5, 19, 8, 8, "galv")
    g.paint(17, 6, 6, 19, 8, 7, "olive")         # label band
    g.paint(17, 6, 8, 19, 8, 8, "galv_hi")       # lid rim
    g.set(18, 8, 8, "olive_dark")                # drip down the front
    g.set(18, 8, 5, "olive_dark")
    g.box(22, 9, 5, 35, 11, 5, "pine_light")     # offcuts, one poking past the end
    g.box(24, 10, 6, 30, 11, 6, "pine_mid")
    g.paint(35, 9, 5, 35, 11, 5, "pine_aged")

    return {"grid": g, "cell": CELL, "footprint_cells": ((0, 33), (0, 13))}


META = {
    "story": ("Home-built garage bench used for years: forearm-polished front edge, a grimy "
              "work zone beside the painted vise, a drawer sagging on a broken runner, a mug "
              "left behind, a saw hung on the end and the shelf used as storage."),
    "resolution_tier": "detail",
    "resolution_rationale": (
        "0.05 m chosen deliberately over the suggested 0.10 m. A 0.10 m block-out read as a "
        "toy: top, shelf, apron and drawer all became 10 cm slabs (2-4x real timber) and the "
        "vise and the brief's tools collapsed into single cubes. At 0.05 m the 10 cm laminated "
        "top, 10x10 cm legs and 5 cm shelf boards match real construction timber and the vise "
        "jaws, T-handle, saw, hammer and drawer read at the three-quarter camera, while the "
        "occupied count stays far below the 10k furniture budget."),
    "pivot_note": "Bottom centre of the bench body footprint (1.70 x 0.70 m); vise, saw and "
                  "offcut overhangs are excluded from the footprint.",
    "front_note": "+Y is the working side (vise, drawer, polished edge).",
    "notes": ["Working surface at 0.90 m; vise top at 1.10 m.",
              "Vise overhangs the front edge by 0.20 m; one offcut pokes 0.10 m past the +X end.",
              "Hand saw hangs on the -X end apron; drawer pulled out 0.10 m with a 5 cm sag."],
    "attachments": {},
    "collision_hint": "Box 1.70 x 0.70 x 0.90 m at the pivot; optional small box for the vise.",
}
