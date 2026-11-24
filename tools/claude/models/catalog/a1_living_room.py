"""Batch A1 - living room, second family file (creator: Claude).

Companion to a1_living.py (Claude_sofa). Same 0.05 m rhythm (the rug is 0.025 m, from the
manifest), same lighting conventions: X right, Y front (+Y = the side a person uses), Z up,
inclusive cell ranges, everything stands on z = 0. The hero camera sees +Y and -X, so the
story details sit on those faces.

Woods are varied on purpose so a room does not look like one flat-pack set:
  oak      pine_light / pine_mid / pine_aged (coffee table, bookcase - matches the dining table)
  walnut   pine_dark / wood_stain / wood_deep (TV cabinet, sideboard)
  birch    sawdust / pine_hi / pine_light (the nearly new side table)
"""
import math

from catalog_registry import model
from voxkit import Grid, hash01


# ---------------------------------------------------------------------------
# small local helpers
# ---------------------------------------------------------------------------
def round_top_corners(g, x0, y0, x1, y1, z):
    """Knock the four corner cells off a slab at height z (softened corners)."""
    for (x, y) in ((x0, y0), (x1, y0), (x0, y1), (x1, y1)):
        g.set(x, y, z, 0)


def leg(g, x, y, z0, z1, c, foot=None, w=2):
    g.box(x, y, z0, x + w - 1, y + w - 1, z1, c)
    if foot:
        g.box(x, y, z0, x + w - 1, y + w - 1, z0, foot)


# ---------------------------------------------------------------------------
# armchair
# ---------------------------------------------------------------------------
@model("armchair",
       story="Grandad's terracotta club chair by the window. Years of the same head have "
             "sun-faded the top of the back cushion, the seat cushion is pressed flat where he "
             "sat, and the seam on the near arm finally split under his hand, showing the "
             "yellowed foam.",
       details=["Curved upholstered back with a separate back cushion, sun-faded at the top",
                "Seat cushion pressed into a shallow dish",
                "Split seam along the top of the near (-X) arm with foam showing",
                "Rolled arms; short dark wooden legs"],
       exclusions=["No pattern noise in the fabric", "No antimacassar or loose cushions"])
def armchair():
    g = Grid(18, 18, 18)
    for (x, y) in ((1, 2), (15, 2), (1, 15), (15, 15)):               # short, visible legs
        leg(g, x, y, 0, 2, "wood_stain", foot="wood_deep")
    g.box(0, 1, 3, 17, 17, 5, "terra_dark")                           # upholstered base
    # back frame: flat top with rounded shoulders
    g.box(0, 0, 6, 17, 3, 14, "terra")
    g.box(0, 0, 14, 0, 3, 14, 0)
    g.box(17, 0, 14, 17, 3, 14, 0)
    g.box(1, 0, 14, 16, 0, 14, 0)
    g.paint(0, 0, 6, 17, 0, 13, "terra_dark")                          # plain back panel
    # rolled arms: crown rolls over to the outside
    for (x0, xo) in ((0, 0), (15, 17)):
        g.box(x0, 2, 6, x0 + 2, 17, 11, "terra")
        g.box(x0, 4, 12, x0 + 2, 16, 12, "terra")
        g.box(xo, 4, 12, xo, 16, 12, 0)
        g.paint(x0, 17, 6, x0 + 2, 17, 6, "terra_dark")                # piping at the arm foot
    # back cushion standing proud of the frame (like the sofa's), its top sun-faded
    g.box(3, 1, 8, 14, 5, 16, "terra")
    g.box(4, 2, 17, 13, 4, 17, "terra")
    for x in (3, 14):
        g.box(x, 1, 16, x, 1, 16, 0)
        g.box(x, 5, 16, x, 5, 16, 0)
    g.box(4, 6, 9, 13, 6, 13, "terra")                                 # cushion belly
    g.paint(3, 1, 8, 3, 6, 16, "terra_dark")                           # side seams
    g.paint(14, 1, 8, 14, 6, 16, "terra_dark")
    g.paint(5, 2, 17, 12, 4, 17, "terra_hi")                           # faded where the head was
    g.paint(5, 5, 14, 12, 5, 16, "terra_hi")
    g.paint(6, 6, 13, 11, 6, 13, "terra_hi")
    # seat cushion, pressed into a shallow dish where he sat
    g.box(3, 7, 6, 14, 17, 8, "terra")
    g.paint(3, 17, 6, 14, 17, 6, "terra_dark")                         # seam under the front
    g.box(4, 8, 8, 13, 16, 8, 0)
    for (x, y) in ((4, 8), (13, 8), (4, 16), (13, 16)):
        g.set(x, y, 8, "terra")                                        # rounded dish corners
    g.paint(3, 17, 8, 14, 17, 8, "terra_hi")                           # front roll, lit
    # split seam on the near (-X) arm: yellowed foam showing along the crown
    g.paint(1, 8, 12, 1, 13, 12, "card_hi")
    g.paint(2, 8, 12, 2, 13, 12, "terra_hi")                           # lifted fabric lip
    g.paint(0, 10, 11, 0, 12, 11, "terra_dark")                        # seam opening down the side
    return {"grid": g, "footprint_cells": ((0, 17), (0, 17))}


# ---------------------------------------------------------------------------
# coffee table
# ---------------------------------------------------------------------------
@model("coffee_table",
       story="A solid oak coffee table that took the knocks of a family living room: the front "
             "corner was chipped when the sofa was dragged past it and never filled, and the "
             "shelf underneath still holds the last week's paper and two magazines.",
       details=["Three-board oak top with softened corners and a chipped front corner",
                "Square legs, plain apron", "Lower shelf with a folded newspaper and magazines"],
       exclusions=["No mugs or remotes baked on top (separate pickups)"])
def coffee_table():
    W, D = 23, 12
    g = Grid(W, D, 9)
    for (x, y) in ((1, 1), (W - 3, 1), (1, D - 3), (W - 3, D - 3)):
        leg(g, x, y, 0, 7, "pine_mid", foot="pine_aged")
    g.box(1, 1, 7, W - 2, D - 2, 7, "pine_mid")                       # apron (hollowed below)
    g.box(3, 3, 7, W - 4, D - 4, 7, 0)
    g.paint(1, D - 2, 7, W - 2, D - 2, 7, "pine_aged")                 # apron under the top
    # top: three boards along X
    for (y0, y1, c) in ((0, 3, "pine_light"), (4, 7, "pine_mid"), (8, 11, "pine_light")):
        g.box(0, y0, 8, W - 1, y1, 8, c)
    round_top_corners(g, 0, 0, W - 1, D - 1, 8)
    # chipped near corner (-X, +Y): a bite out of the top, raw pale wood in the break
    for (x, y) in ((1, 11), (0, 10), (1, 10)):
        g.set(x, y, 8, 0)
    for (x, y) in ((2, 11), (2, 10), (1, 9), (0, 9)):
        g.set(x, y, 8, "pine_hi")
    g.set(1, 10, 7, "pine_hi")                                         # apron corner exposed
    # lower shelf
    g.box(1, 2, 2, W - 2, D - 3, 2, "pine_aged")
    g.box(3, 1, 2, W - 4, D - 2, 2, "pine_aged")
    # the week's newspaper, folded in half, and two magazines on the shelf
    g.box(3, 3, 3, 9, 8, 3, "paper")
    g.paint(3, 6, 3, 9, 6, 3, "cream_mid")                             # print block
    g.paint(3, 8, 3, 9, 8, 3, "cream_shadow")                          # folded edge
    g.box(13, 3, 3, 18, 8, 3, "bluegrey_hi")                           # magazine
    g.box(14, 4, 4, 18, 9, 4, "terra_hi")                              # magazine on top
    g.paint(14, 9, 4, 18, 9, 4, "paper")                               # page edges
    return g


# ---------------------------------------------------------------------------
# television
# ---------------------------------------------------------------------------
@model("television",
       story="The living-room television, switched off at the wall when the power went. "
             "Someone knocked it reaching for the cabinet - a hairline crack now runs across the "
             "near top corner - and dust has settled along its top edge since.",
       details=["Unbranded flat panel on a centre foot", "Dark screen with a soft window sheen",
                "Hairline crack across the near top corner", "Dust along the top edge",
                "Thicker electronics box on the back"],
       exclusions=["No logo, no lit screen, no buttons or text"])
def television():
    W = 22
    g = Grid(W, 4, 14)
    # foot and neck
    g.box(7, 0, 0, 14, 3, 0, "steel_dark")
    round_top_corners(g, 7, 0, 14, 3, 0)
    g.paint(8, 3, 0, 13, 3, 0, "steel")                                # lit front edge
    g.box(10, 0, 1, 11, 0, 3, "charcoal")
    # panel: frame and screen
    g.box(0, 1, 2, W - 1, 1, 13, "charcoal")
    g.box(1, 1, 3, W - 2, 1, 12, "screen")
    g.box(5, 0, 4, W - 6, 0, 10, "charcoal")                          # electronics box
    g.paint(5, 0, 10, W - 6, 0, 10, "steel_dark")
    # faint sheen: the far upper part of the glass catches the window (a value lift, not a stripe)
    for z in range(3, 13):
        for x in range(1, W - 1):
            if x + 1.3 * z > 27:
                g.set(x, 1, z, "water_dark")
    # hairline crack across the near (-X) top corner, from a knock at the edge
    for (x, z) in ((1, 7), (1, 8), (2, 8), (2, 9), (3, 9), (3, 10), (4, 10), (5, 10), (5, 11),
                   (6, 11), (6, 12)):
        g.set(x, 1, z, "screen_sheen")
    g.set(1, 1, 12, "glass_dark")                                       # impact point at the corner
    g.set(2, 1, 12, "screen_sheen")
    g.set(2, 1, 11, "screen_sheen")
    # catch-light on the lower frame edge, a film of dust along the top
    g.paint(0, 1, 2, W - 1, 1, 2, "steel_dark")
    g.paint(3, 1, 13, W - 4, 1, 13, "iron_edge")
    g.paint(5, 0, 10, W - 6, 0, 10, "iron_edge")
    return {"grid": g, "footprint_cells": ((7, 14), (0, 3))}


# ---------------------------------------------------------------------------
# TV cabinet
# ---------------------------------------------------------------------------
@model("tv_cabinet",
       story="A walnut media cabinet that has been moved through three houses. The near door "
             "came off its top hinge and now hangs askew on the bottom one; the set-top box "
             "is still in the open bay, its cable pulled out when someone took the console.",
       details=["Recessed doors inside a walnut frame with brass bar pulls, on short legs",
                "Open middle bay with a set-top box", "A loose cable trailing to the floor",
                "Near door hanging askew off its top hinge, dark gap above it",
                "Front edge of the top rubbed pale above the bay"],
       exclusions=["No television on top (separate model)", "No logo on the box"])
def tv_cabinet():
    W, D = 34, 9                        # carcass y 0..7, doors at y = 7, frame lip at y = 8
    g = Grid(W, D + 3, 12)
    for (x, y) in ((1, 1), (W - 3, 1), (1, D - 3), (W - 3, D - 3)):   # short legs
        leg(g, x, y, 0, 1, "wood_stain", foot="wood_deep")
    g.box(0, 0, 2, W - 1, D - 2, 10, "wood_deep")                      # carcass (dark inside)
    for x in (0, 11, 22, W - 1):                                        # sides and dividers
        g.box(x, 0, 2, x, D - 1, 10, "wood_stain")
    g.box(0, 0, 11, W - 1, D - 1, 11, "pine_dark")                     # top
    g.paint(0, D - 1, 11, W - 1, D - 1, 11, "wood_stain")              # top's front edge
    g.paint(13, D - 1, 11, 20, D - 1, 11, "pine_aged")                 # rubbed above the bay
    g.box(0, 0, 2, W - 1, D - 1, 2, "wood_stain")                      # bottom rail
    round_top_corners(g, 0, 0, W - 1, D - 1, 11)
    # far (+X) door, intact: frame-and-panel, bar pull, finish worn round the pull
    g.box(23, D - 2, 3, 32, D - 2, 10, "pine_dark")
    g.box(24, D - 2, 4, 31, D - 2, 9, "wood_stain")
    g.box(24, D - 1, 6, 24, D - 1, 7, "brass_dark")
    g.paint(23, D - 2, 6, 23, D - 2, 7, "pine_aged")
    # open middle bay: back panel, set-top box, a cable pulled out to the floor
    g.box(12, 1, 3, 21, D - 1, 10, 0)
    g.box(13, 2, 3, 19, 5, 3, "steel_dark")                            # set-top box
    g.paint(13, 5, 3, 19, 5, 3, "charcoal")
    g.set(18, 5, 3, "steel_light")                                      # dead standby light
    for p in ((20, 4, 3), (20, 5, 3), (20, 6, 3), (20, 7, 3), (20, 8, 3), (20, 9, 3),
              (20, 9, 2), (20, 9, 1), (20, 9, 0), (21, 9, 0), (21, 10, 0), (22, 10, 0),
              (23, 10, 0), (23, 11, 0)):
        g.set(*p, "black")
    # near (-X) door: off its top hinge, hanging askew in front of its opening
    g.box(1, D - 2, 3, 10, D - 2, 10, "wood_deep")                     # opening (dark)
    tops = [10, 10, 10, 9, 9, 9, 9, 8, 8, 8]
    bots = [3, 3, 3, 3, 2, 2, 2, 2, 1, 1]
    for i, x in enumerate(range(1, 11)):
        g.box(x, D, bots[i], x, D, tops[i], "pine_dark")
        if 2 <= i <= 8:
            g.box(x, D, bots[i] + 1, x, D, tops[i] - 1, "wood_stain")  # the panel field
    g.box(9, D + 1, 5, 9, D + 1, 6, "brass_dark")                      # its pull
    g.box(1, D - 1, 3, 1, D - 1, 4, "brass")                           # the surviving hinge
    g.set(1, D - 1, 9, "brass_dark")                                   # torn top hinge plate
    return {"grid": g, "footprint_cells": ((0, W - 1), (0, D - 1))}


# ---------------------------------------------------------------------------
# bookshelf
# ---------------------------------------------------------------------------
def book_row(g, x, z, y0, y1, specs):
    """Upright books from x rightwards. spec: (height, colour) | ('gap', n) |
    ('lean', height, colour) - a book leaning left against its neighbour, base one cell out."""
    for sp in specs:
        if sp[0] == "gap":
            x += sp[1]
            continue
        if sp[0] == "lean":
            _, h, c = sp
            lo = h // 2
            g.box(x + 1, y0, z, x + 1, y1, z + lo - 1, c)
            g.box(x, y0, z + lo, x, y1, z + h - 2, c)
            g.box(x + 1, y0, z + lo, x + 1, y1, z + lo, c)
            x += 2
            continue
        h, c = sp
        back = 1 if hash01(x, z, seed=11) < 0.3 else 0                 # some pushed further in
        g.box(x, y0, z, x, y1 - back, z + h - 1, c)
        x += 1
    return x


@model("bookshelf",
       story="The family bookcase, oak veneer over chipboard. When people left they took a few "
             "favourites and a run of the children's books, so the rows lean into the gaps; the "
             "holiday photo and the box of old cables stayed behind.",
       details=["Five shelves in an oak-veneer carcass on a recessed plinth",
                "Books in muted colours, standing, leaning into gaps and lying in a short stack",
                "A small lidded box and a framed photo", "Veneer lifting on the near front edge"],
       exclusions=["No readable titles or text", "No ornaments clutter"])
def bookshelf():
    W, D, H = 25, 8, 37
    g = Grid(W, D, H)
    g.box(0, 0, 0, W - 1, D - 1, H - 1, "pine_aged")                   # carcass block
    g.box(1, 1, 0, W - 2, D - 1, 1, 0)
    g.box(1, 1, 0, W - 2, D - 2, 1, "pine_dark")                       # recessed plinth
    shelves = [2, 9, 16, 23, 30]
    for i, z in enumerate(shelves):                                    # open compartments
        z1 = (shelves[i + 1] - 1) if i + 1 < len(shelves) else H - 2
        g.box(1, 1, z + 1, W - 2, D - 1, z1, 0)
    for z in shelves + [H - 1]:
        g.paint(0, D - 1, z, W - 1, D - 1, z, "pine_light")            # shelf front edges
    g.paint(0, D - 1, 0, 0, D - 1, H - 1, "pine_light")                # side front edges
    g.paint(W - 1, D - 1, 0, W - 1, D - 1, H - 1, "pine_light")
    g.paint(0, 0, H - 1, W - 1, D - 1, H - 1, "pine_mid")              # top
    g.paint(1, 0, 2, W - 2, 0, H - 2, "pine_dark")                     # back panel (shadowed)
    g.paint(0, D - 1, 3, 0, D - 1, 6, "pine_hi")                       # veneer lifting, near edge
    y0, y1 = 2, 6
    # shelf 1 (bottom, tallest books)
    x = book_row(g, 1, 3, y0, y1, [(5, "blue_deep"), (5, "blue_dark"), (5, "red_dark"),
                                   (4, "cream_shadow"), (5, "green_deep"), (5, "olive_dark"),
                                   (4, "mustard_deep"), (5, "red_deep"), (5, "bluegrey_deep"),
                                   (4, "wool_dark")])
    g.box(x + 1, 2, 3, x + 5, 6, 4, "card")                             # lidded box of cables
    g.box(x + 1, 2, 5, x + 5, 6, 5, "card_hi")
    g.paint(x + 1, 6, 5, x + 5, 6, 5, "card_dark")
    book_row(g, x + 7, 3, y0, y1, [(5, "terra_deep"), (5, "blue_dark"), (4, "sage_deep"),
                                   (5, "mauve_deep"), (5, "wood_stain")])
    # shelf 2: a gap where the children's books were, two leaning into it
    x = book_row(g, 1, 10, y0, y1, [(5, "mustard_dark"), (5, "teal_dark"), (4, "cream_mid"),
                                    (5, "red_dark"), (5, "blue_mid"), (4, "olive"),
                                    (5, "terra_dark"), ("lean", 5, "sage_dark"),
                                    ("gap", 6), ("lean", 4, "blue_dark")])
    x = book_row(g, x + 1, 10, y0, y1, [(4, "mauve_dark"), (5, "green_dark"),
                                        (5, "bluegrey_dark"), (4, "cream_shadow"),
                                        (5, "red_deep")])
    # shelf 3: framed holiday photo, a short stack lying flat, books
    g.box(2, 6, 17, 5, 6, 20, "wood_stain")                             # photo frame
    g.box(3, 6, 18, 4, 6, 18, "sage")                                   # the photo: grass..
    g.box(3, 6, 19, 4, 6, 19, "bluegrey_hi")                            # ..and sky
    g.box(3, 5, 17, 4, 5, 18, "wood_deep")                              # strut behind
    for i, c in enumerate(("blue_dark", "cream_mid", "terra_dark")):    # stack lying flat
        g.box(7, 2 + (i % 2), 17 + i, 11, 5 + (i % 2), 17 + i, c)
    book_row(g, 13, 17, y0, y1, [(5, "olive_dark"), (5, "blue_deep"), (4, "mustard_dark"),
                                 (5, "red_dark"), (5, "teal_deep"), (4, "wool"),
                                 (5, "blue_dark"), (5, "maroon"), (4, "green_dark"),
                                 (5, "cream_shadow"), (5, "slate_dark")])
    # shelf 4: half empty - only a few left, one fallen over
    x = book_row(g, 1, 24, y0, y1, [(5, "red_deep"), (5, "bluegrey_dark"), (4, "cream_mid"),
                                    (5, "olive_dark"), (5, "terra_dark"), (4, "teal_dark"),
                                    ("lean", 5, "mustard_dark")])
    g.box(x + 4, 2, 24, x + 8, 5, 24, "blue_dark")                      # one fallen flat
    book_row(g, W - 6, 24, y0, y1, [(5, "green_deep"), (5, "red_dark"), (4, "wool_dark"),
                                    (5, "blue_deep")])
    # shelf 5 (top): tall atlases and a few paperbacks
    book_row(g, 1, 31, y0, y1, [(4, "blue_deep"), (4, "red_deep"), (3, "cream_shadow"),
                                (4, "green_dark"), (3, "mustard_dark"), (4, "bluegrey_deep"),
                                (3, "terra_dark"), (4, "olive_dark"), (4, "mauve_deep"),
                                (3, "cream_mid"), (4, "teal_deep"), (4, "red_dark")])
    return g


# ---------------------------------------------------------------------------
# side table
# ---------------------------------------------------------------------------
@model("side_table",
       story="Bought new a month before everything stopped and still has its showroom finish. "
             "Its only mark is the cork coaster someone always remembered to use.",
       details=["Pale birch top on four square legs", "One drawer with a dark wooden knob",
                "Lower shelf between the legs",
                "A cork coaster on the top"],
       exclusions=["No wear: it is the clean contrast to the worn pieces",
                   "No glass or lamp on top (separate pickups)"])
def side_table():
    g = Grid(11, 10, 11)
    for (x, y) in ((1, 1), (9, 1), (1, 8), (9, 8)):
        g.box(x, y, 0, x, y, 9, "pine_hi")
    g.box(1, 1, 7, 9, 8, 9, "pine_hi")                                  # drawer box / apron
    g.paint(2, 8, 7, 8, 8, 9, "sawdust")                                # drawer front
    g.paint(2, 8, 7, 8, 8, 7, "pine_light")                             # shadow line under it
    g.set(5, 9, 8, "wood_stain")                                        # knob
    g.box(0, 0, 10, 10, 9, 10, "sawdust")                               # top
    round_top_corners(g, 0, 0, 10, 9, 10)
    g.paint(2, 6, 10, 3, 7, 10, "card")                                 # cork coaster
    g.box(1, 1, 2, 9, 8, 2, "pine_light")                               # lower shelf
    g.paint(1, 8, 2, 9, 8, 2, "pine_hi")
    return g


# ---------------------------------------------------------------------------
# floor lamp
# ---------------------------------------------------------------------------
@model("floor_lamp",
       story="The reading lamp behind the sofa. Its linen shade was knocked in the rush to "
             "leave and the near rim stayed dented; the cord still trails across the floor to a "
             "socket that has not worked for months.",
       details=["Weighted round iron base", "Thin dark pole with a lighter collar and switch",
                "Linen drum shade with trim bands, its near rim dented by a knock",
                "Unlit bulb inside the shade under a top diffuser", "Cord trailing across the floor"],
       exclusions=["Nothing lit or glowing"],
       notes=["The trailing cord adds about 0.3 m to the footprint in X/Y; footprint_cells "
              "covers only the base.",
              "The brief's 'slightly tilted' shade is below one cell at 0.05 m (about 3 cm of "
              "rim drop); modelled as a one-cell step it read as a broken shade, so the knock "
              "is shown as a dent in the near rim instead."])
def floor_lamp():
    ox, oy = 4, 0
    g = Grid(ox + 10, oy + 14, 34)
    cx, cy = ox + 4.5, oy + 4.5                                         # pole cell (ox+4, oy+4)
    px, py = ox + 4, oy + 4
    for (i, j) in g.disc_cells(cx, cy, 3.5):                             # weighted base
        g.set(i, j, 0, "iron")
    for (i, j) in g.ring_cells(cx, cy, 3.5):
        g.set(i, j, 0, "iron_edge")
    g.box(px, py, 1, px, py, 26, "charcoal")                            # pole
    g.box(px, py, 1, px, py, 2, "iron_edge")                            # collar
    g.set(px, py, 14, "steel")                                          # joint sleeve
    g.set(px, py, 27, "steel_dark")                                     # socket
    g.set(px, py, 28, "bulb_warm")                                      # unlit bulb
    # linen drum shade on a bottom fitter; the knock left a dent in the near rim
    for (i, j) in g.ring_cells(cx, cy, 4.5):
        g.box(i, j, 26, i, j, 31, "cream")
        g.set(i, j, 26, "cream_mid")                                    # bottom trim
        g.set(i, j, 31, "cream_mid")                                    # top trim
    for i in range(int(cx - 4.5) + 1, int(cx + 4.5)):                   # fitter bar under the bulb
        if not g.get(i, py, 26):
            g.set(i, py, 26, "steel_dark")
    for (i, j) in g.disc_cells(cx, cy, 4.5):                             # top diffuser
        if not g.get(i, j, 31):
            g.set(i, j, 31, "cream_shadow")
    g.paint(px, oy + 0, 26, px, oy + 0, 31, "cream_shadow")             # back seam
    for (i, j) in ((ox + 1, oy + 7), (ox + 2, oy + 8)):                 # dent: near rim pushed in
        g.box(i, j, 26, i, j, 28, 0)
        g.box(i + 1, j - 1, 26, i + 1, j - 1, 28, "cream_shadow")
    g.set(ox + 1, oy + 7, 29, "cream_shadow")
    g.set(ox + 2, oy + 8, 29, "cream_shadow")
    # cord: out of the base and trailing toward the camera in a lazy curve
    cord = [(ox + 1, oy + 5), (ox + 0, oy + 5), (ox - 1, oy + 5), (ox - 1, oy + 6),
            (ox - 2, oy + 6), (ox - 2, oy + 7), (ox - 2, oy + 8), (ox - 3, oy + 8),
            (ox - 3, oy + 9), (ox - 3, oy + 10), (ox - 3, oy + 11), (ox - 2, oy + 11),
            (ox - 2, oy + 12), (ox - 1, oy + 12), (ox - 1, oy + 13)]
    for (i, j) in cord:
        g.set(i, j, 0, "black")
    g.set(px, py + 1, 12, "black")                                      # inline switch on the cord
    return {"grid": g, "footprint_cells": ((ox + 1, ox + 7), (oy + 1, oy + 7))}


# ---------------------------------------------------------------------------
# small storage cabinet
# ---------------------------------------------------------------------------
@model("small_storage_cabinet",
       story="A sage-painted cupboard from the hallway that held the towels. The near door's "
             "paint is worn through to the pine around its knob from years of hands; the other "
             "door was left open by whoever took the first-aid box from the top shelf.",
       details=["Painted sage carcass on four short feet", "Recessed doors with wooden knobs",
                "Paint worn through to bare pine around the near door's knob",
                "Far door left open showing two shelves and stacks of folded towels"],
       notes=["The far door is swung right open rather than a few degrees ajar: an angled "
              "1-cell door at 0.05 m becomes a jagged staircase and hides the towels.",
              "The open door adds 0.45 m in +Y; footprint_cells covers only the carcass."],
       exclusions=["No first-aid box (taken; it is a separate pickup)"])
def small_storage_cabinet():
    W, D = 20, 9                        # carcass y 0..7, frame lip y = 8
    g = Grid(W + 1, D + 6, 22)
    for (x, y) in ((1, 1), (W - 3, 1), (1, D - 3), (W - 3, D - 3)):
        leg(g, x, y, 0, 1, "sage_dark", foot="sage_deep")
    g.box(0, 0, 2, W - 1, D - 1, 20, "sage")                           # carcass
    g.box(0, 0, 21, W - 1, D - 1, 21, "sage_hi")                       # top
    round_top_corners(g, 0, 0, W - 1, D - 1, 21)
    g.box(1, 1, 3, W - 2, D - 1, 19, 0)                                 # open the front
    g.box(1, 0, 3, W - 2, 0, 19, "sage_dark")                           # back, inside
    for z in (8, 14):                                                   # shelves
        g.box(1, 1, z, W - 2, D - 2, z, "sage")
        g.paint(1, D - 2, z, W - 2, D - 2, z, "sage_hi")
    # towels on the middle shelf (behind the open door) and spare ones below
    for (x0, cols) in ((10, ("cream_hi", "bluegrey_hi", "cream")), (14, ("terra_hi", "cream_mid",
                                                                         "bluegrey"))):
        for k, c in enumerate(cols):
            g.box(x0, 2, 9 + k, x0 + 3, 6, 9 + k, c)
    g.box(11, 2, 3, 17, 6, 4, "cream_shadow")                           # folded bath sheet
    g.box(11, 2, 5, 17, 6, 5, "cream_mid")
    g.box(11, 2, 15, 13, 5, 16, "card")                                 # box of bits, top shelf
    # near door (closed), knob and the worn-through paint
    g.box(1, D - 2, 3, 9, D - 2, 19, "sage")
    g.box(2, D - 2, 4, 8, D - 2, 18, "sage_dark")                      # recessed panel
    g.box(3, D - 2, 5, 7, D - 2, 17, "sage")
    g.set(8, D - 1, 11, "pine_dark")                                    # knob
    for (z, xa) in ((13, 8), (12, 7), (11, 7), (10, 8), (9, 9)):         # bare wood under hands
        g.paint(xa, D - 2, z, 9, D - 2, z, "pine_aged")
    g.paint(9, D - 2, 10, 9, D - 2, 12, "pine_mid")
    # far door swung open on its +X hinge
    g.box(W - 1, D, 3, W - 1, D + 8, 19, "sage")
    g.box(W - 1, D + 1, 4, W - 1, D + 7, 18, "sage_dark")              # inside face: panel back
    g.box(W - 1, D + 1, 5, W - 1, D + 6, 17, "sage")
    g.box(W - 1, D + 8, 3, W - 1, D + 8, 19, "sage_hi")                # free edge
    g.set(W, D + 7, 11, "pine_dark")                                    # its knob (outer face)
    g.set(W - 1, D - 1, 5, "steel_dark")                                # hinges
    g.set(W - 1, D - 1, 17, "steel_dark")
    return {"grid": g, "footprint_cells": ((0, W - 1), (0, D - 1))}


# ---------------------------------------------------------------------------
# rug (0.025 m cells, from the manifest: a 2.5 cm weave layer instead of a 5 cm slab)
# ---------------------------------------------------------------------------
_RUG_UNDER = {"wool": "wgrey_warm", "blue_dark": "bluegrey_dark", "blue_deep": "bluegrey_deep",
              "cream_mid": "cream_shadow", "red_dark": "red_deep", "cream_shadow": "cream_deep",
              "wool_dark": "wgrey_mid", "bluegrey_dark": "bluegrey_deep",
              "terra_dark": "red_deep", "cream_deep": "wgrey_mid"}
_RUG_WORN = {"wool": "wool_dark", "blue_dark": "bluegrey_dark", "blue_deep": "blue_dark",
             "cream_mid": "cream_deep", "red_dark": "terra_dark", "cream_shadow": "cream_deep"}


@model("rug",
       story="A flat-woven living-room rug laid across the route from the hall to the kitchen. "
             "A grey track is trodden into it along that line, and the near corner got kicked "
             "over in the last rush through the room and was never laid flat again.",
       details=["Oatmeal field, slate-blue border with a running diamond motif and a brick "
                "inner stripe", "Fringes on the short ends",
                "Trodden walking track crossing it front to back",
                "Near corner folded over, showing the duller reverse"],
       exclusions=["No pile texture noise; flat weave", "No furniture dents"],
       why="A flat-weave rug is about 1 cm thick: 2.5 cm is the thinnest honest layer, and the "
           "finer cells carry the border motif and fringe.")
def rug():
    W, D, F = 96, 70, 3
    g = Grid(W + 2 * F, D, 3)

    def pattern(x, y):
        dx, dy = min(x, W - 1 - x), min(y, D - 1 - y)
        d = min(dx, dy)
        if d <= 1:
            return "blue_deep"
        if d <= 9:
            t = y if dx <= dy else x
            m = abs((t % 12) - 5.5) + abs((d - 2) - 3.5)
            return "cream_mid" if m == 4 else ("red_dark" if m == 1 else "blue_dark")
        if d <= 11:
            return "red_dark"
        if d == 12:
            return "cream_mid"
        return "wool"


    def worn(x, y):
        """0 = untouched, 1 = edge of the track, 2 = trodden core. A gently curving track."""
        c = 56 + (D - 1 - y) * 0.2 + 3.0 * math.sin(y / 11.0)
        hw = 7.0 + 1.2 * math.sin(y / 7.0 + 1.0)
        d = abs(x + 0.5 - c)
        return 2 if d <= hw - 2.5 else (1 if d <= hw else 0)

    cells = {}
    for x in range(W):
        for y in range(D):
            c = pattern(x, y)
            w = worn(x, y)
            if w == 2 or (w == 1 and c != "wool"):
                c = _RUG_WORN.get(c, c)
            elif w == 1:
                c = "wgrey_warm"
            cells[(x, y)] = c
    for y in range(2, D - 2, 2):                                         # fringes
        for k in range(1, F + 1):
            c = "cream_shadow" if k == F else "cream_mid"
            cells[(-k, y)] = c
            cells[(W - 1 + k, y)] = c
    # near (-X, +Y) corner folded over along a 45-degree line
    K = 21
    for (x, y), c in cells.items():
        Y = D - 1 - y
        if x + Y < K - 1:                                                # the lifted flap
            fx, fY = K - 1 - Y, K - 1 - x
            g.set(fx + F, D - 1 - fY, 1, _RUG_UNDER.get(c, c))
        else:
            g.set(x + F, y, 0, c)
            if x + Y == K - 1:                                           # the bend
                g.set(x + F, y, 1, _RUG_UNDER.get(c, c))
    return {"grid": g, "footprint_cells": ((F, F + W - 1), (0, D - 1))}


# ---------------------------------------------------------------------------
# stool
# ---------------------------------------------------------------------------
@model("stool",
       story="The kitchen stool everyone perched on to talk to the cook. Its seat is rubbed "
             "pale in the middle and the front footrest is worn to bare wood by heels.",
       details=["Round-ish seat with a pale, worn centre", "Four square legs with a seat rail",
                "Footrest rungs on all four sides, the front one heel-worn"],
       exclusions=["No cushion"])
def stool():
    g = Grid(9, 9, 14)
    for (x, y) in ((1, 1), (7, 1), (1, 7), (7, 7)):
        g.box(x, y, 0, x, y, 12, "pine_dark")
        g.set(x, y, 0, "wood_stain")
    for z, c in ((12, "pine_dark"), (4, "pine_dark")):                  # seat rail, footrests
        g.box(1, 1, z, 7, 1, z, c)
        g.box(1, 7, z, 7, 7, z, c)
        g.box(1, 1, z, 1, 7, z, c)
        g.box(7, 1, z, 7, 7, z, c)
    g.paint(2, 7, 4, 6, 7, 4, "pine_mid")                                # heel-worn front rung
    g.paint(3, 7, 4, 5, 7, 4, "pine_light")
    g.paint(1, 3, 4, 1, 5, 4, "pine_aged")                               # and the near side
    for (i, j) in g.disc_cells(4.5, 4.5, 4.5):                           # seat
        r = (((i + 0.5 - 4.5) / 1.25) ** 2 + (j + 0.5 - 4.9) ** 2) ** 0.5
        g.set(i, j, 13, "pine_mid" if r < 1.1 else ("pine_aged" if r < 2.2 else "pine_dark"))
    return g


# ---------------------------------------------------------------------------
# sideboard
# ---------------------------------------------------------------------------
@model("sideboard",
       story="The good walnut sideboard in the dining room. Someone went through it for the "
             "candles and left the near drawer pulled out; the fruit bowl is still on top, and "
             "the wedding photo beside it was laid face-down and left that way.",
       details=["Three drawers over two frame-and-panel doors on short legs, brass pulls",
                "Near drawer pulled out, paper lining inside", "Stoneware fruit bowl on top",
                "Picture frame lying face-down, cardboard back showing"],
       exclusions=["No fruit or crockery inside the bowl (separate pickups)"])
def sideboard():
    W, D = 35, 10                         # carcass y 0..8, frame lip y = 9
    g = Grid(W, D + 5, 18)
    for (x, y) in ((1, 1), (W - 3, 1), (1, D - 3), (W - 3, D - 3)):
        leg(g, x, y, 0, 2, "wood_stain", foot="wood_deep")
    g.box(0, 0, 3, W - 1, D - 2, 14, "wood_deep")                        # carcass, dark inside
    for x in (0, 11, 17, 23, W - 1):
        z0, z1 = (11, 14) if x in (11, 23) else ((3, 11) if x == 17 else (3, 14))
        g.box(x, 0, z0, x, D - 1, z1, "wood_stain")
    for z in (3, 11):
        g.box(0, 0, z, W - 1, D - 1, z, "wood_stain")                    # bottom and mid rails
    g.paint(0, D - 1, 3, W - 1, D - 1, 3, "wood_deep")
    g.box(0, 0, 15, W - 1, D - 1, 15, "pine_dark")                       # top
    g.paint(0, D - 1, 15, W - 1, D - 1, 15, "wood_stain")
    round_top_corners(g, 0, 0, W - 1, D - 1, 15)
    # doors: frame and raised field, knobs by the centre stile
    for (x0, x1) in ((1, 16), (18, 33)):
        g.box(x0, D - 2, 4, x1, D - 2, 10, "pine_dark")
        g.box(x0 + 1, D - 2, 5, x1 - 1, D - 2, 9, "wood_stain")
    g.set(15, D - 1, 7, "brass")
    g.set(19, D - 1, 7, "brass")
    # drawers: the two on the +X side closed
    for (x0, x1) in ((12, 22), (24, 33)):
        g.box(x0, D - 2, 12, x1, D - 2, 14, "pine_dark")
        m = (x0 + x1) // 2
        g.box(m - 1, D - 1, 13, m, D - 1, 13, "brass_dark")
    # near drawer pulled out ~25 cm: paper lining, lower sides, front with its pull
    g.box(1, D - 2, 12, 10, D - 2, 14, "wood_deep")                      # the dark slot
    g.box(1, D - 1, 12, 10, D + 3, 13, "pine_aged")
    g.box(2, D - 1, 13, 9, D + 2, 13, 0)
    g.box(2, D - 1, 12, 9, D + 2, 12, "cream_mid")                       # lining paper
    g.box(1, D + 3, 12, 10, D + 3, 14, "pine_dark")
    g.box(5, D + 4, 13, 6, D + 4, 13, "brass_dark")
    # stoneware fruit bowl
    bx, by = 26.0, 5.0
    for (i, j) in g.disc_cells(bx, by, 3.0):
        g.set(i, j, 16, "teal")
    for (i, j) in g.ring_cells(bx, by, 3.0):
        g.set(i, j, 17, "teal_dark")
        g.set(i, j, 16, "teal_dark")
    # wedding photo, face-down: frame edge round a cardboard back
    g.box(4, 2, 16, 9, 6, 16, "wood_stain")
    g.box(5, 3, 16, 8, 5, 16, "card_dark")
    # a little wear: the top's front edge rubbed above the drawers
    g.paint(13, D - 1, 15, 21, D - 1, 15, "pine_dark")
    return {"grid": g, "footprint_cells": ((0, W - 1), (0, D - 1))}


# ---------------------------------------------------------------------------
# small shelf
# ---------------------------------------------------------------------------
@model("small_shelf",
       story="A cheap pine shelf, painted blue-grey years ago, that stood in the corner of the "
             "kitchen holding the everyday plates and the jam jars. Its joints have worked loose "
             "and the top half has racked over to one side.",
       details=["Four posts and four boards; the posts jog one cell sideways above the middle "
                "shelf where the joints have worked loose",
                "Painted blue-grey, chipped to pine on the front edges",
                "Two plates standing at the back, a short stack in front, a crock and "
                "lidded jars"],
       exclusions=["No full dinner service; a few everyday things"],
       notes=["Real racking of a few centimetres is below one cell; it is shown as a single "
              "one-cell jog in the posts so it reads as a loose frame rather than a stack."])
def small_shelf():
    W, D = 17, 7
    g = Grid(W + 1, D, 26)
    JOG = 13                                                            # posts shift above this
    for x in (0, W - 1):
        for y in (0, D - 1):
            g.box(x, y, 0, x, y, JOG, "bluegrey")
            g.box(x + 1, y, JOG, x + 1, y, 24, "bluegrey")
    for (z, s_) in ((1, 0), (8, 0), (17, 1), (24, 1)):                  # boards
        g.box(s_, 0, z, s_ + W - 1, D - 1, z, "bluegrey")
        g.paint(s_, D - 1, z, s_ + W - 1, D - 1, z, "bluegrey_hi")
    g.box(0, 0, 4, W - 1, 0, 4, "bluegrey_dark")                         # back rails
    g.box(1, 0, 21, W, 0, 21, "bluegrey_dark")
    # chipped paint on the front edges, down to pine
    for (x0, x1, z) in ((5, 7, 8), (12, 13, 17), (3, 5, 24)):
        g.paint(x0, D - 1, z, x1, D - 1, z, "pine_aged")
    g.paint(0, D - 1, 5, 0, D - 1, 7, "pine_aged")
    # bottom: a stoneware crock and a jar of rice
    g.box(2, 1, 2, 5, 4, 5, "porcelain_mid")
    g.box(2, 1, 6, 5, 4, 6, "porcelain_shadow")
    g.paint(2, 1, 4, 5, 4, 4, "teal_dark")                              # glaze band
    g.box(9, 2, 2, 10, 3, 3, "sawdust")
    g.box(9, 2, 4, 10, 3, 4, "glass_hi")
    g.box(9, 2, 5, 10, 3, 5, "steel_light")
    # middle: two plates standing at the back, a short stack in front
    for (x0, y) in ((2, 1), (4, 2)):
        for (i, k) in g.disc_cells(x0 + 2.5, 9 + 2.5, 2.5):
            g.set(i, y, k, "porcelain")
        g.set(x0 + 2, y, 11, "porcelain_mid")
        g.set(x0 + 2, y, 10, "porcelain_mid")
    for (i, j) in g.disc_cells(11.5, 3.5, 2.5):
        g.set(i, j, 9, "porcelain_hi")
    for (i, j) in g.disc_cells(11.5, 3.5, 1.5):
        g.set(i, j, 9, "porcelain_mid")
    # top shelf (above the jog): lidded jars - jam, lentils, pasta
    for (x0, c, lid) in ((4, "red_dark", "label_cream"), (8, "card_dark", "brass_dark"),
                         (12, "sawdust", "steel_light")):
        g.box(x0, 2, 18, x0 + 1, 3, 19, c)
        g.box(x0, 2, 20, x0 + 1, 3, 20, "glass_hi")
        g.box(x0, 2, 21, x0 + 1, 3, 21, lid)
    return {"grid": g, "footprint_cells": ((0, W - 1), (0, D - 1))}
