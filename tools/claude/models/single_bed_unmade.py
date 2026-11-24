"""Claude_single_bed_unmade - generator (creator: Claude).

An ordinary dark-stained single bed with a slatted headboard, slept in and left: the
slate-blue duvet has been thrown back toward the foot (a soft rolled fold, the turned-
over flap and its hem), it slides off the side facing the camera (-X) in a long irregular drape
and tumbles over the low foot rail; the pillow is dented and skewed; a paperback lies
face-down on the sheet.

Front (+Y) is the accessible FOOT of the bed; the headboard is at -Y.
Cell size 0.05 m. X right, Y front, Z up. The mattress is a closed hollow shell.
"""
from voxkit import Grid, hash01

BASE_ID = "single_bed_unmade"
CATEGORY = "furniture"
NAME = "Unmade Single Bed"
CELL = 0.05

MZ0, MZ1 = 5, 8          # mattress cells; sleeping surface at 0.45 m
SURF = MZ1 + 1           # first cell above the mattress


def fold_y(x):
    """Head-side edge of the thrown-back duvet: a slightly bowed diagonal."""
    return 17 + (x * 4) // 19 + (1 if 6 <= x <= 11 else 0)


def build():
    g = Grid(22, 40, 15)

    # ---------------- frame: dark-stained hardwood ------------------------------
    for (px, py, top) in [(0, 0, 14), (19, 0, 14), (0, 38, 6), (19, 38, 6)]:
        g.box(px, py, 0, px + 1, py + 1, top, "wood_stain")
        g.box(px, py, top, px + 1, py + 1, top, "pine_dark")       # worn caps
        g.box(px, py, 0, px + 1, py + 1, 0, "wood_deep")
    # side rails, foot rail and the low footboard
    g.box(0, 2, 2, 0, 37, 4, "wood_stain")
    g.box(20, 2, 2, 20, 37, 4, "wood_stain")
    g.box(2, 39, 2, 18, 39, 5, "wood_stain")
    g.paint(2, 39, 5, 18, 39, 5, "pine_dark")                      # rubbed top edge
    g.box(1, 2, 2, 1, 37, 2, "wood_deep")                          # slat cleats
    g.box(19, 2, 2, 19, 37, 2, "wood_deep")
    for y in range(3, 38, 3):                                      # slats (hidden)
        g.box(1, y, 3, 19, y, 4, "pine_aged")
    # headboard: top rail, lower rail and four wide slats with gaps
    g.box(2, 0, 12, 18, 1, 13, "wood_stain")
    g.paint(2, 0, 13, 18, 1, 13, "pine_dark")
    g.box(2, 1, 7, 18, 1, 8, "wood_stain")
    for x0 in (3, 7, 11, 15):
        g.box(x0, 1, 9, x0 + 2, 1, 11, "wood_stain")
    g.paint(12, 1, 11, 13, 1, 11, "pine_dark")                     # a hand-worn patch

    # ---------------- mattress with fitted sheet (hollow shell) ------------------
    g.box(1, 2, MZ0, 19, 38, MZ1, "cream_deep")                    # ticking
    g.clear(2, 3, MZ0 + 1, 18, 37, MZ1 - 1)
    g.paint(1, 2, MZ1 - 1, 19, 38, MZ1, "cream_mid")               # sheet wraps the sides
    g.paint(1, 2, MZ1, 19, 38, MZ1, "cream")                       # sheet top
    # ---------------- pillow: puffy, lopsided (stuffing pushed to one end) -----
    x0, x1, y0, y1 = 5, 17, 3, 10
    for z, c in [(SURF, "cream_mid"), (SURF + 1, "cream_hi")]:
        g.box(x0, y0, z, x1, y1, z, c)
        for (cx, cy) in [(x0, y0), (x1, y0), (x0, y1), (x1, y1)]:
            g.set(cx, cy, z, 0)                                     # rounded corners
    g.box(x1 - 5, y0 + 1, SURF + 2, x1 - 1, y1 - 1, SURF + 2, "cream_hi")   # bunched end
    for (cx, cy) in [(x1 - 5, y0 + 1), (x1 - 1, y0 + 1), (x1 - 5, y1 - 1), (x1 - 1, y1 - 1)]:
        g.set(cx, cy, SURF + 2, 0)
    for (cx, cy) in [(8, 5), (9, 5), (8, 6), (9, 6), (8, 7), (9, 7), (10, 6)]:
        g.set(cx, cy, SURF + 1, 0)                                  # head hollow, 5 cm deep
        g.set(cx, cy, SURF, "cream_hi")
    g.set(x0, y1 - 1, SURF + 1, 0)                                  # flattened front corner
    g.set(x0 + 1, y1, SURF + 1, 0)

    # ---------------- paperback, face-down on the sheet --------------------------
    g.box(14, 13, SURF, 18, 15, SURF, "ochre_dark")
    g.box(16, 13, SURF, 16, 15, SURF, "wood_stain")                # spine
    g.box(14, 15, SURF, 18, 15, SURF, "paper")                     # page edges

    # ---------------- duvet (slate blue) -----------------------------------------
    for x in range(1, 20):
        f = fold_y(x)
        flap = 5 + (1 if 9 <= x <= 14 else 0) - (1 if x >= 17 else 0)   # wavy flap hem
        for y in range(f, 39):
            d = y - f
            if d == 0:                                             # soft rolled fold
                top = SURF + (1 if x in (1, 19) else 2)
                g.box(x, y, SURF, x, y, top, "blue")
                g.set(x, y, top, "blue_hi")
            elif d <= flap:                                        # turned-over flap
                g.box(x, y, SURF, x, y, SURF + 1, "blue_mid")
                g.set(x, y, SURF + 1, "blue_hi" if d == 1 else
                      ("blue_seam" if d == flap else "blue"))
            else:
                g.set(x, y, SURF, "blue")
    # short tuck over the far edge
    for y in range(fold_y(0) + 1, 39):
        g.set(0, y, SURF - 1, "blue_mid")
        g.set(0, y, SURF, "blue_mid")
    # the near side: the duvet slides off in a long drape
    for y in range(fold_y(19) + 2, 39):
        g.set(20, y, SURF, "blue")                                # over the edge
        g.box(20, y, MZ0, 20, y, MZ1, "blue_mid")                  # down the mattress side
        hem = 1 + (abs(y - 30) + 1) // 3 + (1 if hash01(y, seed=7) < 0.35 else 0)
        hem = max(1, min(hem, 4))
        g.box(21, y, hem, 21, y, 4, "blue_mid")                    # past the rail
        if y in (25, 26, 33, 34):                                  # vertical fold valleys
            g.paint(20, y, MZ0, 21, y, MZ1, "blue_dark")
            g.paint(21, y, hem, 21, y, 4, "blue_dark")
        elif y in (29, 30):                                        # fold crest
            g.paint(21, y, hem, 21, y, 4, "blue")
        g.set(21, y, hem, "blue_seam")                              # hem line
    # over the foot: tumbles onto the footboard, hem uneven
    for x in range(7, 21):
        low = 6 if 11 <= x <= 18 else 7
        g.box(x, 39, low, x, 39, SURF - 1, "blue_mid")
        g.set(x, 39, SURF, "blue")
        g.set(x, 39, low, "blue_seam")
    g.box(20, 38, SURF - 4, 21, 39, SURF, "blue_mid")              # corner bunch
    g.set(21, 39, SURF, 0)

    # Mirror so the long drape faces the default three-quarter game camera (-X side).
    g.v = g.v[::-1].copy()

    return {"grid": g, "cell": CELL, "footprint_cells": ((1, 21), (0, 39))}


META = {
    "story": ("Slept in and left in a hurry: the duvet thrown back toward the foot and "
              "sliding off the near side, pillow lopsided with the hollow of a head, a "
              "paperback left face-down on the sheet."),
    "resolution_tier": "detail",
    "resolution_rationale": (
        "0.05 m chosen to meet the brief's explicit 'avoid toy-like thickness'. At 0.10 m the "
        "thinnest possible duvet is 10 cm, the pillow is a single 10 cm slab, and the "
        "headboard slats and rails double in thickness; the cloth-versus-wood test fails. At "
        "0.05 m the duvet is a believable 5 cm layer with a rolled fold, turned-over flap, "
        "hem and side drape. The mattress is a closed hollow shell to avoid invisible fill."),
    "pivot_note": "Bottom centre of the frame footprint (1.05 x 2.00 m); the duvet drape adds "
                  "0.05 m on the -X side.",
    "front_note": "+Y is the FOOT of the bed (accessible end); the headboard is at -Y. The "
                  "long duvet drape faces -X, toward the default three-quarter camera.",
    "notes": ["Sleeping surface (mattress top) at 0.45 m; headboard posts 0.75 m.",
              "Single mattress 0.95 x 1.85 m; hidden slats are modelled for construction logic."],
    "attachments": {},
    "collision_hint": "Box 1.05 x 2.00 x 0.50 m plus a thin box for the headboard.",
}
