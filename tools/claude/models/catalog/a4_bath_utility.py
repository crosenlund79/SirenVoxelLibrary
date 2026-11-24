"""Batch A4 - bathroom and utility room (creator: Claude). X right, Y front (+Y), Z up.

Shared with the kitchen family (a3_kitchen): 0.05 m cells, off-white enamel ramps
(porcelain for white ceramic and enamel, almond/cream for the older almond appliances),
chrome / steel fittings and charcoal recesses for value structure. The bathroom joinery is
painted a faded teal (the kitchen is sage) so the rooms differ but sit in one house.
"""
import math

from catalog_registry import model
from voxkit import Grid


def _ell(cx, cy, rx, ry):
    """Cells (i, j) whose centres fall inside an axis-aligned ellipse (cell units)."""
    out = []
    for i in range(int(math.floor(cx - rx)) - 1, int(math.ceil(cx + rx)) + 2):
        for j in range(int(math.floor(cy - ry)) - 1, int(math.ceil(cy + ry)) + 2):
            if ((i + 0.5 - cx) / rx) ** 2 + ((j + 0.5 - cy) / ry) ** 2 <= 1.0:
                out.append((i, j))
    return out


def _edge(cells):
    s = set(cells)
    return [(i, j) for (i, j) in cells
            if any((i + a, j + b) not in s for a in (-1, 0, 1) for b in (-1, 0, 1))]


def _layer(g, cells, z, c):
    for (i, j) in cells:
        g.set(i, j, z, c)


# =========================================================================================
@model("toilet", name="Toilet",
       story="An ordinary close-coupled toilet in a family bathroom, kept clean until the "
             "water stopped. The lid was left up; the last of the water in the bowl dried "
             "down and left a faint brown line where it stood for weeks.",
       details=["Oval bowl on a narrower pedestal, seat down and lid up against the cistern",
                "Cistern with a lid and a chrome dual-flush button",
                "Chrome supply pipe and stop valve at the back left",
                "Low water in the bowl with a faint tide line above it"],
       exclusions=["No brand", "No toilet roll (a separate pickup)"],
       notes=["0.55 x 0.70 x 0.80 m (GPT reference 0.58 x 0.69 x 0.78 m): the cistern is "
              "0.55 m wide, the bowl 0.45 m."])
def toilet():
    g = Grid(12, 15, 17)
    cx = 6.0
    outer = _ell(cx, 8.5, 4.1, 5.6)                               # rim / seat outline
    hole = _ell(cx, 8.8, 2.2, 3.5)                                # seat opening and bowl
    hs = set(hole)
    # pedestal: foot then a narrower waist under the bowl
    _layer(g, _ell(cx, 8.0, 3.0, 4.0), 0, "porcelain_mid")
    for z in (1, 2, 3):
        _layer(g, _ell(cx, 7.5, 2.1, 3.5), z, "porcelain")
    # bowl swelling out to the rim; walls two cells; low water and a faint tide line
    for z, (rx, ry) in zip((4, 5, 6, 7), ((3.5, 4.9), (3.9, 5.3), (4.1, 5.6), (4.1, 5.6))):
        _layer(g, _ell(cx, 8.5, rx, ry), z, "porcelain")
    _layer(g, _edge(outer), 7, "porcelain_hi")                    # glazed rim edge
    for z in (5, 6, 7):
        for (i, j) in hole:
            g.set(i, j, z, 0)
    for (i, j) in hole:
        g.set(i, j, 4, "porcelain_shadow")                        # inside the bowl
    _layer(g, _ell(cx, 9.4, 1.6, 2.3), 4, "water")                # what is left of the water
    for (x, y) in set(outer) - hs:
        if any((x + a, y + b) in hs for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))):
            g.set(x, y, 5, "porcelain_deep")                      # tide line, inner wall
    # seat (down) on the rim: light oak with a darker edge
    _layer(g, [c for c in outer if c not in hs], 8, "pine_light")
    _layer(g, _edge(outer), 8, "pine_mid")
    # rear platform carrying the cistern
    g.box(3, 1, 4, 8, 3, 7, "porcelain")
    # cistern
    g.box(0, 0, 8, 11, 3, 14, "porcelain")
    g.paint(0, 0, 8, 0, 3, 14, "porcelain_mid")                   # side panels a step down
    g.paint(11, 0, 8, 11, 3, 14, "porcelain_mid")
    g.box(0, 0, 15, 11, 3, 15, "porcelain_hi")                    # cistern lid
    g.paint(5, 1, 15, 6, 2, 15, "chrome")                         # dual-flush button
    g.set(5, 2, 15, "steel_light")
    # oak lid up, resting against the cistern; its underside faces the room
    rows = [(2, 9)] * 5 + [(3, 8), (4, 7)]
    for z, (xa, xb) in zip(range(9, 16), rows):
        g.box(xa, 4, z, xb, 4, z, "pine_light")
        g.set(xa, 4, z, "pine_mid")
        g.set(xb, 4, z, "pine_mid")
    g.paint(4, 4, 15, 7, 4, 15, "pine_mid")
    g.box(3, 4, 8, 3, 4, 8, "chrome")                             # hinges
    g.box(8, 4, 8, 8, 4, 8, "chrome")
    # supply pipe and stop valve behind, at the left
    g.box(1, 0, 2, 1, 0, 7, "chrome")
    g.box(1, 1, 3, 1, 1, 3, "steel_light")
    g.set(1, 0, 3, "steel")
    return {"grid": g, "footprint_cells": ((0, 11), (0, 14))}


# =========================================================================================
@model("bathtub", name="Bathtub",
       story="When the mains failed, the family filled the bath while the pressure lasted and "
             "used it as their water tank. A plank laid across the far end holds the saucepan "
             "they dipped with; the level has dropped well below the grey line where it "
             "first stood.",
       details=["Built-in enamel tub with a tiled-in front panel and a recessed plinth",
                "Sloped back at the head end, flat end under the taps",
                "Deck-mounted chrome mixer with two cross-head taps and an overflow plate",
                "Stored water (opaque) with a scum line well above the current level",
                "Pine plank across the tub carrying a steel saucepan used as a dipper"],
       exclusions=["No bath toys or shower curtain", "No transparency"],
       front_note="+Y is the open front panel; the back and both ends go against walls.",
       notes=["1.75 x 0.75 x 0.65 m with the taps (rim 0.60 m; GPT reference 1.75 x 0.75 x "
              "0.58 m)."])
def bathtub():
    L, D = 35, 15
    g = Grid(L, D, 14)
    RIM = 11
    g.box(0, 0, 1, L - 1, D - 1, RIM, "porcelain")                 # tub body + panel
    g.box(0, 0, 0, L - 1, D - 3, 0, "porcelain_shadow")           # plinth, recessed
    g.paint(0, D - 3, 0, L - 1, D - 3, 0, "charcoal")
    # front panel: painted teal tongue-and-groove boarding (matches the vanity)
    g.paint(0, D - 1, 1, L - 1, D - 1, RIM - 1, "teal_hi")
    g.paint(0, D - 1, RIM - 1, L - 1, D - 1, RIM - 1, "teal")     # top rail
    g.paint(0, D - 1, 1, L - 1, D - 1, 1, "teal")                 # bottom rail
    g.paint(0, D - 2, 1, L - 1, D - 2, RIM - 1, "teal_dark")
    for x in range(3, L - 1, 4):
        g.paint(x, D - 1, 2, x, D - 1, RIM - 2, "teal")           # V-grooves between boards
    g.paint(0, D - 1, 1, 3, D - 1, 1, "teal_dark")                # scuffed by feet
    g.paint(0, 0, 1, 0, D - 3, RIM - 1, "porcelain_mid")           # end faces (walls)
    g.paint(L - 1, 0, 1, L - 1, D - 3, RIM - 1, "porcelain_mid")
    g.paint(0, 0, RIM, L - 1, D - 1, RIM, "porcelain_hi")         # rim / deck
    # interior: rounded plan, flat foot end (x small, under the taps), sloped head end
    x0, x1, y0, y1 = 3, L - 3, 2, D - 3
    for z in range(3, RIM + 1):
        head = x1 - max(0, (z - 3) // 2 - 1)                      # slope widens upward
        g.clear(x0, y0, z, head, y1, z)
        for (x, y) in [(x0, y0), (x0, y1), (head, y0), (head, y1)]:
            g.set(x, y, z, "porcelain")                           # soft inside corners
    # stored water, its old scum line, a grey tide well above the current level
    WZ = 6
    g.box(x0, y0, 3, x1, y1, WZ, "water")
    for (x, y) in [(x0, y0), (x0, y1), (x1, y0), (x1, y1)]:
        g.box(x, y, 3, x, y, WZ, "porcelain")
    g.paint(x0, y0, WZ, x1, y1, WZ, "water_hi")
    g.paint(x0 + 1, y0 + 1, WZ, x1 - 1, y1 - 1, WZ, "water")
    for z, col in ((WZ + 3, "porcelain_shadow"), (WZ + 1, "porcelain_mid")):
        for x in range(x0 - 1, x1 + 2):
            for y in range(y0 - 1, y1 + 2):
                if g.get(x, y, z) and any(
                        x0 <= x + a <= x1 and y0 <= y + b <= y1 and not g.get(x + a, y + b, z)
                        for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                    g.set(x, y, z, col)
    # taps on the deck at the foot (-X) end, overflow plate below
    g.box(1, 7, RIM + 1, 1, 7, RIM + 2, "chrome")                 # spout column
    g.box(2, 7, RIM + 2, 3, 7, RIM + 2, "chrome")                 # spout over the water
    g.set(3, 7, RIM + 1, "steel_light")
    for y in (4, 10):
        g.set(1, y, RIM + 1, "chrome")
        g.box(1, y - 1, RIM + 2, 1, y + 1, RIM + 2, "steel_light")
        g.box(0, y, RIM + 2, 2, y, RIM + 2, "steel_light")
        g.set(1, y, RIM + 2, "chrome")
    g.set(x0 - 1, 7, 9, "chrome")                                 # overflow plate
    g.set(x0 - 1, 7, 8, "steel_light")
    # plank across the head end, saucepan dipper on it
    g.box(L - 9, 0, RIM + 1, L - 7, D - 1, RIM + 1, "pine_mid")
    g.paint(L - 9, 0, RIM + 1, L - 9, D - 1, RIM + 1, "pine_light")
    g.paint(L - 9, D - 1, RIM + 1, L - 7, D - 1, RIM + 1, "pine_aged")
    g.box(L - 9, 5, RIM + 2, L - 7, 7, RIM + 3, "steel_light")    # saucepan (16 cm)
    g.set(L - 8, 6, RIM + 3, 0)                                   # its open top
    g.set(L - 8, 6, RIM + 2, "steel_dark")
    g.box(L - 8, 8, RIM + 3, L - 8, 10, RIM + 3, "charcoal")      # handle toward the room
    return g


# =========================================================================================
@model("bathroom_sink", name="Bathroom Vanity",
       story="A teal-painted vanity from the family bathroom, past its best before anything "
             "happened: the top hinge of the right door pulled out of the damp chipboard and "
             "the door hangs open on the bottom one. A toothbrush is still in its cup, and the "
             "tap has left a brown drip stain down to the plug.",
       details=["Ceramic one-piece top with an oval basin, plug and a brown drip stain",
                "Chrome mixer tap with a lever", "Toothbrush in a glass cup on the back corner",
                "Teal shaker doors with brass knobs; the right door hangs open and sags",
                "Inside: chrome U-bend, a toilet roll and a bleach bottle on its side",
                "Paint chipped to bare wood along the bottom rail"],
       exclusions=["No mirror (see Claude_medicine_cabinet)", "No brand on the bottle"],
       notes=["Closed body 0.60 x 0.55 x 0.85 m (GPT reference 0.62 x 0.52 x 0.83 m); the "
              "hanging door adds 0.30 m of depth at the right end, the tap and cup reach "
              "0.95 m."])
def bathroom_sink():
    W = 12
    g = Grid(W + 2, 16, 20)
    TOP = 16
    YP, YF = 9, 10                                                # door panel / frame planes
    g.box(0, 0, 0, W - 1, YP - 1, TOP - 1, "teal")                # carcass
    g.paint(0, YP - 1, 0, W - 1, YP - 1, 1, "teal_deep")          # toe kick face
    g.clear(0, YP - 1, 0, W - 1, YP - 1, 1)
    g.paint(0, YP - 2, 0, W - 1, YP - 2, 1, "teal_deep")
    g.clear(1, 1, 2, W - 2, YP - 1, TOP - 2)                      # cupboard interior
    g.paint(1, 1, 1, W - 2, YP - 1, 1, "teal_dark")               # its floor
    g.box(1, 0, 2, W - 2, 0, TOP - 2, "teal_dark")                # back panel
    # left door, closed: shaker, brass knob near the meeting edge
    g.box(0, YP, 2, 5, YP, TOP - 2, "teal")
    g.box(0, YF, 2, 5, YF, TOP - 2, "teal")
    g.clear(1, YF, 3, 4, YF, TOP - 3)
    g.set(5, YF + 1, TOP - 4, "brass")
    g.paint(0, YF, 2, 5, YF, 2, "teal_dark")                      # bottom rail scuffed
    g.paint(1, YF, 2, 2, YF, 2, "teal_deep")
    g.paint(4, YF, TOP - 5, 5, YF, TOP - 3, "teal_hi")            # hand-worn by the knob
    # right door hanging open on its bottom hinge: leaf along +Y beyond the right side,
    # the free end has dropped a cell
    for y in range(YP, YP + 6):
        drop = 1 if y >= YP + 3 else 0
        g.box(W - 1, y, 2 - drop, W - 1, y, TOP - 2 - drop, "teal_hi")   # inner face
        g.box(W, y, 2 - drop, W, y, TOP - 2 - drop, "teal")              # outer frame
    g.clear(W, YP + 1, 3, W, YP + 4, TOP - 4)
    g.box(W - 1, YP - 1, 2, W - 1, YP - 1, 3, "brass_dark")       # surviving hinge
    g.box(W - 1, YP - 1, TOP - 3, W - 1, YP - 1, TOP - 3, "pine_mid")  # torn-out screw hole
    g.set(W + 1, YP + 5, TOP - 5, "brass")                        # its knob, outside face
    # inside the cupboard: U-bend, toilet roll, bleach bottle on its side
    g.box(6, 4, 9, 6, 4, TOP - 3, "chrome")                       # tail pipe
    g.box(6, 4, 8, 6, 2, 8, "steel_light")                        # trap
    g.box(6, 1, 8, 6, 1, 11, "steel_light")                       # to the wall
    g.box(8, 5, 2, 9, 6, 3, "paper")                              # toilet roll
    g.set(8, 5, 3, "card")
    g.box(6, 6, 2, 9, 7, 3, 0)
    g.box(7, 7, 2, 10, 7, 3, "porcelain_hi")                      # bleach bottle lying
    g.paint(8, 7, 2, 9, 7, 3, "label_blue")
    g.set(6, 7, 3, "label_blue")                                  # cap
    # ceramic top with an oval basin
    g.box(0, 0, TOP, W - 1, YF, TOP, "porcelain_hi")
    g.box(2, 2, TOP - 3, W - 3, 8, TOP - 1, "porcelain")           # basin body under the top
    for (i, j) in _ell(6.0, 5.0, 3.1, 2.6):
        g.box(i, j, TOP - 2, i, j, TOP, 0)
        g.set(i, j, TOP - 3, "porcelain_mid")
    for (i, j) in _edge(_ell(6.0, 5.0, 3.1, 2.6)):
        g.set(i, j, TOP - 3, "porcelain_mid")
    g.set(6, 5, TOP - 3, "black")                                 # plug hole
    g.set(5, 5, TOP - 3, "black")
    for (x, y, z) in [(5, 3, TOP - 3), (6, 3, TOP - 3), (6, 4, TOP - 3), (5, 2, TOP - 2),
                      (6, 2, TOP - 2)]:
        g.paint_cell(x, y, z, "card_dark")                        # drip stain to the plug
    # tap at the back, toothbrush cup on the back-right corner
    g.box(5, 1, TOP + 1, 6, 1, TOP + 2, "chrome")
    g.box(5, 2, TOP + 2, 6, 2, TOP + 2, "chrome")                 # spout
    g.box(5, 1, TOP + 3, 6, 1, TOP + 3, "steel_light")            # lever
    g.paint(4, 1, TOP, 7, 1, TOP, "porcelain_mid")                # tap base
    g.set(4, 1, TOP, "rust_deep")
    g.box(W - 2, 1, TOP + 1, W - 2, 1, TOP + 2, "glass_hi")       # cup
    g.box(W - 2, 1, TOP + 3, W - 2, 1, TOP + 3, "label_blue")     # toothbrush
    return {"grid": g, "footprint_cells": ((0, W - 1), (0, YF))}


# =========================================================================================
@model("medicine_cabinet", name="Mirrored Medicine Cabinet",
       story="The bathroom cabinet was the first thing searched. Someone swept the shelves "
             "into a bag and left the right door hanging open; only an amber pill bottle and "
             "a plastic bottle that rolled to the back were left. Damp has started to lift "
             "the mirror silver along its bottom edge.",
       details=["Painted steel cabinet with two mirror doors; the left door is closed",
                "Right door swung open 90 degrees, its painted back toward the shelves",
                "Two glass shelves, one amber pill bottle standing, one white bottle on its "
                "side", "Mirror silver lifting along the bottom edge; rust starting on the "
                "bottom front lip"],
       exclusions=["No reflections painted as pictures", "No readable labels"],
       mount={"type": "wall", "recommended_bottom_height_m": 1.2},
       pivot_note="Bottom centre of the back face (the cabinet body, not the open door). Hang "
                  "with the back on the wall; bottom at about 1.20 m (over a 0.85 m vanity).",
       front_note="+Y faces into the room; the back (y = 0) is flat for the wall.",
       collision_hint="Box 0.65 x 0.20 x 0.75 m for the body; the open door adds a 0.05 x "
                      "0.30 m leaf at the right end.",
       notes=["Closed body 0.65 x 0.20 x 0.75 m (GPT reference 0.65 x 0.22 x 0.74 m); the "
              "open right door adds 0.30 m of depth."])
def medicine_cabinet():
    W, H = 13, 15
    g = Grid(W + 1, 11, H)
    g.box(0, 0, 0, W - 1, 2, H - 1, "paint_white")                # steel box
    g.clear(1, 1, 1, W - 2, 2, H - 2)
    g.box(1, 0, 1, W - 2, 0, H - 2, "paint_white_shadow")         # back inside
    for z in (5, 10):
        g.box(1, 1, z, W - 2, 2, z, "glass_hi")                   # glass shelves
        g.paint(1, 2, z, W - 2, 2, z, "glass")
    g.paint(0, 2, 0, W - 1, 2, 0, "paint_white_shadow")           # bottom lip
    for (x, z) in [(2, 0), (3, 0)]:
        g.paint_cell(x, 2, z, "rust_deep")                        # rust starting on the lip
    # left mirror door, closed (frame + mirror)
    g.box(0, 3, 0, 6, 3, H - 1, "paint_white")
    g.box(1, 3, 1, 5, 3, H - 2, "mirror")
    for (x, z) in [(1, 1), (2, 1), (1, 2), (4, 1), (5, 1)]:
        g.set(x, 3, z, "glass_hi")                                # silver lifting, damp edge
    g.set(6, 4, 6, "chrome")                                      # finger pull
    # right door open on its right-hand hinge
    g.box(W - 1, 3, 0, W - 1, 8, H - 1, "paint_white_shadow")     # painted back of door
    g.box(W, 3, 1, W, 8, H - 2, "mirror")                         # mirror face, outward
    g.box(W, 3, 0, W, 8, 0, "paint_white")
    g.box(W, 3, H - 1, W, 8, H - 1, "paint_white")
    g.box(W - 1, 8, 1, W - 1, 8, H - 2, "mirror")                 # mirror edge at the free end
    # what was left: an amber pill bottle and a white bottle on its side
    g.box(9, 1, 6, 9, 1, 7, "ochre")
    g.set(9, 1, 8, "porcelain_hi")                                # child-proof cap
    g.box(8, 2, 1, 10, 2, 1, "porcelain_hi")
    g.set(9, 2, 1, "label_red")
    g.set(11, 2, 1, "steel_light")                                # its cap
    g.box(3, 1, 11, 4, 1, 11, "paint_white_shadow")               # a clean patch on the shelf
    return {"grid": g, "pivot_cells": (W / 2, 0, 0)}               # bottom centre of the back


# =========================================================================================
@model("washing_machine", name="Washing Machine",
       story="A white front-loader in the utility room, only a few years old and still "
             "clean. The last load was pulled out in a hurry; one mustard sock stayed caught "
             "in the door seal and hangs down the front (its partner is in the laundry "
             "basket).",
       details=["Round porthole door: grey ring, dark recessed glass, handle on the right",
                "Detergent drawer, small display and program dial on the control strip",
                "Separate top panel seam, plinth with a filter hatch",
                "Mustard sock caught in the seal at the bottom of the door"],
       exclusions=["No brand or readable controls", "No water or suds behind the glass"],
       pairs_with=["Claude_laundry_basket", "Claude_clothes_dryer"],
       notes=["0.65 x 0.70 x 0.85 m with the door ring (GPT reference 0.64 x 0.64 x 0.86 m)."])
def washing_machine():
    W = 13
    g = Grid(W, 15, 17)
    FY = 11                                                       # front face
    g.box(0, 0, 0, W - 1, FY, 16, "porcelain")
    g.paint(0, FY, 0, W - 1, FY, 16, "porcelain_hi")              # front panel
    g.paint(0, 0, 16, W - 1, FY, 16, "porcelain_hi")              # top panel
    g.paint(0, 0, 15, 0, FY - 1, 15, "porcelain_mid")             # top panel seam
    g.paint(W - 1, 0, 15, W - 1, FY - 1, 15, "porcelain_mid")
    g.paint(0, FY - 1, 0, 0, FY - 1, 14, "porcelain_mid")         # front panel seam
    g.paint(W - 1, FY - 1, 0, W - 1, FY - 1, 14, "porcelain_mid")
    # plinth with a filter hatch
    g.paint(0, FY, 0, W - 1, FY, 1, "porcelain")
    g.paint(0, FY, 0, W - 1, FY, 0, "porcelain_mid")
    g.paint(9, FY, 0, 11, FY, 1, "porcelain_mid")
    g.paint(9, FY, 1, 11, FY, 1, "porcelain_shadow")
    # control strip: drawer, display, dial
    g.paint(0, FY, 13, W - 1, FY, 15, "porcelain")
    g.box(1, FY + 1, 13, 4, FY + 1, 14, "porcelain_hi")           # detergent drawer
    g.paint(4, FY + 1, 13, 4, FY + 1, 13, "porcelain_shadow")     # finger recess
    g.paint(6, FY, 14, 7, FY, 14, "screen")
    g.box(9, FY + 1, 13, 10, FY + 1, 14, "steel_light")           # program dial
    g.set(10, FY + 1, 14, "charcoal")
    # porthole door: a 45 cm ring proud of the front, dark glass recessed behind it
    cx, cz = 6.5, 7.5
    glass = [(i, k) for i in range(3, 10) for k in range(4, 11)
             if (i, k) not in {(3, 4), (9, 4), (3, 10), (9, 10)}]  # rounded 35 cm window
    for (i, k) in g.disc_cells(cx, cz, 4.5):
        g.set(i, FY + 1, k, "steel_light")
    for (i, k) in glass:
        g.set(i, FY + 1, k, 0)
        g.set(i, FY, k, "glass_deep")
    g.box(4, FY, 10, 8, FY, 10, "glass_dark")                     # sheen along the top
    g.box(3, FY, 9, 3, FY, 9, "glass_dark")
    g.box(11, FY + 1, 7, 11, FY + 1, 8, "porcelain_mid")          # door handle
    # the sock: tucked under the ring at the bottom-left, hanging to the floor
    for z in (3, 2, 1):
        g.set(3, FY + 1, z, "mustard")
    g.box(2, FY + 1, 0, 3, FY + 1, 0, "mustard_dark")             # toe turned out
    g.set(3, FY + 1, 3, "mustard_dark")                           # cuff in the seal
    return {"grid": g, "footprint_cells": ((0, W - 1), (0, FY))}


# =========================================================================================
@model("clothes_dryer", name="Almond Tumble Dryer",
       story="An old almond tumble dryer, much older than the washer beside it. It was "
             "dented when it was dragged in through the back door, the lint was never "
             "cleaned out properly, and the foil vent hose still trails out of the back "
             "where it was meant to go to the window.",
       details=["Big flat almond door with a recessed pull, no glass (unlike the washer)",
                "Backsplash console with a timer dial and a heat knob",
                "Lint filter pulled up on the top, grey fluff caught at the door's lower "
                "seam and on the floor", "Dent in the left side panel",
                "Ribbed foil vent hose from the back, sagging to the floor"],
       exclusions=["No brand", "No readable dial markings"],
       pairs_with=["Claude_washing_machine"],
       notes=["0.65 x 0.80 x 0.85 m with the vent hose (GPT reference 0.64 x 0.64 x 0.85 m); "
              "the body is 0.65 x 0.65 m."])
def clothes_dryer():
    W, B = 13, 3                                                  # B: room behind for the hose
    g = Grid(W + 2, 17, 17)
    FY = B + 11
    g.box(0, B, 1, W - 1, FY, 14, "almond")
    g.paint(0, B, 1, 0, FY, 14, "cream_mid")                      # side panels
    g.paint(W - 1, B, 1, W - 1, FY, 14, "cream_mid")
    g.paint(0, B, 14, W - 1, FY, 14, "cream")                     # top
    for (x, y) in [(0, B), (W - 1, B), (0, FY), (W - 1, FY)]:
        g.set(x, y, 0, "charcoal")                                # feet
    g.box(1, B + 1, 0, W - 2, FY - 1, 0, "charcoal")
    g.paint(0, FY, 1, W - 1, FY, 2, "almond_dark")                # kick panel
    # backsplash console with dials
    g.box(0, B, 15, W - 1, B + 2, 16, "almond")
    g.paint(0, B + 2, 15, W - 1, B + 2, 16, "cream_mid")
    g.paint(0, B, 16, W - 1, B + 2, 16, "cream")
    g.box(8, B + 3, 15, 10, B + 3, 16, "cream_hi")                # timer dial
    g.set(9, B + 4, 16, "charcoal")                               # its pointer
    g.box(2, B + 3, 15, 3, B + 3, 15, "iron_edge")                # heat knob
    # big flat door with cut corners and a recessed pull along its top
    g.box(1, FY + 1, 3, W - 2, FY + 1, 12, "almond")
    for (x, z) in [(1, 3), (W - 2, 3), (1, 12), (W - 2, 12)]:
        g.set(x, FY + 1, z, 0)
    g.paint(1, FY + 1, 3, W - 2, FY + 1, 3, "almond_dark")        # lower edge in shade
    g.box(4, FY + 1, 11, 8, FY + 1, 11, 0)                        # pull recess
    g.paint(4, FY, 11, 8, FY, 11, "almond_dark")
    g.paint(2, FY + 1, 6, 2, FY + 1, 9, "cream")                  # hinge-side highlight edge
    # lint: caught in the lower seam, a drift on the floor, the filter pulled up on top
    for (x, z) in [(3, 2), (4, 2), (5, 2), (7, 2), (4, 1)]:
        g.set(x, FY + 1, z, "ash_light")
    g.box(3, FY + 2, 0, 5, FY + 2, 0, "ash_light")
    g.set(4, FY + 1, 0, "ash")
    g.box(3, FY - 1, 14, 8, FY - 1, 14, "charcoal")               # empty lint-screen slot
    g.box(2, FY - 5, 15, 7, FY - 3, 15, "steel_light")            # screen left lying on top
    g.box(3, FY - 4, 15, 6, FY - 4, 15, "ash")                    # grey lint on it
    # dent in the left side panel (camera side)
    for (y, z) in [(B + 5, 7), (B + 6, 7), (B + 6, 8), (B + 7, 8), (B + 5, 8), (B + 6, 6),
                   (B + 7, 7)]:
        g.set(0, y, z, 0)
        g.set(1, y, z, "almond_dark")
    g.paint(0, B + 4, 7, 0, B + 4, 8, "cream_shadow")
    # foil vent hose out of the back, sagging to the floor and trailing right
    path = [(10, B - 1, 6), (10, B - 2, 5), (10, B - 2, 4), (10, B - 3, 3), (10, B - 3, 2),
            (11, B - 3, 1), (12, B - 3, 1), (13, B - 3, 1)]
    for n, (x, y, z) in enumerate(path):
        col = "foil" if n % 2 == 0 else "galv_dark"
        g.box(x, y, z, x + 1, y, z + 1, col) if y < B - 2 or z > 2 else None
        g.box(x, y, z - 1 if z > 0 else 0, x + 1, y + 1 if y < B - 1 else y, z, col)
    g.box(10, B - 1, 6, 11, B - 1, 7, "galv")                     # collar on the back
    return {"grid": g, "footprint_cells": ((0, W - 1), (B, FY))}


# =========================================================================================
@model("water_heater", name="Gas Water Heater",
       story="The tank water heater in the utility corner. After the gas went off it became "
             "the house's emergency water: someone has been drawing off the drain valve into "
             "buckets, and the valve's slow drip has left a rust streak down the jacket.",
       details=["60 cm cylindrical jacket with a top cap and a base ring",
                "Copper cold-in and hot-out pipes with brass valves, turning back to the wall",
                "Galvanised flue with a draft hood in the middle of the top",
                "Relief valve near the top with its copper discharge pipe down the side",
                "Drain valve at the bottom with a rust streak below it",
                "Gas control with a red knob, burner access cover, plain data plate"],
       exclusions=["No readable data plate", "No brand"],
       notes=["0.65 x 0.70 x 1.60 m with the valves and pipes (GPT reference 0.61 x 0.61 x "
              "1.60 m); the tank itself is 0.60 m across."])
def water_heater():
    g = Grid(14, 16, 32)
    cx, cy = 7.0, 7.0                                             # tank x 1-12, y 1-12
    disc = g.disc_cells(cx, cy, 6.0)
    for (i, j) in g.disc_cells(cx, cy, 5.5):
        g.box(i, j, 0, i, j, 1, "steel_dark")                     # base ring
    for (i, j) in disc:
        g.box(i, j, 2, i, j, 26, "paint_white")                   # jacket
        g.set(i, j, 2, "paint_white_shadow")
        g.set(i, j, 27, "steel_light")                            # top cap band
    for (i, j) in g.disc_cells(cx, cy, 5.0):
        g.set(i, j, 28, "steel_light")                            # domed top
    for (i, j) in g.disc_cells(cx, cy, 4.0):
        g.set(i, j, 28, "steel_hi")
    for z in range(3, 27):                                        # vertical seam at the back
        g.paint_cell(7, 1, z, "paint_white_shadow")
    # flue and draft hood
    g.box(5, 5, 29, 8, 8, 29, "galv")
    g.box(6, 6, 30, 7, 7, 31, "galv_hi")
    g.paint(5, 5, 29, 8, 5, 29, "galv_dark")
    # copper pipes in and out, rising then turning back toward the wall
    for x, valve in ((3, "brass"), (11, "brass")):
        g.box(x, 7, 29, x, 7, 30, "copper")
        g.box(x, 0, 31, x, 7, 31, "copper")
        g.set(x, 7, 30, valve)
    g.box(3, 7, 31, 3, 8, 31, "copper")
    g.box(2, 8, 31, 4, 8, 31, "signal_red_dark")                  # cold-in valve lever
    # relief valve near the top on the camera side, discharge pipe down the side
    g.box(0, 7, 23, 0, 8, 24, "brass")
    g.box(0, 8, 3, 0, 8, 22, "copper")
    g.set(0, 8, 2, "copper")
    # data plate (plain, unreadable)
    g.box(5, 12, 17, 8, 12, 19, "label_cream")
    g.paint(5, 12, 18, 8, 12, 18, "cream_shadow")
    g.paint(5, 12, 17, 5, 12, 17, "cream_deep")
    # gas control and burner access at the bottom front
    g.box(6, 13, 7, 8, 13, 8, "charcoal")
    g.set(8, 14, 8, "signal_red_dark")                            # gas knob
    g.set(6, 14, 7, "steel_light")                                # pilot button
    g.box(5, 12, 2, 8, 12, 4, "steel_dark")                       # burner access cover
    g.paint(6, 12, 3, 7, 12, 3, "charcoal")
    g.box(7, 13, 7, 7, 13, 5, "steel_light")                      # gas line to the burner
    # drain valve at the bottom left of the front, with a rust streak below
    g.box(3, 11, 4, 3, 13, 4, "brass")
    g.set(3, 13, 3, "brass_dark")
    for (x, y, z) in [(3, 11, 3), (3, 11, 2), (3, 11, 1), (3, 11, 0), (4, 12, 2), (3, 10, 1),
                      (4, 11, 1)]:
        g.paint_cell(x, y, z, "rust_dark")
    for (x, y, z) in [(3, 11, 2), (3, 11, 0)]:
        g.paint_cell(x, y, z, "rust")
    for (x, y, z) in [(2, 10, 0), (4, 11, 0), (5, 11, 0)]:
        g.paint_cell(x, y, z, "rust_deep")
    return {"grid": g, "footprint_cells": ((1, 12), (1, 12))}


# =========================================================================================
@model("laundry_basket", name="Laundry Basket",
       story="The family's laundry basket, still holding the last unwashed load: jeans, a "
             "towel, a mauve shirt with one sleeve flopped over the rim, and the other mustard "
             "sock from the pair caught in the washer.",
       details=["Pale blue perforated plastic basket, slightly tapered, with hand-hole grips",
                "Clothes heaped over the rim in a few large garment masses",
                "One sleeve hanging over the front rim; the stray mustard sock on top"],
       exclusions=["No pattern prints on the clothes"],
       pairs_with=["Claude_washing_machine"],
       notes=["0.55 x 0.50 x 0.50 m with the sleeve (GPT reference 0.57 x 0.43 x 0.49 m); "
              "the basket body is 0.55 x 0.45 x 0.40 m."])
def laundry_basket():
    W, D = 11, 9
    g = Grid(W, D + 1, 10)
    # clothes inside first (they show through the perforations), then the basket around them
    g.box(1, 1, 1, 4, D - 2, 7, "denim_dark")                     # jeans at the left
    g.box(5, 1, 1, 6, D - 2, 7, "mauve_dark")                     # shirt in the middle
    g.box(7, 1, 1, W - 2, D - 2, 7, "cream_shadow")               # towel at the right
    # basket: inset foot, straight walls with softened corners, a darker rim band
    g.box(1, 1, 0, W - 2, D - 2, 0, "bottle")
    for z in range(1, 8):
        for (x0, y0, x1, y1) in ((0, 0, W - 1, 0), (0, D - 1, W - 1, D - 1),
                                 (0, 0, 0, D - 1), (W - 1, 0, W - 1, D - 1)):
            g.box(x0, y0, z, x1, y1, z, "bottle_hi")
    g.paint(0, 0, 7, W - 1, D - 1, 7, "bottle")                   # rim
    for (x, y) in ((0, 0), (W - 1, 0), (0, D - 1), (W - 1, D - 1)):
        g.box(x, y, 0, x, y, 7, 0)                                # rounded corners
    # perforations: staggered rows of horizontal slots (brick pattern)
    for (z, xs) in ((2, [(1, 2), (4, 6), (8, 9)]), (4, [(2, 4), (6, 8)])):
        for (xa, xb) in xs:
            g.box(xa, 0, z, xb, 0, z, 0)
            g.box(xa, D - 1, z, xb, D - 1, z, 0)
    for (z, ys) in ((2, [(2, 3), (5, 6)]), (4, [(3, 5)])):
        for (ya, yb) in ys:
            g.box(0, ya, z, 0, yb, z, 0)
            g.box(W - 1, ya, z, W - 1, yb, z, 0)
    for x in (0, W - 1):                                          # hand-holes under the rim
        g.box(x, 3, 6, x, 5, 6, 0)
    # the heap, just over the rim: three garment masses
    g.box(1, 1, 8, 4, 7, 8, "denim")                              # jeans, a leg folded over
    g.box(1, 2, 9, 2, 6, 9, "denim")
    g.set(3, 3, 9, "denim")
    g.paint(1, 1, 8, 4, 1, 8, "denim_dark")
    g.paint(1, 2, 9, 1, 6, 9, "denim_dark")
    for (x, y) in ((1, 1), (4, 7), (1, 7)):
        g.set(x, y, 8, 0)
    g.box(7, 1, 8, 9, 6, 8, "cream")                              # towel, loosely folded
    g.box(7, 2, 9, 8, 3, 9, "cream_hi")
    g.set(8, 4, 9, "cream_hi")
    g.paint(9, 1, 8, 9, 6, 8, "cream_mid")
    for (x, y) in ((9, 1), (9, 6), (7, 6)):
        g.set(x, y, 8, 0)
    g.box(5, 2, 8, 6, 7, 8, "mauve")                              # shirt
    g.box(5, 3, 9, 5, 5, 9, "mauve_hi")
    g.box(3, 7, 8, 4, 8, 8, "mauve")                              # sleeve over the rim...
    g.box(3, D, 4, 4, D, 8, "mauve")                              # ...and down the front
    g.paint(3, D, 4, 4, D, 4, "mauve_dark")                       # cuff
    g.paint(4, D, 5, 4, D, 7, "mauve_dark")                       # a fold
    g.box(7, 5, 9, 8, 5, 9, "mustard")                            # the other sock
    return {"grid": g, "footprint_cells": ((0, W - 1), (0, D - 1))}
