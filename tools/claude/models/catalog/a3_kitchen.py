"""Batch A3 - kitchen (creator: Claude). X right, Y front (+Y), Z up; inclusive cells.

One kitchen: the base units (counter, sink), the cooker and the wall cabinet share the same
0.05 m rhythm so they line up in a run:
  * toe kick z 0-1 (10 cm, recessed 10 cm), carcass to z 16, worktop / cooktop at z 17
    (top surface 0.90 m), carcass front at y 9, door panels at y 10, door frames at y 11,
    worktop front edge and handles at y 12 (0.65 m deep overall);
  * sage painted shaker doors (1-cell frame, panel recessed one cell), slab drawer fronts,
    charcoal bar handles, an oiled pine worktop;
  * appliances use the shared off-white enamel family (porcelain ramp for white enamel,
    almond/cream for the older almond pieces) with seams, recessed panels and darker trim
    so they never read as flat white blocks.
Small kitchen items (crockery, pan, kettle, board) are separate fine/micro-tier pickups.
"""
from catalog_registry import model
from voxkit import Grid

# ---- shared kitchen rhythm (cells) -------------------------------------------------------
Y_CARC = 9          # carcass front face
Y_PANEL = 10        # recessed door panels / slab drawer backs
Y_FRAME = 11        # door frames / drawer fronts
Y_EDGE = 12         # worktop front edge, handles
Z_TOP = 17          # worktop / cooktop layer (top at 0.90 m)
HANDLE = "charcoal"


def _carcass(g, x0, x1):
    """Sage carcass with a recessed toe kick; the front face shows dark in the reveals."""
    g.box(x0, 0, 0, x1, Y_CARC, Z_TOP - 1, "sage")
    g.paint(x0 + 1, Y_CARC, 2, x1 - 1, Y_CARC, Z_TOP - 1, "sage_deep")
    g.paint(x0, Y_CARC, 0, x1, Y_CARC, 1, "sage_deep")          # toe kick board
    g.paint(x0, 0, 0, x1, Y_CARC - 1, 0, "sage_dark")            # floor grime line on sides


def _shaker_door(g, xa, xb, za, zb, frame="sage", panel="sage"):
    """Door: frame at Y_FRAME, panel recessed at Y_PANEL."""
    g.box(xa, Y_PANEL, za, xb, Y_PANEL, zb, panel)
    g.box(xa, Y_FRAME, za, xb, Y_FRAME, zb, frame)
    g.clear(xa + 1, Y_FRAME, za + 1, xb - 1, Y_FRAME, zb - 1)


def _drawer(g, xa, xb, za, zb, dy=0, handle=True, col="sage"):
    """Slab drawer front (two cells thick); dy > 0 pulls it out of the carcass."""
    g.box(xa, Y_PANEL + dy, za, xb, Y_FRAME + dy, zb, col)
    if dy:                                                      # drawer box sides show
        g.box(xa + 1, Y_PANEL, za, xa + 1, Y_PANEL + dy - 1, zb - 1, "pine_light")
        g.box(xb - 1, Y_PANEL, za, xb - 1, Y_PANEL + dy - 1, zb - 1, "pine_light")
    if handle:
        cx = (xa + xb) // 2
        g.box(cx - 1, Y_EDGE + dy, zb - 1, cx + 2 - ((xb - xa) % 2 == 0), Y_EDGE + dy, zb - 1,
              HANDLE)


def _worktop(g, x0, x1, holes=()):
    g.box(x0, 0, Z_TOP, x1, Y_EDGE, Z_TOP, "pine_light")
    g.paint(x0, 0, Z_TOP, x1, 2, Z_TOP, "pine_mid")              # oiled dark along the wall
    for (a, b, c, d) in holes:
        g.clear(a, b, Z_TOP, c, d, Z_TOP)


# =========================================================================================
@model("kitchen_counter", name="Kitchen Base Unit",
       story="The everyday prep counter beside the cooker. The left drawer, where the cutlery "
             "lived, was yanked open by someone looking for a knife and left out; the paint is "
             "rubbed through to the wood where hands pulled the doors for years.",
       details=["Two sage shaker doors under two slab drawers, charcoal bar handles",
                "Oiled pine worktop with a forearm-pale front edge in the work zone",
                "Recessed toe kick; carcass reveals read as dark grooves",
                "Left (cutlery) drawer pulled out 5 cm, its pine box sides showing",
                "Paint rubbed to bare wood beside the handles of the left door"],
       exclusions=["No baked-on clutter (board, kettle and crockery are separate pickups)"],
       notes=["Shares the kitchen run rhythm: worktop top 0.90 m, 0.65 m deep, same doors, "
              "handles and toe kick as Claude_kitchen_sink and Claude_wall_cabinet.",
              "Width 1.25 m (25 cells, two 0.60 m doors and a centre reveal) against GPT's "
              "1.26 m reference."])
def kitchen_counter():
    W = 25
    g = Grid(W, 15, 18)
    _carcass(g, 0, W - 1)
    # two drawers (z 13-16) over two doors (z 2-11); reveals at x 12 and z 12
    _drawer(g, 0, 11, 13, 16, dy=1)                               # cutlery drawer, left ajar
    _drawer(g, 13, W - 1, 13, 16)
    _shaker_door(g, 0, 11, 2, 11)
    _shaker_door(g, 13, W - 1, 2, 11)
    g.box(11, Y_EDGE, 7, 11, Y_EDGE, 10, HANDLE)                  # door handles at the meeting
    g.box(13, Y_EDGE, 7, 13, Y_EDGE, 10, HANDLE)
    # wear: paint rubbed through to the pine where fingers pull the left door
    g.paint(11, Y_FRAME, 4, 11, Y_FRAME, 6, "sage_hi")
    g.paint(11, Y_FRAME, 11, 11, Y_FRAME, 11, "sage_hi")
    g.paint(10, Y_FRAME, 11, 10, Y_FRAME, 11, "pine_mid")
    g.paint(11, Y_FRAME, 5, 11, Y_FRAME, 6, "pine_mid")
    g.paint(13, Y_FRAME, 5, 13, Y_FRAME, 6, "sage_hi")
    g.paint(0, Y_FRAME, 2, 1, Y_FRAME, 2, "sage_dark")            # kicked bottom corner
    # worktop with the work zone rubbed pale along the front edge
    _worktop(g, 0, W - 1)
    g.paint(3, Y_EDGE, Z_TOP, 14, Y_EDGE, Z_TOP, "pine_hi")
    return {"grid": g, "footprint_cells": ((0, W - 1), (0, Y_EDGE))}


# =========================================================================================
@model("kitchen_sink", name="Kitchen Sink Unit",
       story="The family washed up here every evening. The last water dried in the basin and "
             "left a brown tide ring round the drain; two plates are still standing in the rack "
             "where somebody left them to drain.",
       details=["Same sage shaker base as the counter, with a false drawer front",
                "Inset stainless basin and ribbed drainer in the pine worktop",
                "Swan-neck mixer tap with two cross-head valves",
                "Wire dish rack with two upright plates and a mug",
                "Dry brown tide ring and drip marks in the basin"],
       exclusions=["No running water or soap foam", "No brand on the tap"],
       notes=["Same rhythm as Claude_kitchen_counter (0.90 m worktop, 0.65 m deep); 1.05 m "
              "wide (21 cells, two doors and a centre reveal) against GPT's 1.00 m reference.",
              "Overall height 1.20 m is the tap; the worktop line is 0.90 m."])
def kitchen_sink():
    W = 21
    g = Grid(W, 15, 25)
    _carcass(g, 0, W - 1)
    _drawer(g, 0, W - 1, 13, 16, handle=False)                    # false (tilt) front
    g.paint(0, Y_FRAME, 13, W - 1, Y_FRAME, 13, "sage_dark")      # its lower lip in shade
    _shaker_door(g, 0, 9, 2, 11)
    _shaker_door(g, 11, W - 1, 2, 11)
    g.box(9, Y_EDGE, 7, 9, Y_EDGE, 10, HANDLE)
    g.box(11, Y_EDGE, 7, 11, Y_EDGE, 10, HANDLE)
    g.paint(8, Y_FRAME, 6, 9, Y_FRAME, 11, "sage_hi")             # hands worn the left door
    g.paint(0, Y_FRAME, 2, 9, Y_FRAME, 2, "sage_dark")            # splash-darkened bottom rails
    g.paint(11, Y_FRAME, 2, W - 1, Y_FRAME, 2, "sage_dark")
    # worktop with the basin opening (x 2-9, y 3-10) and the drainer (x 11-18)
    _worktop(g, 0, W - 1)
    bx0, bx1, by0, by1 = 2, 10, 3, 11                              # steel rim outer edge
    g.box(bx0, by0, Z_TOP, bx1, by1, Z_TOP, "steel_hi")           # rim
    g.box(bx0 + 1, by0 + 1, Z_TOP - 4, bx1 - 1, by1 - 1, Z_TOP - 1, "steel_light")
    g.clear(bx0 + 1, by0 + 1, Z_TOP - 3, bx1 - 1, by1 - 1, Z_TOP)  # basin, 0.20 m deep
    g.paint(bx0 + 1, by0 + 1, Z_TOP - 4, bx1 - 1, by1 - 1, Z_TOP - 4, "steel")  # basin floor
    cx, cy = (bx0 + bx1) // 2, (by0 + by1) // 2
    g.set(cx, cy, Z_TOP - 4, "black")                             # drain
    for (x, y) in [(cx - 1, cy), (cx + 1, cy), (cx, cy - 1), (cx, cy + 1),
                   (cx - 2, cy + 1), (cx - 1, cy + 2), (cx + 2, cy - 1), (cx + 1, cy - 2)]:
        g.set(x, y, Z_TOP - 4, "rust_deep")                       # dried tide ring
    for (x, y) in [(cx - 2, cy), (cx + 2, cy + 1), (cx, cy + 2), (cx - 1, cy - 2)]:
        g.set(x, y, Z_TOP - 4, "card_dark")
    g.paint(bx0 + 1, by1 - 1, Z_TOP - 3, bx1 - 1, by1 - 1, Z_TOP - 3, "steel")  # water line
    # drainer: ribbed steel with a raised lip
    g.box(bx1 + 1, by0, Z_TOP, W - 3, by1, Z_TOP, "steel_hi")
    for x in range(bx1 + 2, W - 3, 2):
        g.paint(x, by0 + 1, Z_TOP, x, by1 - 1, Z_TOP, "steel_light")
    # swan-neck mixer behind the basin: column, neck reaching over the basin, short spout
    g.paint(cx - 2, 1, Z_TOP, cx + 2, 2, Z_TOP, "steel_hi")        # deck plate
    g.box(cx, 1, Z_TOP + 1, cx, 1, Z_TOP + 6, "chrome")           # column
    g.box(cx, 2, Z_TOP + 6, cx, 5, Z_TOP + 6, "chrome")           # neck
    g.set(cx, 5, Z_TOP + 5, "steel_light")                        # spout tip
    for sx in (cx - 2, cx + 2):                                   # valves with lever tops
        g.set(sx, 1, Z_TOP + 1, "chrome")
        g.box(sx, 1, Z_TOP + 2, sx, 2, Z_TOP + 2, "steel_light")
    # wire dish rack on the drainer: two plates on edge and an upturned mug
    rx0, rx1, ry0, ry1 = 12, W - 3, 4, 10
    for y in (ry0, ry1):
        g.box(rx0, y, Z_TOP + 1, rx1, y, Z_TOP + 1, "steel_light")  # long rails
    for x in range(rx0, rx1 + 1, 2):
        g.box(x, ry0, Z_TOP + 1, x, ry1, Z_TOP + 1, "steel_light")  # cross wires
    for x in (rx0, rx1):                                          # low tines at the ends
        for y in (5, 7, 9):
            g.set(x, y, Z_TOP + 2, "steel_light")
    for py in (6, 8):                                             # 25 cm plates on edge,
        for (x, z1) in [(13, Z_TOP + 4), (14, Z_TOP + 5), (15, Z_TOP + 5),  # faces to the room
                        (16, Z_TOP + 5), (17, Z_TOP + 4)]:
            g.box(x, py, Z_TOP + 1, x, py, z1, "porcelain_hi")
        for (x, z) in [(13, Z_TOP + 4), (14, Z_TOP + 5), (15, Z_TOP + 5), (16, Z_TOP + 5),
                       (17, Z_TOP + 4), (13, Z_TOP + 2), (17, Z_TOP + 2)]:
            g.paint(x, py, z, x, py, z, "porcelain_mid")           # rim
    g.box(13, 9, Z_TOP + 1, 14, 10, Z_TOP + 2, "terra")            # upturned mug
    g.set(12, 9, Z_TOP + 2, "terra_dark")                         # its handle
    return {"grid": g, "footprint_cells": ((0, W - 1), (0, Y_EDGE))}


# =========================================================================================
@model("kitchen_oven", name="Stove / Oven",
       story="A plain white enamel gas range that cooked for a family for fifteen years. The "
             "front-left burner was the favourite: its drip pan is burnt brown and grease has "
             "run down the front below its knob. Nobody has lit it since the gas stopped.",
       details=["Four burners: cast-iron square grates over chrome drip pans and iron caps",
                "Backguard with a lit top edge", "Control strip with four knobs and a small "
                "clock window", "Oven door with a dark window and a chrome handle bar",
                "Storage drawer and recessed kick", "Grease burnt into the favourite burner "
                "and run down the front below its knob"],
       exclusions=["No brand plate or readable dial text", "No flames or glow"],
       notes=["Cooktop flush with the kitchen's 0.90 m worktop line and 0.65 m deep like the "
              "base units; the grates (5 cm) and the 10 cm backguard take the total to 1.0 m "
              "against GPT's 0.90 m reference, and 0.70 m wide (14 cells) against 0.68 m."])
def kitchen_oven():
    W = 14
    g = Grid(W, 14, 21)
    FY = 11                                                       # front face
    g.box(0, 0, 1, W - 1, FY, Z_TOP - 1, "porcelain")             # enamel body
    g.box(1, 0, 0, W - 2, FY - 1, 0, "charcoal")                  # recessed kick
    g.paint(0, 0, 1, 0, FY, Z_TOP - 1, "porcelain_mid")           # side panels a step down
    g.paint(W - 1, 0, 1, W - 1, FY, Z_TOP - 1, "porcelain_mid")
    g.paint(0, FY, 1, 0, FY, Z_TOP - 1, "porcelain")              # front corner trim
    g.paint(W - 1, FY, 1, W - 1, FY, Z_TOP - 1, "porcelain")
    # storage drawer z 1-2, reveal z 3
    g.paint(1, FY, 1, W - 2, FY, 2, "porcelain_hi")
    g.paint(1, FY, 3, W - 2, FY, 3, "porcelain_shadow")
    g.box(5, FY + 1, 2, 8, FY + 1, 2, "porcelain_mid")            # finger pull
    # oven door z 4-12 with window and handle bar
    g.paint(1, FY, 4, W - 2, FY, 12, "porcelain_hi")
    g.paint(3, FY, 6, W - 4, FY, 9, "glass_deep")                 # dark window
    g.paint(3, FY, 9, W - 4, FY, 9, "glass_dark")                 # top sheen row
    g.paint(2, FY, 6, 2, FY, 9, "porcelain_mid")                  # window frame shade
    g.box(2, FY + 1, 11, W - 3, FY + 1, 11, "chrome")             # handle bar
    g.paint(1, FY, 13, W - 2, FY, 13, "porcelain_shadow")         # reveal under controls
    # control strip z 14-16 with four knobs and a clock window
    g.paint(1, FY, 14, W - 2, FY, 16, "porcelain_mid")
    for kx in (2, 4, 9, 11):
        g.set(kx, FY + 1, 15, "charcoal")
    g.paint(6, FY, 15, 7, FY, 15, "screen")
    # cooktop, backguard
    g.box(0, 0, Z_TOP, W - 1, FY, Z_TOP, "porcelain_hi")
    g.box(0, 0, Z_TOP + 1, W - 1, 0, Z_TOP + 2, "porcelain")       # backguard
    g.paint(0, 0, Z_TOP + 2, W - 1, 0, Z_TOP + 2, "porcelain_hi")
    # four burners: 5x5 grate rings (back pair y 1-5, front pair y 6-10)
    for gx0 in (1, 8):
        for gy0 in (1, 6):
            g.box(gx0, gy0, Z_TOP + 1, gx0 + 4, gy0 + 4, Z_TOP + 1, "iron")
            g.clear(gx0 + 1, gy0 + 1, Z_TOP + 1, gx0 + 3, gy0 + 3, Z_TOP + 1)
            g.paint(gx0 + 1, gy0 + 1, Z_TOP, gx0 + 3, gy0 + 3, Z_TOP, "chrome")   # drip pan
            g.set(gx0 + 2, gy0 + 2, Z_TOP + 1, "iron_dark")                     # cap
            g.paint(gx0, gy0, Z_TOP + 1, gx0 + 4, gy0, Z_TOP + 1, "iron_edge")   # lit far bar
    # the favourite burner (front-left): burnt pan, grease on the enamel and down the front
    g.paint(2, 7, Z_TOP, 4, 9, Z_TOP, "rust_deep")
    g.paint(3, 9, Z_TOP, 4, 9, Z_TOP, "coal")
    g.paint(0, FY, Z_TOP, 5, FY, Z_TOP, "almond")
    g.paint(1, 10, Z_TOP, 1, 11, Z_TOP, "almond_dark")
    g.paint(2, FY, 16, 2, FY, 16, "almond_dark")                  # drip below the knob
    g.paint(3, FY, 14, 3, FY, 16, "almond")
    g.paint(3, FY, 13, 3, FY, 13, "almond_dark")
    return {"grid": g, "footprint_cells": ((0, W - 1), (0, FY))}


# =========================================================================================
@model("wall_cabinet", name="Kitchen Wall Cabinet",
       story="Hung above the counter, it held the everyday plates and cups. The right-hand door "
             "was left standing open; most of the cups are gone, the plates were left because "
             "nobody needed plates any more.",
       details=["Sage shaker doors matching the base units; right door open 90 degrees",
                "Interior shelf with a short plate stack and two cups, one tipped",
                "Charcoal handles at the bottom of the doors (reachable from below)",
                "Flat back for the wall"],
       exclusions=["No wall, no mounting rail modelled"],
       mount={"type": "wall", "recommended_bottom_height_m": 1.45},
       pivot_note="Bottom centre of the back face (the cabinet body, not the open door). Hang "
                  "with the back on the wall; bottom at about 1.45 m (0.55 m over the 0.90 m "
                  "worktop).",
       front_note="+Y faces into the room; the back (y = 0) is flat for the wall.",
       collision_hint="Box 1.05 x 0.35 x 0.75 m for the body; the open door adds a 0.05 x "
                      "0.50 m leaf at the right end.",
       notes=["Closed body 1.05 x 0.35 x 0.75 m (GPT reference 1.06 x 0.36 x 0.76 m). The open "
              "door is part of the story and adds 0.50 m of depth at the right end only."])
def wall_cabinet():
    W, H = 21, 15
    g = Grid(W + 2, 18, H)
    FP, FF = 5, 6                                                 # panel / frame planes
    g.box(0, 0, 0, W - 1, FP - 1, H - 1, "sage")                  # carcass
    g.clear(1, 1, 1, W - 2, FP - 1, H - 2)                        # open interior
    g.box(1, 0, 1, W - 2, 0, H - 2, "sage_dark")                  # back panel inside
    g.paint(1, 1, 1, W - 2, FP - 1, 1, "sage_dark")               # floor of the box
    g.box(1, 1, 7, W - 2, FP - 1, 7, "sage")                      # shelf
    g.paint(1, FP - 1, 7, W - 2, FP - 1, 7, "sage_hi")            # shelf's lit front lip
    # left door, closed (shaker, panel recessed)
    g.box(0, FP, 0, 9, FP, H - 1, "sage")
    g.box(0, FF, 0, 9, FF, H - 1, "sage")
    g.clear(1, FF, 1, 8, FF, H - 2)
    g.box(9, FF + 1, 1, 9, FF + 1, 3, HANDLE)                     # handle low, by the opening
    g.paint(9, FF, 4, 9, FF, 5, "sage_hi")                        # rubbed by fingers
    # right door, open 90 degrees on its right-hand hinge: the leaf stands along +Y just
    # beyond the right side; its plain inner face looks back at the shelves (-X) and its
    # shaker frame and handle face outward (+X)
    g.box(W - 1, FP, 0, W - 1, FP + 10, H - 1, "sage")            # flat inner face
    g.box(W, FP, 0, W, FP + 10, H - 1, "sage")                    # frame plane, faces +X
    g.clear(W, FP + 1, 1, W, FP + 9, H - 2)
    g.box(W + 1, FP + 10, 1, W + 1, FP + 10, 3, HANDLE)           # handle on the free stile
    for z0 in (1, H - 3):                                         # hinges at the front edge
        g.box(W - 1, FP - 1, z0, W - 1, FP - 1, z0 + 1, "steel_dark")
    g.paint(W - 1, FP + 5, 6, W - 1, FP + 7, 10, "paper")         # a list taped inside the door
    g.paint(W - 1, FP + 5, 8, W - 1, FP + 7, 8, "cream_shadow")
    g.paint(W - 1, FP + 6, 10, W - 1, FP + 6, 10, "cream_deep")   # tape
    # lower shelf: side plates and two nested bowls; upper: one mug, a glass, a mug on its side
    g.box(11, 1, 1, 14, 4, 2, "porcelain")                        # plate stack
    g.paint(11, 1, 1, 14, 4, 1, "porcelain_mid")                  # plate edges
    g.paint(11, 1, 2, 14, 4, 2, "porcelain_hi")
    g.paint(12, 2, 2, 13, 3, 2, "porcelain_mid")                  # top plate's well
    g.box(16, 2, 1, 18, 4, 2, "porcelain_hi")                     # bowls
    g.paint(16, 2, 1, 18, 4, 1, "porcelain_shadow")
    g.clear(17, 3, 2, 17, 3, 2)
    g.box(11, 2, 8, 12, 3, 9, "terra")                            # mug, handle toward the room
    g.set(11, 4, 9, "terra_dark")
    g.box(14, 3, 8, 14, 3, 9, "glass_hi")                         # glass
    g.box(16, 2, 8, 17, 3, 9, "porcelain_hi")                     # white mug on its side
    g.paint(17, 2, 8, 17, 3, 9, "porcelain_mid")                  # its open end
    g.set(16, 2, 10, "porcelain_mid")                             # handle pointing up
    return {"grid": g, "pivot_cells": (W / 2, 0, 0)}               # bottom centre of the back


# =========================================================================================
@model("refrigerator", name="Almond Fridge-Freezer",
       story="A twenty-year-old almond fridge-freezer that outlived two kitchens. A shopping "
             "note and a child's drawing are still held by magnets; the door seal on the "
             "opening side has come loose and hangs out, and damp under it has bloomed into "
             "rust along the bottom corner.",
       details=["Freezer door over a taller fridge door, dark seam between them",
                "Soft rounded top edge; slightly darker side panels; door gasket seam on the "
                "sides", "Steel bar handles on the opening (left) side",
                "Paper note and a child's drawing held by three magnets",
                "Loose rubber door seal hanging from the opening edge",
                "Rust bloom at the bottom front corner and on the kick grille"],
       exclusions=["No brand badge", "No ice dispenser", "No readable writing on the note"],
       notes=["0.75 x 0.70 x 1.80 m (GPT reference 0.73 x 0.70 x 1.78 m); the hanging seal "
              "adds one cell on the left."])
def refrigerator():
    o, W = 2, 15                                                  # x offset for the seal
    x0, x1 = o, o + W - 1
    g = Grid(W + 3, 15, 37)
    TOPZ = 35
    # cabinet: body y 0-10 (sides cream_mid), gasket seam y 10 on the sides, doors y 11-12
    g.box(x0, 0, 1, x1, 10, TOPZ, "cream_mid")
    g.paint(x0, 0, 1, x1, 0, TOPZ, "almond_dark")                 # back panel
    g.paint(x0, 10, 1, x0, 10, TOPZ, "cream_deep")                # gasket seam, both sides
    g.paint(x1, 10, 1, x1, 10, TOPZ, "cream_deep")
    g.box(x0 + 1, 1, 0, x1 - 1, 9, 0, "charcoal")                 # recessed base
    g.box(x0 + 1, 10, 0, x1 - 1, 10, 0, "iron_edge")              # kick grille
    for x in range(x0 + 2, x1 - 1, 2):
        g.set(x, 10, 0, "black")
    g.box(x0, 11, 1, x1, 12, TOPZ, "almond")                      # doors
    g.paint(x0, 11, 1, x1, 11, TOPZ, "cream_mid")                 # door edges seen from side
    g.clear(x0, 11, 23, x1, 12, 23)                               # seam between the doors
    g.box(x0 + 1, 10, 23, x1 - 1, 10, 23, "charcoal")
    # soft top: the freezer door's upper edge is rounded over
    g.clear(x0, 12, TOPZ, x1, 12, TOPZ)
    g.paint(x0, 0, TOPZ, x1, 10, TOPZ, "cream")                   # top panel
    g.paint(x0, 11, TOPZ, x1, 11, TOPZ, "almond")
    for z0 in (2, 20, 25, TOPZ - 2):                              # hinges on the right
        g.box(x1, 11, z0, x1, 11, z0 + 1, "almond_dark")
    # handles on the opening (left) side
    g.box(x0 + 1, 13, 25, x0 + 1, 13, 30, "steel_light")
    g.box(x0 + 1, 13, 15, x0 + 1, 13, 21, "steel_light")
    g.paint(x0 + 1, 13, 25, x0 + 1, 13, 25, "steel")              # bar ends
    g.paint(x0 + 1, 13, 15, x0 + 1, 13, 15, "steel")
    g.paint(x0, 12, 16, x0, 12, 20, "cream")                      # door edge rubbed clean
    g.paint(x0 + 2, 12, 14, x0 + 2, 12, 21, "cream_mid")          # hand grime by the handle
    # note and magnets on the freezer door, a drawing on the fridge door
    g.paint(x0 + 8, 12, 27, x0 + 10, 12, 30, "porcelain_hi")
    g.paint(x0 + 8, 12, 28, x0 + 9, 12, 28, "cream_shadow")       # faint lines, unreadable
    g.set(x0 + 9, 13, 30, "signal_red_dark")
    g.set(x0 + 5, 13, 32, "teal_dark")
    g.paint(x0 + 6, 12, 15, x0 + 9, 12, 18, "porcelain_hi")       # child's drawing
    g.paint(x0 + 6, 12, 15, x0 + 9, 12, 15, "leaf")               # green ground
    g.paint(x0 + 7, 12, 16, x0 + 7, 12, 17, "terra")              # a little house
    g.paint(x0 + 9, 12, 18, x0 + 9, 12, 18, "mustard")            # sun
    g.set(x0 + 6, 13, 18, "mustard_dark")
    # loose door seal hanging out of the opening edge of the fridge door
    for (x, y, z) in [(x0 - 1, 11, 14), (x0 - 1, 11, 13), (x0 - 1, 11, 12), (x0 - 1, 12, 11),
                      (x0 - 2, 12, 11), (x0 - 2, 12, 10), (x0 - 2, 12, 9), (x0 - 2, 12, 8),
                      (x0 - 2, 12, 7), (x0 - 2, 12, 6), (x0 - 1, 12, 6), (x0 - 1, 11, 6),
                      (x0 - 1, 11, 5), (x0 - 1, 11, 7)]:
        g.set(x, y, z, "iron_edge")                               # sagging loop of rubber
    g.set(x0 - 2, 12, 8, "steel_dark")
    # rust bloom at the bottom front-left corner (damp under the loose seal)
    for (x, y, z) in [(x0, 11, 1), (x0, 12, 1), (x0 + 1, 12, 1), (x0 + 2, 12, 1),
                      (x0, 12, 2), (x0, 11, 2), (x0, 10, 1), (x0, 9, 1), (x0, 12, 3),
                      (x0 + 1, 12, 2), (x0 + 3, 12, 1)]:
        g.paint_cell(x, y, z, "rust_dark")
    for (x, y, z) in [(x0, 12, 1), (x0 + 1, 12, 1), (x0, 11, 1)]:
        g.paint_cell(x, y, z, "rust")
    for (x, y, z) in [(x0 + 1, 10, 0), (x0 + 3, 10, 0)]:
        g.paint_cell(x, y, z, "rust_deep")
    return {"grid": g, "footprint_cells": ((x0, x1), (0, 12))}


# =========================================================================================
def _can(g, x, y, z, label, lying=False):
    """10 cm food can: two label cells and a foil top (or lying along X)."""
    if lying:
        g.box(x, y, z, x + 2, y + 1, z + 1, label)
        g.paint(x + 2, y, z, x + 2, y + 1, z + 1, "foil")
    else:
        g.box(x, y, z, x + 1, y + 1, z + 1, label)
        g.box(x, y, z + 2, x + 1, y + 1, z + 2, "foil")


def _jar(g, x, y, z, fill="mustard_dark"):
    g.box(x, y, z, x + 1, y + 1, z + 1, fill)
    g.paint(x, y, z + 1, x + 1, y + 1, z + 1, "glass_hi")         # empty upper glass
    g.box(x, y, z + 2, x + 1, y + 1, z + 2, "brass_dark")         # lid


@model("pantry_shelf", name="Pantry Shelving",
       story="Plain pine shelving in a walk-in pantry, stripped by whoever came first. They "
             "took what they could carry: a few cans rolled to the back, two jars nobody "
             "wanted, a flour sack that split when it was dragged and spilled down to the "
             "floor, and the cardboard tray the tins came in.",
       details=["Five pine shelves on four square posts with back stop rails",
                "Split flour sack slumped on the bottom shelf, flour spilled over the edge "
                "into a drift on the floor", "Empty cardboard tray on the middle shelf",
                "Three cans (one fallen on its side) and two jars, pushed to the back",
                "Pale clean patches on the boards where stock stood for years"],
       exclusions=["No readable labels or brands", "Mostly empty on purpose"],
       notes=["1.15 x 0.50 x 1.80 m (GPT reference 1.15 x 0.48 x 1.80 m)."])
def pantry_shelf():
    W, D, H = 23, 10, 36
    g = Grid(W, D + 3, H)
    shelves = [2, 10, 18, 26, 35]
    for (x, y) in [(0, 0), (W - 1, 0), (0, D - 1), (W - 1, D - 1)]:
        g.box(x, y, 0, x, y, H - 1, "pine_aged")                  # posts
        g.set(x, y, 0, "pine_dark")                               # floor-grimed feet
    for z in shelves:
        g.box(0, 0, z, W - 1, D - 1, z, "pine_mid")
        g.paint(0, 5, z, W - 1, D - 1, z, "pine_light")           # front board, more light
        if z != shelves[-1]:
            g.box(1, 0, z + 1, W - 2, 0, z + 1, "pine_aged")      # back stop rail
    g.box(0, 1, 1, 0, D - 2, 1, "pine_aged")                      # low side rails
    g.box(W - 1, 1, 1, W - 1, D - 2, 1, "pine_aged")
    for z in (14, 30):                                            # side braces mid-height
        g.box(0, 1, z, 0, D - 2, z, "pine_aged")
        g.box(W - 1, 1, z, W - 1, D - 2, z, "pine_aged")
    # clean outlines where stock stood (paler wood), only on the upper shelves
    g.paint(3, 2, 26, 8, 6, 26, "pine_hi")
    g.paint(13, 2, 10, 17, 5, 10, "pine_hi")
    # bottom shelf: the split flour sack, slumped against the left post
    g.rbox(2, 3, 3, 7, 7, 5, "cream")                             # sack body, soft corners
    g.rbox(2, 3, 6, 6, 5, 6, "cream")                             # slumped shoulder at back
    g.box(3, 3, 7, 5, 4, 7, "cream_mid")
    g.paint(2, 3, 3, 7, 7, 3, "cream_shadow")                     # weight sags at the bottom
    g.paint(2, 3, 5, 7, 7, 5, "blue_mid")                         # faded printed band
    g.paint(2, 3, 5, 7, 3, 5, "blue_dark")
    g.box(4, 3, 8, 4, 4, 8, "cream_mid")                          # tied neck flopped back
    g.set(4, 4, 8, "card_dark")                                   # string
    g.clear(6, 7, 4, 7, 7, 4)                                     # the split, front corner
    g.paint(5, 6, 4, 7, 6, 4, "paper")                            # flour inside the split
    g.box(4, 8, 3, 9, 9, 3, "paper")                              # spill along the shelf,
    g.box(6, 10, 3, 7, 10, 3, "paper")                            # over the front lip
    for (y, xa, xb) in [(9, 1, 8), (10, 1, 9), (11, 2, 8), (12, 4, 6)]:
        g.box(xa, y, 0, xb, y, 0, "paper")                        # low drift on the floor
    g.box(5, 10, 1, 7, 11, 1, "porcelain_hi")                     # heaped under the trickle
    # second shelf: three cans, one on its side, and a jar
    _can(g, 14, 1, 11, "label_red")
    _can(g, 17, 1, 11, "label_green")
    _can(g, 10, 7, 11, "label_red", lying=True)                   # rolled to the front edge
    _jar(g, 3, 1, 11)
    # middle shelf: the empty cardboard tray the tins came in
    g.box(9, 2, 19, 16, 8, 19, "card")
    g.clear(10, 3, 19, 15, 7, 19)
    g.paint(9, 8, 19, 16, 8, 19, "card_hi")
    g.paint(10, 3, 18, 15, 7, 18, "card_dark")                    # tray floor (on the shelf)
    g.box(10, 3, 19, 15, 7, 19, 0)
    g.box(10, 3, 18, 15, 7, 18, "card_dark")
    # fourth shelf: one jar left at the back
    _jar(g, 16, 1, 27, fill="red_dark")
    return {"grid": g, "footprint_cells": ((0, W - 1), (0, D - 1))}


# =========================================================================================
# Small kitchen pickups (fine 0.025 m / micro 0.0125 m)
# =========================================================================================
def _disc(g, cx, cy, r, z, c):
    for (i, j) in g.disc_cells(cx, cy, r):
        g.set(i, j, z, c)


def _ring(g, cx, cy, r, z0, z1, c):
    for (i, j) in g.ring_cells(cx, cy, r):
        g.box(i, j, z0, i, j, z1, c)


@model("dining_crockery", name="Dining Crockery Set",
       story="The last clean things in the house: four dinner plates, a bowl, a mug and a "
             "tumbler put away on a folded tea towel after the final washing-up, and never "
             "used again.",
       details=["Stack of four dinner plates; the top plate shows its rim and sunken well",
                "White bowl with a foot ring", "Terracotta glazed mug with a loop handle",
                "Pale glass tumbler", "Folded cream tea towel with two faded blue stripes "
                "joins the set into one piece"],
       exclusions=["No food", "No pattern noise on the plates"],
       notes=["0.525 x 0.30 x 0.125 m at 2.5 cm cells (GPT reference 0.52 x 0.32 x 0.13 m). "
              "Plates are 25 cm across; each plate is one 2.5 cm layer (thicker than real, the "
              "minimum at this tier)."])
def dining_crockery():
    g = Grid(21, 12, 6)
    # folded tea towel: one layer, two woven stripes, a darker hem along the front
    g.box(0, 0, 0, 20, 11, 0, "cream")
    for x in (2, 18):
        g.box(x, 0, 0, x, 11, 0, "blue_mid")
    g.paint(0, 11, 0, 20, 11, 0, "cream_mid")
    g.paint(2, 11, 0, 2, 11, 0, "blue_dark")
    g.paint(18, 11, 0, 18, 11, 0, "blue_dark")
    # four 25 cm dinner plates; edges alternate so the plates read; rim and well on top
    pcx, pcy = 6.0, 6.0
    for z, col in ((1, "porcelain_mid"), (2, "porcelain"), (3, "porcelain_mid"),
                   (4, "porcelain")):
        _disc(g, pcx, pcy, 5.3, z, col)
    _disc(g, pcx, pcy, 5.3, 4, "porcelain_hi")                    # top plate's rim
    _disc(g, pcx, pcy, 3.0, 4, "porcelain")                       # its well
    # bowl: small foot, then a wall ring with the inside showing
    bcx, bcy = 16.0, 3.0
    g.box(15, 2, 1, 16, 3, 1, "porcelain_mid")                    # foot ring
    _disc(g, bcx, bcy, 3.0, 2, "porcelain")
    _ring(g, bcx, bcy, 3.0, 3, 4, "porcelain")
    _ring(g, bcx, bcy, 3.0, 4, 4, "porcelain_hi")                 # lip
    _disc(g, bcx, bcy, 2.0, 2, "porcelain_hi")                    # inside floor
    # mug (terracotta glaze), handle toward the front
    g.box(17, 7, 1, 19, 9, 4, "terra")
    g.paint(17, 7, 4, 19, 9, 4, "terra_hi")                       # glazed lip
    g.set(18, 8, 4, 0)
    g.set(18, 8, 3, "terra_deep")                                 # inside, in shadow
    g.set(18, 10, 2, "terra_dark")
    g.set(18, 10, 4, "terra_dark")
    g.box(18, 11, 2, 18, 11, 4, "terra_dark")
    # glass tumbler
    g.box(12, 8, 1, 14, 10, 4, "glass_hi")
    g.paint(12, 8, 1, 14, 10, 1, "glass")                         # thick base
    g.set(13, 9, 4, 0)
    g.set(13, 9, 3, 0)
    g.set(13, 9, 2, "glass")
    return g


@model("frying_pan", name="Cast-Iron Skillet",
       story="A heavy cast-iron skillet seasoned black by years of cooking. It was left on a "
             "cold stove, so a little rust has started where the rim met the damp air; the "
             "inside is still smooth from the last oiling.",
       details=["11-cell (27 cm) pan with flared walls and a lit rim edge",
                "Seasoned interior with a polished cooking zone",
                "Long cast handle with a hanging hole and a small helper lug opposite",
                "Rust beginning along one arc of the rim"],
       exclusions=["No non-stick coating colours", "No food"],
       attachments={"grip": {"note": "Main hand on the cast grip, near the hanging hole"}},
       notes=["0.575 x 0.275 x 0.10 m at 2.5 cm cells (GPT reference 0.57 x 0.28 x 0.10 m). "
              "Laid out along X like a pan on a hob; as an improvised weapon the grip "
              "attachment is the hand position (rotate so the pan points +Y)."])
def frying_pan():
    g = Grid(23, 11, 4)
    cx, cy = 16.5, 5.5                                            # pan body x 11-21
    _disc(g, cx, cy, 4.5, 0, "iron")                              # base, narrower: flare
    _disc(g, cx, cy, 5.5, 1, "iron")
    _ring(g, cx, cy, 5.5, 2, 2, "iron_edge")                      # rim with a catch-light
    for (i, j) in g.disc_cells(cx, cy, 5.5):
        if not g.get(i, j, 2):
            g.set(i, j, 1, "iron_dark")                           # seasoned cooking surface
    for (i, j) in g.disc_cells(cx, cy, 2.5):
        g.set(i, j, 1, "iron_blue")                               # polished centre
    # rust beginning on the rim arc facing the camera (front, handle side)
    for (i, j, z) in [(12, 7, 2), (12, 8, 2), (12, 9, 2), (13, 9, 2), (13, 10, 2),
                      (14, 10, 2), (15, 10, 2)]:
        g.paint_cell(i, j, z, "rust_deep")                        # rust starting on the lip
    for (i, j, z) in [(13, 9, 2), (12, 8, 1)]:
        g.paint_cell(i, j, z, "rust_dark")
    # long handle toward -X: a shaft at rim height, then a wider grip with a hanging hole
    g.box(5, 5, 2, 10, 5, 2, "iron_edge")                         # shaft, lit top
    g.box(3, 5, 3, 5, 5, 3, "iron_edge")                          # rising grip
    g.box(0, 4, 3, 2, 6, 3, "iron")                               # loop round the hole
    g.paint(0, 4, 3, 2, 4, 3, "iron_edge")
    g.set(1, 5, 3, 0)                                             # hanging hole
    # small helper lug opposite the handle
    g.box(22, 4, 2, 22, 6, 2, "iron_edge")
    return {"grid": g, "attachments": {"grip": (3, 5, 3)}}


@model("kettle", name="Enamel Stovetop Kettle",
       story="A cream enamel kettle that lived on the back burner. Years of being banged onto "
             "the grate chipped the enamel round the base and the lid, and the flames left "
             "the bottom sooted black. Somebody boiled water in it for days after the "
             "power went.",
       details=["Round-bellied cream enamel body with a lid seam and a black knob",
                "Dark curved spout rising from the lower belly",
                "Black handle arching over the lid on two posts",
                "Soot on the base licking up the sides; enamel chips at the base, the lid "
                "rim and the spout root"],
       exclusions=["No whistle cap text", "No steam"],
       notes=["0.275 x 0.20 x 0.275 m at 1.25 cm cells (GPT reference 0.26 x 0.24 x 0.28 m); "
              "the spout points -X toward the default camera and the handle arches along X."])
def kettle():
    g = Grid(23, 17, 22)
    cx, cy = 15.0, 8.0                                            # body centre (16 cells)
    profile = [(0, 7.0, "soot"), (1, 7.0, "soot"), (2, 8.0, "char")] + \
        [(z, 8.0, "cream") for z in range(3, 10)] + \
        [(10, 7.0, "cream"), (11, 6.0, "cream_hi"), (12, 5.0, "cream_hi")]
    for z, r, col in profile:                                     # lathe: belly, shoulder
        for (i, j) in g.disc_cells(cx, cy, r):
            g.set(i, j, z, col)
    for (i, j) in g.disc_cells(cx, cy, 4.0):                      # lid
        g.set(i, j, 13, "cream_hi")
    for (i, j) in g.ring_cells(cx, cy, 4.0):
        g.set(i, j, 13, "cream_shadow")                           # lid seam
    for (i, j) in g.disc_cells(cx, cy, 3.0):
        g.set(i, j, 14, "cream_hi")
    g.box(14, 7, 15, 15, 8, 16, "black")                          # knob
    # soot licking up the camera-side flank, and chipped enamel where it hits the grate
    for (x, y, z) in [(7, 6, 3), (7, 7, 3), (7, 8, 3), (7, 9, 3), (8, 11, 3), (8, 12, 3),
                      (9, 13, 3), (7, 8, 4), (7, 9, 4), (8, 12, 4), (11, 15, 3), (12, 15, 3)]:
        g.paint_cell(x, y, z, "char")
    for (x, y, z) in [(12, 15, 4), (13, 15, 4), (13, 15, 5), (14, 15, 3)]:
        g.paint_cell(x, y, z, "iron_dark")                        # chip on the front belly
    for (x, y, z) in [(12, 11, 13), (13, 12, 13)]:
        g.paint_cell(x, y, z, "iron_edge")                        # chip on the lid rim
    # spout: dark, rising from the lower belly toward -X
    for k in range(6):
        x, z0 = 7 - k, 3 + k
        g.box(x, 7, z0, x + 1, 8, z0 + 2, "iron")
    g.box(1, 7, 9, 2, 8, 10, "iron_edge")                         # lit lip
    g.set(1, 7, 10, "black")                                      # opening
    g.set(1, 8, 10, "black")
    for (x, y, z) in [(7, 6, 4), (7, 9, 4), (7, 6, 5), (7, 9, 5)]:
        g.set(x, y, z, "iron")                                    # flared spout root
    # handle: thin steel posts from the shoulder, a black grip arching over the lid
    for x in (10, 20):
        g.box(x, 7, 11, x, 8, 19, "steel_dark")
    g.box(10, 7, 20, 20, 8, 21, "black")
    g.paint(11, 7, 21, 19, 8, 21, "charcoal")                     # worn top of the grip
    g.clear(10, 7, 21, 10, 8, 21)
    g.clear(20, 7, 21, 20, 8, 21)
    return g


@model("cutting_board", name="Wooden Cutting Board",
       story="A beech chopping board from the knife drawer side of the counter, scored grey in "
             "the middle by years of onions, with the little paring knife still lying on it "
             "from the last meal anyone made.",
       details=["Edge-glued strips in three close tones, rounded corners",
                "Hanging hole at the left end", "Knife-scored, greyed work zone in the "
                "middle and a darker damp end-grain stain", "Small paring knife: steel "
                "blade with a pale edge, dark wooden handle with two brass rivets"],
       exclusions=["No food", "No brand burn mark"],
       notes=["0.425 x 0.30 x 0.05 m at 1.25 cm cells (GPT reference 0.43 x 0.29 x 0.045 m); "
              "board 2.5 cm thick, knife handle on top."])
def cutting_board():
    W, D = 34, 24
    g = Grid(W, D, 4)
    tones = ["pine_light", "pine_hi", "pine_light", "pine_mid", "pine_hi", "pine_light"]
    widths = [4, 3, 5, 4, 4, 4]                                   # edge-glued strips
    j = 0
    for t, w in zip(tones, widths):
        g.box(0, j, 0, W - 1, j + w - 1, 1, t)
        j += w
    for (x, y) in [(0, 0), (1, 0), (0, 1), (W - 1, 0), (W - 2, 0), (W - 1, 1),
                   (0, D - 1), (1, D - 1), (0, D - 2), (W - 1, D - 1), (W - 2, D - 1),
                   (W - 1, D - 2)]:
        g.clear(x, y, 0, x, y, 1)                                 # rounded corners
    g.paint(0, 0, 0, W - 1, D - 1, 0, "pine_mid")                 # underside / lower arris
    g.clear(2, 11, 0, 3, 12, 1)                                   # hanging hole
    # the work zone: scrubbed paler, with a few deeper knife cuts in different directions
    for (y, xa, xb) in [(5, 16, 21), (6, 13, 23), (7, 12, 24), (8, 11, 24), (9, 11, 25),
                        (10, 12, 25), (11, 12, 24), (12, 14, 22), (13, 16, 20)]:
        g.paint(xa, y, 1, xb, y, 1, "pine_hi")
    for (x0, y0, x1, y1) in [(13, 7, 16, 7), (22, 6, 22, 8), (17, 12, 21, 12),
                             (19, 8, 19, 9), (12, 10, 13, 10)]:
        g.paint(x0, y0, 1, x1, y1, 1, "pine_mid")
    # paring knife lying along the front: blade toward +X, handle toward -X
    g.box(8, 18, 2, 14, 19, 2, "wood_stain")                      # handle
    g.box(8, 18, 3, 14, 19, 3, "wood_stain")
    g.paint(8, 18, 3, 14, 18, 3, "pine_dark")                     # worn top edge
    g.set(10, 19, 3, "brass")
    g.set(13, 19, 3, "brass")
    g.box(15, 18, 2, 15, 19, 2, "steel")                          # bolster
    g.box(16, 18, 2, 21, 19, 2, "steel_light")                    # blade
    g.paint(16, 19, 2, 21, 19, 2, "steel_hi")                     # honed edge
    g.box(22, 18, 2, 22, 18, 2, "steel_light")                    # tip
    return g
