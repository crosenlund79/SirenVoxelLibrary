"""Claude_dining_table - generator (creator: Claude).

A solid oak family dining table that has been used every day for years and looked after:
three wide top boards held square by breadboard ends, a plain apron, square legs on an
H-stretcher. Two places along the front edge are rubbed pale by forearms, a single dark
mug ring was never sanded out, and the centre stretcher is polished where feet rested.
Kept clean on purpose: crockery is a separate fine-tier model that can be set on top.

Cell size 0.05 m. Coordinates: X right, Y front (+Y), Z up; inclusive cell ranges.
Size 1.60 x 0.90 x 0.75 m (32 x 18 x 15 cells).
"""
from voxkit import Grid

BASE_ID = "dining_table"
CATEGORY = "furniture"
NAME = "Family Oak Dining Table"
CELL = 0.05
BATCH = "catalog_A"

NX, NY, NZ = 32, 18, 15
TOP = 14                       # 5 cm top board; top surface at 0.75 m
LEGS = [(1, 1), (29, 1), (1, 15), (29, 15)]   # 2x2-cell (10 x 10 cm) legs, min corner


def build():
    g = Grid(NX, NY, NZ)

    # ---- legs, with floor grime and one boot-scuffed foot ------------------------------
    for (lx, ly) in LEGS:
        g.box(lx, ly, 0, lx + 1, ly + 1, TOP - 1, "pine_mid")
        g.box(lx, ly, 0, lx + 1, ly + 1, 0, "pine_aged")
    g.paint(2, 16, 1, 2, 16, 2, "pine_light")          # front-left leg: scuffed outer arris

    # ---- apron (10 cm), flush with the legs' outer faces -------------------------------
    g.box(3, 16, 12, 28, 16, 13, "pine_mid")            # front
    g.box(3, 1, 12, 28, 1, 13, "pine_aged")             # back (less light, a little darker)
    g.box(1, 3, 12, 1, 14, 13, "pine_mid")              # left end
    g.box(30, 3, 12, 30, 14, 13, "pine_mid")            # right end
    g.paint(3, 16, 12, 28, 16, 12, "pine_aged")         # lower edge of the apron in shadow

    # ---- H-stretcher at ankle height ----------------------------------------------------
    g.box(1, 3, 3, 2, 14, 3, "pine_mid")                # side rails between the leg pairs
    g.box(29, 3, 3, 30, 14, 3, "pine_mid")
    g.box(3, 8, 3, 28, 9, 3, "pine_mid")                # centre rail
    g.paint(10, 8, 3, 21, 9, 3, "pine_light")           # polished where feet rested

    # ---- top: three boards along X, breadboard ends along Y ----------------------------
    g.box(2, 0, TOP, 29, 5, TOP, "pine_light")
    g.box(2, 6, TOP, 29, 11, TOP, "pine_mid")
    g.box(2, 12, TOP, 29, 17, TOP, "pine_light")
    g.box(0, 0, TOP, 1, 17, TOP, "pine_aged")           # breadboard ends: grain runs across
    g.box(30, 0, TOP, 31, 17, TOP, "pine_aged")
    for (x, y) in [(0, 0), (31, 0), (0, 17), (31, 17)]:  # softened corners
        g.set(x, y, TOP, 0)

    # ---- wear on the working (front) side: the arris is rubbed pale, not the whole top --
    for x0 in (6, 19):                                  # two everyday places
        g.paint(x0, 17, TOP, x0 + 5, 17, TOP, "pine_hi")
        g.paint(x0 + 1, 16, TOP, x0 + 4, 16, TOP, "pine_hi")
        g.paint(x0 + 1, 17, TOP - 2, x0 + 4, 17, TOP - 2, "pine_light")  # apron under hands
    g.set(14, 17, TOP, "pine_aged")                     # small dent in the front edge
    g.set(23, 6, TOP, "pine_aged")                      # faint ring on the middle board
    g.set(24, 6, TOP, "pine_aged")

    return {"grid": g, "cell": CELL, "footprint_cells": ((0, NX - 1), (0, NY - 1))}


META = {
    "story": ("An everyday family table, well used and looked after: forearm-polished places "
              "along the front, a faint mug ring nobody sanded out and a stretcher polished by "
              "restless feet. Left clean when the family went; plates and candles are separate "
              "models."),
    "condition": "used",
    "gameplay_use": "Dining-room furniture; a work and eating surface in the defended house; "
                    "cover/obstacle; set dressing for kitchen and dining scenes.",
    "silhouette": ("Broad flat top with breadboard ends over a plain apron and four square legs; "
                   "the H-stretcher reads through the legs from the three-quarter camera."),
    "details": ["Three top boards in alternating oak tones; breadboard ends with darker cross "
                "grain", "Two forearm-polished places on the front arris, a faint mug ring",
                "H-stretcher with a polished centre rail", "Floor grime on the feet, one "
                "scuffed leg"],
    "exclusions": ["No crockery or clutter baked onto the top (use Claude_crockery_set)",
                   "No random speckle noise; wear only where hands, mugs and feet go"],
    "resolution_tier": "detail",
    "resolution_rationale": (
        "0.05 m matches the other household furniture (pilot bed and workbench), so tables, "
        "chairs and beds share one voxel rhythm in a room. A 5 cm top, 10 cm legs and apron "
        "are real joinery sizes; at 0.10 m the top would be a 10 cm slab and the stretcher "
        "would disappear."),
    "pivot_note": "Bottom centre of the 1.60 x 0.90 m footprint.",
    "front_note": "+Y is the long side with the polished places; the table is symmetric "
                  "enough to be placed either way round.",
    "notes": ["Table height 0.75 m; knee clearance under the apron 0.60 m.",
              "Seats six: two per long side and one at each end."],
    "attachments": {},
    "collision_hint": "Box 1.60 x 0.90 x 0.75 m at the pivot (or four leg boxes + top slab).",
    "pairs_with": ["Claude_dining_chair", "Claude_crockery_set"],
}
