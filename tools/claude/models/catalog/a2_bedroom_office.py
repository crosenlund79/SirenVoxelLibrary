"""Batch A2 - bedroom and office (creator: Claude).

Sits in the same houses as Claude_sofa, Claude_dining_table and Claude_single_bed_unmade.
0.05 m cells; X right, Y front (+Y = the side a person uses; for beds, the FOOT), Z up;
inclusive cell ranges; everything stands on z = 0. The hero camera sees +Y and -X, so the
story details sit on those faces.

Woods and finishes, varied on purpose:
  honey oak  pine_mid / pine_aged / pine_light (double bed, nightstand - a bought-together set)
  oak        pine_light / pine_mid / pine_aged (dining chair: the SAME ramp and roles as
             Claude_dining_table so they read as a pair)
  mahogany   leather_hi / leather / leather_dark / leather_deep (the old dresser)
  white      paint_white / paint_white_shadow (the flat-pack wardrobe, the desk pedestal)
"""
import math

from catalog_registry import model
from voxkit import Grid


def round_top_corners(g, x0, y0, x1, y1, z):
    for (x, y) in ((x0, y0), (x1, y0), (x0, y1), (x1, y1)):
        g.set(x, y, z, 0)


def line4(g, x0, y0, x1, y1, z, c):
    """Horizontal line between two cells that stays face-connected (no diagonal-only joins)."""
    n = max(abs(x1 - x0), abs(y1 - y0)) * 4 or 1
    px, py = x0, y0
    g.set(px, py, z, c)
    for i in range(1, n + 1):
        qx = int(math.floor(x0 + (x1 - x0) * i / n + 0.5))
        qy = int(math.floor(y0 + (y1 - y0) * i / n + 0.5))
        if qx != px and qy != py:
            g.set(qx, py, z, c)                                         # bridge the corner
        if (qx, qy) != (px, py):
            g.set(qx, qy, z, c)
        px, py = qx, qy


def leg(g, x, y, z0, z1, c, foot=None, w=2):
    g.box(x, y, z0, x + w - 1, y + w - 1, z1, c)
    if foot:
        g.box(x, y, z0, x + w - 1, y + w - 1, z0, foot)


# ---------------------------------------------------------------------------
# double bed
# ---------------------------------------------------------------------------
@model("double_bed",
       story="The parents' bed. Only the near side was slept in that last night: its pillow is "
             "still dented and skewed, and the mauve duvet was yanked up in a hurry before they "
             "left - square on the far side, rumpled and turned back on the near one.",
       details=["Honey-oak frame with a panelled headboard and a low footboard",
                "Mauve duvet pulled up crookedly, hanging lower on the near (-X) side",
                "Near side slept in: turned-back fold, sheet showing, dented pillow",
                "Far side neat: plump pillow, duvet up to it"],
       exclusions=["No throw cushions", "No pattern on the bedding"])
def double_bed():
    g = Grid(35, 42, 18)
    # frame: posts, rails, headboard panel, footboard
    for (x, y, top) in ((1, 0, 17), (32, 0, 17), (1, 40, 7), (32, 40, 7)):
        g.box(x, y, 0, x + 1, y + 1, top, "pine_aged")
        g.box(x, y, top, x + 1, y + 1, top, "pine_light")               # caps
        g.box(x, y, 0, x + 1, y + 1, 0, "pine_dark")                    # floor grime
    g.box(1, 2, 2, 1, 39, 4, "pine_aged")                               # side rails
    g.box(33, 2, 2, 33, 39, 4, "pine_aged")
    g.box(3, 0, 15, 31, 1, 16, "pine_aged")                             # headboard top rail
    g.paint(3, 0, 16, 31, 1, 16, "pine_light")
    g.box(3, 0, 4, 31, 1, 5, "pine_aged")                               # headboard bottom rail
    g.box(3, 1, 6, 31, 1, 14, "pine_mid")                               # panel
    g.box(5, 1, 7, 29, 1, 13, "pine_light")                             # raised field
    g.paint(13, 1, 12, 16, 1, 13, "pine_hi")                            # rubbed by the near head
    g.box(3, 41, 2, 31, 41, 6, "pine_mid")                              # footboard
    g.box(3, 41, 6, 31, 41, 6, "pine_aged")
    # mattress shell with fitted sheet
    g.box(2, 2, 5, 32, 39, 8, "cream_deep")
    g.paint(2, 2, 7, 32, 39, 8, "cream_mid")
    g.paint(2, 2, 8, 32, 39, 8, "cream")
    # pillows: far one plump and square, near one dented and skewed
    x0, x1, y0, y1 = 19, 30, 3, 8
    g.box(x0, y0, 9, x1, y1, 10, "cream_hi")
    g.paint(x0, y0, 9, x1, y1, 9, "cream_mid")
    for (cx, cy) in ((x0, y0), (x1, y0), (x0, y1), (x1, y1)):
        g.set(cx, cy, 10, 0)
    g.box(x0 + 2, y0 + 1, 11, x1 - 2, y1 - 1, 11, "cream_hi")           # plump crown
    g.box(4, 4, 9, 16, 9, 9, "cream_mid")
    g.box(5, 3, 9, 15, 3, 9, "cream_mid")
    g.box(5, 4, 10, 15, 8, 10, "cream_hi")
    g.box(4, 5, 10, 4, 7, 10, "cream_hi")
    g.box(16, 6, 10, 16, 8, 10, "cream_hi")
    for (cx, cy) in ((8, 5), (9, 5), (10, 5), (8, 6), (9, 6), (10, 6), (11, 6), (9, 7), (10, 7)):
        g.set(cx, cy, 10, "cream_mid")                                  # the head's hollow
    g.set(14, 4, 11, "cream_hi")                                        # bunched corner
    g.box(13, 4, 11, 15, 5, 11, "cream_hi")
    # duvet: head edge square on the far side, turned back on the near side
    def edge(x):
        return 10 if x >= 18 else (16 if x <= 13 else 16 - (x - 13))
    for x in range(0, 35):
        e = edge(x)
        if 1 <= x <= 33:
            g.box(x, e, 9, x, 40, 9, "mauve")
    # drapes: long and uneven on the near side, short and straight on the far side
    for y in range(edge(0) + 1, 41):
        hem = 3 + (1 if (y // 5) % 2 else 0) - (1 if 24 <= y <= 30 else 0)
        g.box(0, y, hem, 0, y, 9, "mauve")
        g.box(1, y, 5, 1, y, 9, "mauve")
        g.set(0, y, hem, "mauve_dark")
        if y in (19, 20, 27, 28, 35, 36):                                # fold valleys
            g.paint(0, y, hem, 0, y, 8, "mauve_dark")
    for y in range(11, 41):
        g.box(34, y, 5, 34, y, 9, "mauve")
        g.box(33, y, 5, 33, y, 9, "mauve")
        g.set(34, y, 5, "mauve_dark")
    g.box(1, 40, 6, 33, 40, 9, "mauve")                                 # over the foot
    g.paint(1, 40, 6, 33, 40, 6, "mauve_dark")
    # near side: the turned-back fold over the slept-in half
    for x in range(1, 17):
        e = edge(x)
        g.box(x, e, 10, x, e + 2, 10, "mauve_hi")                       # turned-back flap
        g.set(x, e, 11 if 3 <= x <= 12 else 10, "mauve_hi")              # rolled fold
        g.paint(x, e + 3, 9, x, e + 3, 9, "mauve_dark")                 # flap's shadowed hem
    g.paint(3, 10, 8, 14, 13, 8, "cream_hi")                             # warm, creased sheet
    g.paint(5, 11, 8, 11, 11, 8, "cream_mid")
    return {"grid": g, "footprint_cells": ((1, 33), (0, 41))}


# ---------------------------------------------------------------------------
# nightstand
# ---------------------------------------------------------------------------
@model("nightstand",
       story="The near-side nightstand, from the same honey-oak set as the double bed. The "
             "drawer was pulled open for a phone charger that was not there; the wind-up "
             "alarm clock stopped at some small hour and a paperback lies where it was put down.",
       details=["Drawer over an open shelf, drawer pulled a little open",
                "Twin-bell alarm clock with a pale face", "A paperback lying on top"],
       exclusions=["No lamp (separate model)", "No phone or charger"],
       notes=["Body top at 0.50 m to sit just above the double bed's 0.45 m mattress; the "
              "clock adds 0.15 m, so the overall height is 0.65 m."])
def nightstand():
    W, D = 10, 9                         # carcass y 0..7, frame lip y = 8
    g = Grid(W, D + 3, 14)
    for (x, y) in ((0, 0), (W - 1, 0), (0, D - 1), (W - 1, D - 1)):
        g.box(x, y, 0, x, y, 1, "pine_aged")
        g.set(x, y, 0, "pine_dark")
    g.box(0, 0, 2, W - 1, D - 1, 9, "pine_mid")                          # carcass
    g.box(0, 0, 9, W - 1, D - 1, 9, "pine_light")                        # top
    round_top_corners(g, 0, 0, W - 1, D - 1, 9)
    g.paint(0, D - 1, 2, W - 1, D - 1, 2, "pine_aged")
    g.box(1, 1, 3, W - 2, D - 1, 4, 0)                                   # open shelf
    g.box(1, 0, 3, W - 2, 0, 4, "pine_dark")
    g.box(1, 1, 5, W - 2, D - 1, 5, "pine_mid")                          # shelf / divider
    g.paint(1, D - 1, 5, W - 2, D - 1, 5, "pine_aged")
    # drawer, pulled 10 cm open
    g.box(1, D - 1, 6, W - 2, D - 1, 8, "pine_dark")                     # dark opening
    g.box(1, D, 6, W - 2, D + 1, 7, "pine_aged")                         # drawer sides showing
    g.box(2, D, 7, W - 3, D + 1, 7, 0)
    g.box(1, D + 2, 6, W - 2, D + 2, 8, "pine_mid")                      # drawer front
    g.set(4, D + 3, 7, "brass_dark")                                     # knob
    g.paint(1, D + 2, 8, W - 2, D + 2, 8, "pine_light")
    # on top: paperback lying open-side down, wind-up alarm clock
    g.box(1, 3, 10, 4, 6, 10, "terra_dark")
    g.box(1, 6, 10, 4, 6, 10, "paper")                                   # page edges toward us
    g.box(5, 2, 10, 7, 3, 11, "brass_dark")                              # clock body
    g.box(5, 3, 10, 7, 3, 11, "porcelain_hi")                            # face
    g.set(6, 3, 11, "black")                                             # stopped hands
    g.set(5, 2, 12, "brass")                                             # twin bells
    g.set(7, 2, 12, "brass")
    return {"grid": g, "footprint_cells": ((0, W - 1), (0, D - 1))}


# ---------------------------------------------------------------------------
# wardrobe
# ---------------------------------------------------------------------------
@model("wardrobe",
       story="A white flat-pack wardrobe in the back bedroom. The far door was left open "
             "after someone grabbed clothes for a few days - there are gaps on the rail - and "
             "the old suitcase on top was not the one they took. Years of shoes kicking the "
             "near door shut left grey marks along its foot.",
       details=["Shaker-style doors on a recessed plinth under a plain cornice",
                "Far (+X) door open: hanging rail with clothes and gaps, a shelf above",
                "Leather suitcase with straps lying on top",
                "Grey kick marks at the foot of the closed near (-X) door"],
       exclusions=["No mirror", "No loose shoes on the floor"],
       notes=["The far door is swung right open rather than ajar: an angled one-cell door at "
              "0.05 m becomes a jagged staircase and hides the clothes.",
              "The open door adds 0.75 m in +Y; footprint_cells covers only the carcass.",
              "Carcass and cornice 1.80 m, suitcase on top brings it to 2.00 m."])
def wardrobe():
    g = Grid(32, 28, 41)
    X0, X1, Y1 = 1, 29, 10                                               # carcass x 1..29, y 0..10
    g.box(X0 + 1, 1, 0, X1 - 1, Y1 - 1, 1, "paint_white_shadow")         # recessed plinth
    g.box(X0, 0, 2, X1, Y1, 34, "porcelain_shadow")                      # carcass (inside tone)
    for x in (X0, X1):
        g.box(x, 0, 2, x, Y1, 34, "paint_white")                         # sides
    g.box(X0, 0, 2, X1, Y1, 2, "paint_white")                            # base
    g.box(X0, 0, 33, X1, Y1, 34, "paint_white")                          # top
    g.box(0, 0, 35, 30, Y1 + 1, 35, "paint_white")                       # cornice, 5 cm proud
    g.paint(0, Y1 + 1, 35, 30, Y1 + 1, 35, "paint_white_shadow")
    # near (-X) door, closed: shaker panel, bar handle, kick marks at its foot
    g.box(X0, Y1 + 1, 2, 15, Y1 + 1, 34, "paint_white")
    for (a, b, z0, z1) in ((X0 + 2, 13, 4, 32),):
        g.box(a, Y1 + 1, z0, b, Y1 + 1, z0, "paint_white_shadow")
        g.box(a, Y1 + 1, z1, b, Y1 + 1, z1, "paint_white_shadow")
        g.box(a, Y1 + 1, z0, a, Y1 + 1, z1, "paint_white_shadow")
        g.box(b, Y1 + 1, z0, b, Y1 + 1, z1, "paint_white_shadow")
    g.box(14, Y1 + 2, 17, 14, Y1 + 2, 20, "steel")                       # bar handle
    g.paint(13, Y1 + 1, 16, 15, Y1 + 1, 21, "porcelain_mid")             # grubby round the handle
    for (x0, x1, z) in ((4, 6, 2), (8, 9, 3), (10, 12, 2), (5, 6, 3)):    # kick marks
        g.paint(x0, Y1 + 1, z, x1, Y1 + 1, z, "ash")
    g.paint(9, Y1 + 1, 2, 9, Y1 + 1, 2, "ash_dark")
    g.paint(3, Y1 - 1, 0, 8, Y1 - 1, 1, "concrete")                      # scuffed plinth
    # far (+X) opening: interior, rail, shelf, clothes with gaps
    g.box(16, 1, 3, X1 - 1, Y1, 32, 0)
    g.box(16, 0, 3, X1 - 1, 0, 32, "porcelain_deep")                     # back panel in shadow
    g.box(16, 1, 29, X1 - 1, Y1 - 1, 29, "paint_white_shadow")           # hat shelf
    g.box(16, 5, 27, X1 - 1, 5, 27, "steel_light")                       # hanging rail
    g.box(17, 2, 30, 21, 8, 31, "card")                                  # a box on the shelf
    clothes = [(17, 12, "denim_dark"), (18, 16, "slate_dark"), (19, 12, "cream_mid"),
               (21, 18, "khaki_dark"), (22, 11, "mauve_dark"), (23, 12, "green_dark"),
               (27, 17, "terra_dark"), (28, 12, "bluegrey")]
    for (x, length, c) in clothes:
        g.box(x, 2, 26 - length + 1, x, 8, 26, c)
        g.box(x, 5, 26, x, 5, 27, "steel_dark")                          # hanger hook on the rail
    g.box(24, 5, 26, 24, 5, 26, "steel_dark")                            # empty hangers in the gap
    g.box(26, 5, 26, 26, 5, 26, "steel_dark")
    g.box(17, 3, 3, 20, 7, 4, "red_dark")                                # a bag left on the floor
    # far door, swung open on its +X hinge
    g.box(X1, Y1 + 1, 2, X1, Y1 + 15, 34, "paint_white")
    g.box(X1 + 1, Y1 + 1, 2, X1 + 1, Y1 + 15, 34, "paint_white")
    g.box(X1, Y1 + 3, 4, X1, Y1 + 13, 32, "paint_white_shadow")          # inside face, panel back
    g.box(X1, Y1 + 4, 5, X1, Y1 + 12, 31, "paint_white")
    g.set(X1 + 1, Y1 + 1, 6, "steel_dark")                               # hinges
    g.set(X1 + 1, Y1 + 1, 30, "steel_dark")
    g.box(X1 + 2, Y1 + 14, 17, X1 + 2, Y1 + 14, 20, "steel")             # its handle (outer face)
    # leather suitcase on top
    g.box(3, 2, 36, 18, 9, 39, "leather")
    g.box(3, 2, 39, 18, 9, 39, "leather_hi")
    g.paint(3, 9, 37, 18, 9, 37, "leather_dark")                         # lid seam
    for x in (6, 15):                                                    # straps
        g.paint(x, 2, 36, x, 9, 39, "leather_deep")
    g.box(9, 10, 38, 12, 10, 38, "leather_deep")                          # handle
    g.box(9, 10, 37, 9, 10, 37, "leather_deep")
    g.box(12, 10, 37, 12, 10, 37, "leather_deep")
    g.paint(6, 9, 37, 6, 9, 37, "brass")                                  # buckles
    g.paint(15, 9, 37, 15, 9, 37, "brass")
    return {"grid": g, "footprint_cells": ((0, 30), (0, Y1 + 1))}


# ---------------------------------------------------------------------------
# dresser
# ---------------------------------------------------------------------------
@model("dresser",
       story="An old mahogany chest of drawers handed down twice. Its top drawer was yanked "
             "out and emptied in a hurry - only the rucked lining paper is left - and the "
             "drawer below the middle was shoved shut on a jumper sleeve.",
       details=["Four drawers in a mahogany frame on bracket feet, brass pulls",
                "Top drawer pulled right out and empty, lining paper rucked up",
                "A sage jumper sleeve caught in a closed drawer, hanging down the front",
                "Finish rubbed pale along the top's front edge"],
       exclusions=["No mirror", "No clutter on top"])
def dresser():
    W, D = 25, 10                         # carcass y 0..8, frame lip y = 9
    g = Grid(W, D + 7, 18)
    for (x, y) in ((0, 0), (W - 2, 0), (0, D - 2), (W - 2, D - 2)):      # bracket feet
        g.box(x, y, 0, x + 1, y + 1, 1, "leather_dark")
        g.set(x, y, 0, "leather_deep")
    g.box(1, 1, 1, W - 2, D - 2, 1, "leather_deep")                      # plinth between feet
    g.box(0, 0, 2, W - 1, D - 2, 16, "leather_deep")                     # carcass, dark inside
    for x in (0, W - 1):
        g.box(x, 0, 2, x, D - 1, 16, "leather_dark")
    rails = [2, 6, 10, 14]
    for z in rails:
        g.box(0, 0, z, W - 1, D - 1, z, "leather_dark")
    g.box(0, 0, 17, W - 1, D, 17, "leather_hi")                          # top, 5 cm proud at front
    g.paint(0, D, 17, W - 1, D, 17, "leather")
    round_top_corners(g, 0, 0, W - 1, D, 17)
    g.paint(2, D, 17, 8, D, 17, "leather_hi")                             # rubbed front edge
    g.paint(16, D, 17, 22, D, 17, "leather_hi")
    # drawers: three closed, the top one pulled right out
    for (z0, z1) in ((3, 5), (7, 9), (11, 13)):
        g.box(1, D - 2, z0, W - 2, D - 2, z1, "leather")
        g.paint(1, D - 2, z1, W - 2, D - 2, z1, "leather_hi")             # lit top lip of the front
        for x in (5, W - 6):
            g.box(x - 1, D - 1, (z0 + z1) // 2, x + 1, D - 1, (z0 + z1) // 2, "brass")
    g.box(1, D - 2, 15, W - 2, D - 2, 16, "leather_deep")                # empty slot
    g.box(1, D - 1, 15, W - 2, D + 5, 16, "leather_dark")                # drawer box out 30 cm
    g.box(2, D - 1, 16, W - 3, D + 4, 16, 0)
    g.box(2, D - 1, 15, W - 3, D + 4, 15, "pine_aged")                   # bare drawer bottom
    g.box(1, D + 6, 15, W - 2, D + 6, 16, "leather")                     # its front
    g.paint(1, D + 6, 16, W - 2, D + 6, 16, "leather_hi")
    for x in (5, W - 6):
        g.box(x - 1, D + 7, 15, x + 1, D + 7, 15, "brass")
    g.box(3, D + 1, 15, 9, D + 3, 15, "paper")                           # rucked lining paper
    g.box(5, D + 2, 16, 7, D + 2, 16, "paper")
    g.box(14, D + 2, 15, 17, D + 4, 15, "cream_mid")
    # the jumper sleeve caught in the third drawer, hanging down on the near side
    g.box(3, D - 1, 13, 4, D - 1, 13, "sage")
    g.box(3, D, 6, 4, D, 13, "sage")
    g.paint(3, D, 6, 4, D, 7, "sage_dark")                               # ribbed cuff
    g.paint(3, D, 10, 3, D, 11, "sage_dark")                             # a crease
    return {"grid": g, "footprint_cells": ((0, W - 1), (0, D - 1))}


# ---------------------------------------------------------------------------
# small desk
# ---------------------------------------------------------------------------
@model("small_desk",
       story="A teenager's homework desk under the bedroom window. The laptop was shut and "
             "left; the top pedestal drawer was pulled out by someone hunting for papers, and "
             "the last mug of tea is still on the corner.",
       details=["Oak top on a white three-drawer pedestal and two square legs",
                "Modesty panel at the back", "Top drawer pulled out with loose papers",
                "Closed silver laptop and a mug on the top"],
       exclusions=["No chair (Claude_desk_chair)", "No lamp or screen"],
       notes=["Desk top at 0.75 m; the laptop and mug bring the overall height to 0.85 m."])
def small_desk():
    W, D = 25, 12
    g = Grid(W, D + 5, 17)
    # pedestal on the near (-X) side
    g.box(1, 1, 0, 8, D - 2, 13, "paint_white")
    g.box(1, 1, 0, 8, D - 2, 0, "paint_white_shadow")                    # kick strip
    for (z0, z1) in ((1, 4), (5, 8)):
        g.paint(2, D - 2, z0, 7, D - 2, z1, "paint_white")
        g.paint(2, D - 2, z1, 7, D - 2, z1, "paint_white_shadow")         # gap under the next one
        g.box(4, D - 1, z1 - 1, 5, D - 1, z1 - 1, "steel")                # bar pulls
    # top drawer pulled out
    g.box(2, D - 2, 10, 7, D - 2, 12, "porcelain_deep")                  # dark slot
    g.box(2, D - 1, 10, 7, D + 2, 11, "paint_white_shadow")              # drawer box
    g.box(3, D - 1, 11, 6, D + 1, 11, 0)
    g.box(2, D + 3, 10, 7, D + 3, 12, "paint_white")                     # front
    g.box(4, D + 4, 11, 5, D + 4, 11, "steel")
    g.box(3, D - 1, 11, 5, D + 1, 11, "paper")                           # loose papers
    g.set(6, D, 11, "label_blue")
    # far legs, back panel
    for y in (1, D - 3):
        g.box(W - 3, y, 0, W - 2, y + 1, 13, "paint_white")
        g.box(W - 3, y, 0, W - 2, y + 1, 0, "paint_white_shadow")
    g.box(9, 1, 7, W - 4, 1, 12, "paint_white")                          # modesty panel
    g.box(W - 3, 3, 1, W - 2, D - 4, 1, "paint_white")                   # foot rail
    # top
    g.box(0, 0, 13, W - 1, D - 1, 13, "pine_mid")
    g.paint(0, D - 1, 13, W - 1, D - 1, 13, "pine_light")                # front edge, hand-worn
    round_top_corners(g, 0, 0, W - 1, D - 1, 13)
    # closed laptop and a mug
    g.box(9, 3, 14, 15, 7, 14, "steel_light")
    g.paint(9, 7, 14, 15, 7, 14, "steel")                                # front lip
    g.box(19, 6, 14, 20, 7, 15, "porcelain")
    g.set(21, 6, 15, "porcelain")                                        # handle
    g.set(21, 6, 14, "porcelain")
    return {"grid": g, "footprint_cells": ((0, W - 1), (0, D - 1))}


# ---------------------------------------------------------------------------
# desk chair
# ---------------------------------------------------------------------------
@model("desk_chair",
       story="The cheap swivel chair from the same bedroom desk. The tilt lock broke long ago "
             "so the backrest lolls backwards, and the front corner of the seat has torn "
             "through to the foam from years of being dragged against the desk drawer.",
       details=["Five-star base with castors and a gas lift", "Padded seat on a dark seat pan",
                "Torn front corner showing foam", "Backrest leaning back on a broken tilt"],
       exclusions=["No armrests"])
def desk_chair():
    g = Grid(13, 14, 19)
    cx, cy = 6, 6                                                       # column cell
    for k in range(5):                                                   # five-star base
        a = math.radians(90 + k * 72)
        ex, ey = cx + round(5.2 * math.cos(a)), cy + round(5.2 * math.sin(a))
        line4(g, cx, cy, ex, ey, 1, "charcoal")
        g.set(ex, ey, 0, "black")                                        # castor
        g.set(ex, ey, 1, "iron_edge")
    g.box(cx, cy, 1, cx, cy, 4, "charcoal")                              # column shroud
    g.box(cx, cy, 5, cx, cy, 7, "steel_light")                           # gas lift
    # seat: dark pan under a fabric cushion with rounded corners
    g.box(2, 2, 8, 10, 11, 8, "charcoal")
    g.box(2, 2, 9, 10, 11, 9, "denim_dark")
    g.box(2, 2, 10, 10, 11, 10, "denim")
    for (x, y) in ((2, 2), (10, 2), (2, 11), (10, 11)):
        g.box(x, y, 8, x, y, 10, 0)
    g.paint(3, 11, 10, 9, 11, 10, "denim_hi")                            # rubbed front roll
    # torn front corner (-X, +Y): fabric gone, foam showing
    for (x, y) in ((2, 10), (3, 11), (3, 10), (4, 11)):
        g.paint(x, y, 10, x, y, 10, "almond")
    g.paint(2, 10, 9, 2, 10, 9, "almond_dark")
    g.paint(3, 11, 9, 3, 11, 9, "almond_dark")
    g.paint(4, 10, 10, 4, 10, 10, "denim_hi")                            # frayed edge
    g.paint(5, 11, 10, 5, 11, 10, "denim_hi")
    # back support and backrest, leaning back on the broken tilt
    g.box(cx, 1, 8, cx, 1, 11, "charcoal")
    g.box(cx, 0, 11, cx, 0, 12, "charcoal")
    for (z0, z1, y) in ((12, 14, 1), (15, 17, 0)):
        g.box(2, y, z0, 10, y, z1, "denim")                               # pad
    g.box(2, 0, 12, 10, 0, 14, "charcoal")                               # shell behind the pad
    g.box(3, 0, 18, 9, 0, 18, "denim")
    g.paint(2, 1, 12, 10, 1, 12, "denim_dark")                           # lumbar seam
    g.paint(3, 0, 18, 9, 0, 18, "denim_hi")                              # top roll
    # backrest shell for the upper part sits one cell further back
    g2 = Grid(13, 15, 19)
    g2.v[:, 1:, :] = g.v[:, :, :]
    g2.box(2, 0, 15, 10, 0, 17, "charcoal")
    g2.box(3, 0, 18, 9, 0, 18, "charcoal")
    for (x, y) in ((2, 1), (10, 1)):
        g2.set(x, y, 17, 0)
        g2.set(x, 0, 17, 0)
    return {"grid": g2, "footprint_cells": ((0, 12), (1, 13))}


# ---------------------------------------------------------------------------
# dining chair
# ---------------------------------------------------------------------------
@model("dining_chair",
       story="One of the six chairs bought with the oak dining table. Its seat front and crest "
             "rail are rubbed pale by years of hands pulling it out, and one spindle that "
             "snapped was replaced with a darker one from the hardware shop.",
       details=["Same oak, tones and H-stretcher as Claude_dining_table",
                "Spindle back with a deep crest rail", "One replaced, darker spindle",
                "Seat front and crest rail rubbed pale"],
       exclusions=["No seat pad"],
       notes=["The manifest brief asks for a sage-painted chair that does not quite match the "
              "table; the commission for this batch asks that the chair clearly belongs with "
              "Claude_dining_table, so it is in the table's oak and keeps the brief's "
              "replaced darker spindle as the mismatch.",
              "Seat height 0.45 m, back 0.90 m, 0.45 m wide (the 3-spindle rhythm needs an "
              "odd width)."],
       pairs_with=["Claude_dining_table"])
def dining_chair():
    W = 9
    g = Grid(W, 11, 18)
    for x in (0, W - 1):
        g.box(x, 10, 0, x, 10, 7, "pine_mid")                           # front legs
        g.set(x, 10, 0, "pine_aged")
        g.box(x, 1, 0, x, 1, 17, "pine_mid")                            # back legs into posts
        g.set(x, 1, 0, "pine_aged")
        g.set(x, 1, 17, "pine_light")
        g.box(x, 2, 3, x, 9, 3, "pine_mid")                             # H-stretcher sides
    g.box(1, 5, 3, W - 2, 6, 3, "pine_mid")                             # H-stretcher centre
    g.paint(2, 5, 3, W - 3, 6, 3, "pine_light")                         # polished by feet
    # seat: oak boards, softened front corners, rubbed front edge
    g.box(0, 1, 8, W - 1, 10, 8, "pine_light")
    g.paint(0, 4, 8, W - 1, 7, 8, "pine_mid")                           # middle board
    g.set(0, 10, 8, 0)
    g.set(W - 1, 10, 8, 0)
    g.box(0, 10, 7, W - 1, 10, 7, "pine_mid")                           # front apron
    g.paint(2, 10, 8, W - 3, 10, 8, "pine_hi")
    g.paint(3, 9, 8, W - 4, 9, 8, "pine_hi")
    # spindle back: crest rail, three spindles, the near one a darker replacement
    g.box(0, 1, 15, W - 1, 1, 16, "pine_mid")
    g.paint(1, 1, 16, W - 2, 1, 16, "pine_light")
    g.paint(3, 1, 16, W - 4, 1, 16, "pine_hi")                          # hand-rubbed top
    for x in (2, 4, 6):
        g.box(x, 1, 9, x, 1, 14, "wood_stain" if x == 2 else "pine_light")
    return {"grid": g, "footprint_cells": ((0, W - 1), (1, 10))}
