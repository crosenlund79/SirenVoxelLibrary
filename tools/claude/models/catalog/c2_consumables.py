"""Batch C2 - consumables: food, water, storage and medical supplies (creator: Claude).

X right, Y front (+Y), Z up; inclusive cells. Pickups are generic and unbranded: labels are
plain colour bands, never text. Round items use clean pixel circles (8 cells: rows 4-6-8-8-8-8-
6-4, 7 cells: 3-5-7-7-7-5-3, 6 cells: 4-6-6-6-6-4) so cans and bottles never read as plus signs.
"""
import math

from catalog_registry import model
from voxkit import Grid, P


# ---------------------------------------------------------------------------
# local helpers
# ---------------------------------------------------------------------------
def disc(g, cx, cy, r):
    """Cells of a clean pixel circle (centre in cell units)."""
    return g.disc_cells(cx, cy, r)


def angle_of(i, j, cx, cy):
    """Angle of a cell centre around (cx, cy); 0 = +X, 90 = +Y (degrees, -180..180)."""
    return math.degrees(math.atan2(j + 0.5 - cy, i + 0.5 - cx))


def rim(g, cx, cy, r, z, c, ox=0, oy=0):
    """Paint the thin outline of a disc (cells with an edge-neighbour outside it) - used to
    draw a rolled seam on a flat lid; occupied cells only."""
    d = set(g.disc_cells(cx, cy, r))
    for (i, j) in d:
        if any((i + a, j + b) not in d for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))):
            g.paint_cell(ox + i, oy + j, z, c)


def can_body(g, ox, oy, cx, cy, r, z0, z1, c):
    for (i, j) in disc(g, cx, cy, r):
        g.box(ox + i, oy + j, z0, ox + i, oy + j, z1, c)


def paint_ring_band(g, ox, oy, cx, cy, r, z0, z1, c, ang=None):
    """Recolour the outer ring of a cylinder between z0..z1 (optionally only cells whose
    angle lies inside ang=(a0, a1) degrees)."""
    for (i, j) in g.ring_cells(cx, cy, r):
        if ang is not None:
            a = angle_of(i, j, cx, cy)
            if not (ang[0] <= a <= ang[1]):
                continue
        for z in range(z0, z1 + 1):
            g.paint_cell(ox + i, oy + j, z, c)


# ---------------------------------------------------------------------------
# canned food
# ---------------------------------------------------------------------------
@model("canned_food", name="Canned Food",
       story="A tall tin of vegetables from the back of a pantry shelf, still sealed. It was "
             "knocked off the shelf at some point: one small dent creases the label near the base.",
       details=["Clean 8-cell round tin with rolled top and bottom seams",
                "Flat lid with a bright rolled seam", "Muted green paper label with a cream band",
                "Two rib lines pressed through the label", "One small dent near the base"],
       exclusions=["No text, brand or picture on the label", "No ring-pull (see soup_can)"],
       notes=["Tall food tin with a muted paper label (simple colour blocks, no text), ribbed "
              "side, one small dent."])
def canned_food():
    g = Grid(8, 8, 11)
    c = (4.0, 4.0, 4.0)                                  # centre on a cell corner -> 8 cells
    can_body(g, 0, 0, c[0], c[1], c[2], 0, 10, "label_green")
    g.paint(0, 0, 0, 7, 7, 0, "steel_dark")              # bottom seam
    g.paint(0, 0, 1, 7, 7, 1, "steel")                   # bare metal below the label
    g.paint(0, 0, 9, 7, 7, 9, "steel")                   # and above it
    g.paint(0, 0, 4, 7, 7, 6, "label_cream")             # cream band
    g.paint(0, 0, 3, 7, 7, 3, "leaf_mid")                # ribs pressed through the label
    g.paint(0, 0, 7, 7, 7, 7, "leaf_mid")
    # flat lid: rolled seam outline, lighter pressed centre
    g.paint(0, 0, 10, 7, 7, 10, "galv")
    rim(g, 4.0, 4.0, 4.0, 10, "steel_light")
    # small dent on the front-left (camera) side near the base, label creased darker
    g.set(1, 6, 2, 0)
    g.set(1, 6, 3, 0)
    for (x, y, z) in [(2, 6, 2), (2, 6, 3), (1, 5, 2), (1, 5, 3)]:
        g.paint_cell(x, y, z, "leaf_dark")
    return g


# ---------------------------------------------------------------------------
# soup can
# ---------------------------------------------------------------------------
@model("soup_can", name="Soup Can",
       story="A squat can of soup with an easy-open lid, the kind kept for power cuts. It "
             "is unopened; the ring-pull still lies flat against the lid.",
       details=["Squat 7-cell round can, clearly shorter and wider-looking than canned_food",
                "Cream label with one broad muted red band",
                "Ring-pull lid: rolled seam and a flat pull ring around its rivet"],
       exclusions=["No text, brand or picture on the label"],
       notes=["Squat soup can with a red-and-cream label band and a ring-pull lid - reads "
              "differently from canned_food.",
              "Made squat (8.75 x 10 cm) as the brief asks, rather than GPT's 13 cm height."])
def soup_can():
    g = Grid(7, 7, 8)
    cx = cy = 3.5                                        # centre on a cell centre -> 7 cells
    can_body(g, 0, 0, cx, cy, 3.2, 0, 7, "label_cream")
    g.paint(0, 0, 0, 6, 6, 0, "steel_dark")
    g.paint(0, 0, 6, 6, 6, 6, "steel")
    g.paint(0, 0, 2, 6, 6, 4, "label_red")               # broad red band
    g.paint(0, 0, 1, 6, 6, 1, "label_cream")
    # flat lid: rolled seam outline, ring-pull lying flat on a rivet, tab to the front
    g.paint(0, 0, 7, 6, 6, 7, "galv")
    rim(g, cx, cy, 3.2, 7, "steel_light")
    for (i, j) in [(2, 2), (3, 2), (4, 2), (2, 3), (4, 3), (2, 4), (3, 4), (4, 4), (3, 5)]:
        g.set(i, j, 7, "chrome")                          # pull ring and tab
    g.set(3, 3, 7, "steel_dark")                          # rivet / hole in the ring
    return g


# ---------------------------------------------------------------------------
# food box (crackers)
# ---------------------------------------------------------------------------
@model("food_box", name="Food Box",
       story="A family box of crackers torn open in a hurry: the back flap stands up, the front "
             "flap is folded out, the waxed inner bag is crumpled at the top and the front corner "
             "is creased where it was squeezed into a backpack.",
       details=["Printed card box: muted mustard with a cream window panel and a rust title band",
                "Open top: back flap standing, front flap folded forward, one dust flap out",
                "Crumpled waxed-paper inner bag showing at the opening",
                "Creased front-left corner"],
       exclusions=["No text, logo, mascot or food photograph"],
       notes=["Cardboard cereal/cracker box with a muted printed panel, top flap open, a crease."])
def food_box():
    W, D, H = 18, 8, 19                                  # 0.225 x 0.10 x 0.24 m body
    ox, oy = 2, 0
    g = Grid(W + 3, D + 2, H + 5)
    x0, x1, y0, y1 = ox, ox + W - 1, oy, oy + D - 1
    g.box(x0, y0, 0, x1, y1, H - 1, "mustard")
    # printed front: rust title band, cream window panel, darker base strip
    g.paint(x0, y1, H - 5, x1, y1, H - 3, "terra")
    g.paint(x0 + 3, y1, 3, x1 - 3, y1, H - 8, "label_cream")
    g.paint(x0, y1, 0, x1, y1, 1, "mustard_dark")
    g.paint(x0, y0, H - 5, x0, y1, H - 3, "terra")       # title band wraps the left side
    g.paint(x0, y0 + 2, 3, x0, y1 - 2, 10, "label_cream")  # side panel (plain block)
    # open top: cut card edges, crumpled inner bag rising above the rim
    g.clear(x0 + 1, y0 + 1, H - 1, x1 - 1, y1 - 1, H - 1)
    g.paint(x0, y0, H - 1, x1, y1, H - 1, "card_hi")
    g.box(x0 + 1, y0 + 1, H - 1, x1 - 1, y1 - 1, H, "paper")
    g.box(x0 + 2, y0 + 2, H + 1, x1 - 5, y1 - 2, H + 1, "paper")
    g.box(x0 + 4, y0 + 3, H + 2, x1 - 9, y1 - 3, H + 2, "paper")
    g.paint(x0 + 7, y0 + 2, H + 1, x0 + 7, y1 - 2, H + 2, "cream_shadow")   # fold in the bag
    g.paint(x0 + 1, y1 - 1, H, x1 - 1, y1 - 1, H, "cream_shadow")
    # long flaps standing up: back flap straight, front flap bent outward at its tip
    g.box(x0, y0, H, x1, y0, H + 4, "card_hi")
    g.paint(x0, y0, H + 4, x1, y0, H + 4, "card")
    g.box(x0, y1, H, x1, y1, H + 2, "card_hi")
    g.box(x0, y1 + 1, H + 2, x1, y1 + 1, H + 3, "card_hi")
    g.paint(x0, y1 + 1, H + 3, x1, y1 + 1, H + 3, "card")
    # dust flaps: left one splayed outward, right one standing
    g.box(x0 - 2, y0 + 2, H - 1, x0 - 1, y1 - 2, H - 1, "card_hi")
    g.box(x1, y0 + 2, H, x1, y1 - 2, H + 1, "card_hi")
    # crease: crushed front-left corner with a darker fold line
    g.clear(x0, y1, 6, x0, y1, 9)
    g.paint(x0 + 1, y1, 5, x0 + 1, y1, 10, "mustard_dark")
    g.paint(x0, y1 - 1, 6, x0, y1 - 1, 9, "mustard_dark")
    return g


# ---------------------------------------------------------------------------
# snack package
# ---------------------------------------------------------------------------
@model("snack_package", name="Snack Package",
       story="A sealed bag of crisps from a petrol-station shelf, still puffed with air. It is "
             "untouched; only the film has crinkled where it was packed in the box.",
       details=["Pillow-shaped body bulging between flat crimped seals",
                "Serrated crimp teeth along the top and bottom edges",
                "Muted paprika film with a plain cream front panel",
                "Darker crinkle folds fanning from the crimps", "Vertical fin seal on the back"],
       exclusions=["No text, logo, mascot or food photograph"],
       notes=["Pillow-shaped crinkled snack bag with crimped ends and a plain colour panel.",
              "Stands on its bottom crimp in a display pose."])
def snack_package():
    W, H, T = 12, 17, 3                                  # width, height, max half-thickness
    g = Grid(W, 2 * T + 1, H)
    cy = T                                               # centre row (y = 3)
    # cushion body: flat faces, a soft taper into the crimps and rounded side edges
    taper = {2: 1, 3: 2, H - 3: 1, H - 4: 2}
    for x in range(W):
        for z in range(2, H - 2):
            t = taper.get(z, T)
            if x in (0, W - 1):
                t = max(1, t - 2)
            elif x in (1, W - 2):
                t = max(1, t - 1)
            g.box(x, cy - t, z, x, cy + t, z, "terra")
    for z in (0, 1, H - 2, H - 1):                       # crimped seals: one cell thick
        g.box(0, cy, z, W - 1, cy, z, "terra_dark")
    for x in range(0, W, 2):                             # serrated teeth
        g.set(x, cy, 0, 0)
        g.set(x, cy, H - 1, 0)
    for x in range(1, W, 2):
        g.paint_cell(x, cy, 1, "terra_hi")
        g.paint_cell(x, cy, H - 2, "terra_hi")
    g.set(0, cy, 0, "terra_dark")                         # keep the two outer corners
    # plain cream front panel and a few crinkle folds fanning from the crimps
    g.paint(3, 2 * T, 6, W - 4, 2 * T, 11, "label_cream")
    for (x, z0, z1) in [(2, 12, 13), (5, 12, 13), (9, 12, 13), (3, 4, 5), (8, 4, 5)]:
        for z in range(z0, z1 + 1):
            ys = [y for y in range(2 * T + 1) if g.get(x, y, z)]
            if ys:
                g.set(x, ys[-1], z, "terra_dark")
    for z in range(2, H - 2):                            # fin seal down the back
        ys = [y for y in range(2 * T + 1) if g.get(W // 2, y, z)]
        if ys:
            g.set(W // 2, ys[0], z, "terra_dark")
    return g


# ---------------------------------------------------------------------------
# large water container
# ---------------------------------------------------------------------------
@model("large_water_container", name="Large Water Container",
       story="A 20-litre camping water container that used to live in a car boot for summer "
             "trips. It has been refilled from the rain barrel many times; the base is scuffed "
             "and grey with grime and the spigot cap is a slightly different blue.",
       details=["Rounded block body with a moulded carry handle bridging the top",
                "Fill cap on the top, screw cap with a spigot tap low on the front",
                "Moulded horizontal stacking groove around the body",
                "Scuffed, grimy base and front corners"],
       exclusions=["No brand, volume markings or text"],
       notes=["20 L stackable blue plastic water container with moulded handle and a spigot cap."])
def large_water_container():
    g = Grid(11, 11, 18)
    body, dark, lite = "bottle_cap", "label_blue", "bottle"
    g.rbox(0, 0, 0, 10, 9, 14, body, r=1)
    g.box(1, 1, 15, 9, 8, 15, body)                      # rounded shoulder
    # stacking groove around the body
    for z in (10,):
        for x in range(0, 11):
            for y in range(0, 10):
                if g.get(x, y, z) and (x in (0, 10) or y in (0, 9)):
                    g.set(x, y, z, 0)
                    inner = (min(max(x, 1), 9), min(max(y, 1), 8))
                    g.set(inner[0], inner[1], z, dark)
    # moulded handle bridging the top from back to front
    g.box(4, 2, 16, 6, 2, 16, body)
    g.box(4, 7, 16, 6, 7, 16, body)
    g.box(4, 2, 17, 6, 7, 17, body)
    g.paint(4, 3, 17, 6, 6, 17, lite)                     # hand-worn grip
    # fill cap on top (front-left), spigot cap on the front face, low
    g.box(1, 6, 16, 2, 8, 16, "navy")
    g.box(4, 10, 1, 6, 10, 3, "blue_dark")
    g.box(5, 10, 0, 5, 10, 0, "blue_dark")
    g.paint(5, 10, 2, 5, 10, 2, "charcoal")               # spigot outlet
    # grime and scuffs
    g.paint(0, 0, 0, 10, 9, 0, "bluegrey_deep")
    g.paint(0, 9, 1, 1, 9, 2, "bluegrey")
    g.paint(9, 9, 1, 10, 9, 1, "bluegrey")
    return g


# ---------------------------------------------------------------------------
# food storage crate
# ---------------------------------------------------------------------------
def tin(g, x0, y0, z0, h, label, band, d=6):
    """A small tin on the grid: d = 6 (rows 4-6-6-6-6-4) or 7 cells, label + band colours,
    bright rim on top."""
    c = d / 2.0
    r = 3.0 if d == 6 else 3.2
    for (i, j) in g.disc_cells(c, c, r):
        g.box(x0 + i, y0 + j, z0, x0 + i, y0 + j, z0 + h - 1, label)
        g.set(x0 + i, y0 + j, z0, "steel_dark")
        g.set(x0 + i, y0 + j, z0 + h - 1, "galv")
        if h >= 6:
            g.box(x0 + i, y0 + j, z0 + h // 2 - 1, x0 + i, y0 + j, z0 + h // 2, band)
    rim(g, c, c, r, z0 + h - 1, "steel_light", x0, y0)


def jar(g, x0, y0, z0, h, fill):
    """A glass jar (6 cells round): opaque glass tinted by its contents, dark screw lid."""
    for (i, j) in g.disc_cells(3.0, 3.0, 3.0):
        g.box(x0 + i, y0 + j, z0, x0 + i, y0 + j, z0 + h - 3, fill)
        g.set(x0 + i, y0 + j, z0 + h - 2, "glass")
    for (i, j) in g.disc_cells(3.0, 3.0, 2.2):
        g.set(x0 + i, y0 + j, z0 + h - 1, "iron_warm")
    rim(g, 3.0, 3.0, 3.0, z0 + h - 2, "glass_hi", x0, y0)


@model("food_storage_crate", name="Food Storage Crate", cell=0.0125,
       why="Overridden from 2.5 cm to 1.25 cm so the tins and jars inside are built at the same "
           "scale and roundness as the canned_food and soup_can pickups (6-7 cell circles, not "
           "3-cell squares).",
       story="A ventilated stacking crate from a garage pantry shelf, half emptied: tins stacked "
             "two high at the front, jars of preserves at the back, a gap where the first tins "
             "were taken. Its lid leans against the back where it was dropped.",
       details=["Grey-green plastic crate with two bands of vent slots and end hand-holds",
                "Rolled top lip", "Stacks of tins (green and red labels) and three jars with lids",
                "Gap at the front-left where tins were taken",
                "Ribbed lid leaning against the back"],
       exclusions=["No brand or text on the tins or crate", "No loose food"],
       notes=["Ventilated plastic stacking crate holding cans and jars, lid leaning against it.",
              "The lid leaning behind it raises the silhouette to about 0.33 m."])
def food_storage_crate():
    L, D, H = 36, 26, 21                                  # 0.45 x 0.325 x 0.26 m
    oy = 3                                                # room behind for the leaning lid
    g = Grid(L, D + oy, 27)
    body, dark, lite = "sage", "sage_dark", "sage_hi"
    y0, y1 = oy, oy + D - 1
    g.box(0, y0, 0, L - 1, y1, H - 1, body)
    g.clear(1, y0 + 1, 1, L - 2, y1 - 1, H - 1)
    g.paint(0, y0, H - 1, L - 1, y1, H - 1, lite)         # rolled lip
    g.paint(0, y0, 0, L - 1, y1, 0, dark)                 # foot
    # vent slots: two bands on every wall
    for (za, zb) in ((3, 7), (11, 15)):
        for x in range(3, L - 3, 3):
            g.clear(x, y0, za, x, y0, zb)
            g.clear(x, y1, za, x, y1, zb)
        for y in range(y0 + 3, y1 - 2, 3):
            g.clear(0, y, za, 0, y, zb)
            g.clear(L - 1, y, za, L - 1, y, zb)
    for x in (0, L - 1):                                  # hand-holds in the end walls
        g.clear(x, y0 + 9, 17, x, y1 - 9, 18)
    # contents: back row jars, front rows tins stacked two high, a gap front-left
    for k, fill in enumerate(("rust", "mustard_dark", "red_dark")):
        jar(g, 3 + 7 * k, y0 + 17, 1, 13, fill)
    tin(g, 24, y0 + 17, 1, 9, "label_green", "label_cream")
    tin(g, 24, y0 + 17, 10, 9, "label_green", "label_cream")
    stacks = [(10, y0 + 9, "label_red", "label_cream"), (17, y0 + 9, "label_green", "label_cream"),
              (24, y0 + 9, "label_red", "label_cream"), (17, y0 + 2, "label_green", "label_cream"),
              (24, y0 + 2, "label_red", "label_cream"), (3, y0 + 9, "label_green", "label_cream")]
    for (x, y, lab, band) in stacks:
        tin(g, x, y, 1, 8, lab, band, d=7)
        tin(g, x, y, 9, 8, lab, band, d=7)
    tin(g, 10, y0 + 2, 1, 8, "label_red", "label_cream", d=7)   # single tin; one taken above
    # lid leaning against the back: panel with a perimeter rib, bottom edge on the ground
    for (ya, za, zb) in ((0, 0, 7), (1, 8, 16), (2, 17, 25)):
        g.box(0, ya, za, L - 1, ya, zb, body)
    for (ya, za, zb) in ((1, 0, 7), (2, 8, 16), (3, 17, 21)):
        for x in (0, 1, L - 2, L - 1):
            g.box(x, ya, za, x, ya, zb, dark)             # rib on the inner face
        if za == 0:
            g.box(0, ya, za, L - 1, ya, za, dark)
    for (ya, z) in ((2, 25), (2, 24)):
        g.box(0, ya, z, L - 1, ya, z, dark)
    g.paint(0, 0, 25, L - 1, 2, 25, lite)
    for x in range(6, L - 5, 6):                          # cross ribs
        g.box(x, 1, 1, x, 1, 7, dark)
        g.box(x, 2, 8, x, 2, 16, dark)
    return g


# ---------------------------------------------------------------------------
# small cooler
# ---------------------------------------------------------------------------
@model("small_cooler", name="Small Cooler",
       story="A picnic cooler that went to every beach weekend for fifteen years. The teal has "
             "faded, the corners are scuffed pale, and now it keeps a few cans cool in a dark "
             "garage instead of drinks in the sun.",
       details=["Faded teal body with chamfered corners and a moulded lid seat",
                "Pale lid with a front lip", "Swing handle folded back over the hinges",
                "Drain plug low on the front", "Scuffed corners and grimy base"],
       exclusions=["No brand or text", "No ice or contents shown"],
       notes=["Picnic cooler with faded teal body, pale lid and swing handle, scuffed corners."])
def small_cooler():
    g = Grid(18, 13, 12)
    body, dark, deep, lite = "teal", "teal_dark", "teal_deep", "teal_hi"
    g.rbox(1, 1, 0, 16, 12, 9, body, r=1)
    g.paint(1, 1, 0, 16, 12, 0, deep)                      # grimy base
    g.paint(1, 1, 9, 16, 12, 9, dark)                      # lid seat
    # lid: two cells, chamfered, front lip
    g.rbox(1, 1, 10, 16, 12, 11, "almond", r=1)
    g.paint(2, 2, 11, 15, 11, 11, "porcelain_mid")
    g.box(7, 13 - 1, 9, 10, 12, 9, "almond_dark")          # lip to lift the lid
    # swing handle: pivots on the ends, arms folded back, bar behind the back wall
    for x in (0, 17):
        g.box(x, 5, 7, x, 6, 8, "almond_dark")             # pivot boss
        g.box(x, 0, 7, x, 4, 7, "porcelain_mid")           # arm folded back
    g.box(0, 0, 7, 17, 0, 7, "porcelain_mid")              # grip bar behind
    # hinges at the back top
    for x in (4, 12):
        g.box(x, 0, 9, x + 1, 0, 10, "almond_dark")
    # drain plug
    g.box(13, 12, 1, 14, 12, 2, "charcoal")
    g.set(13, 12, 2, "iron_edge")
    # scuffed corners (pale, worn plastic) on the vertical chamfers
    for (x, y) in [(2, 12), (1, 11), (15, 12), (16, 11)]:
        g.paint(x, y, 1, x, y, 4, lite)
    g.paint(1, 11, 5, 1, 11, 6, lite)
    g.paint(2, 12, 10, 3, 12, 10, "almond_dark")           # lid corner rubbed
    return g


# ---------------------------------------------------------------------------
# bandage roll
# ---------------------------------------------------------------------------
@model("bandage_roll", name="Bandage Roll",
       story="A fresh roll of gauze from a bathroom cabinet's first-aid tin, just unwrapped. "
             "The loose end has been pulled out across the floor, ready to be cut.",
       details=["Clean 8-cell round roll lying on its side",
                "End faces show the wound layers and a darker core",
                "Loose tail unrolled flat from under the roll, with a soft fold and a frayed end"],
       exclusions=["No packaging, clips or tape", "No blood"],
       notes=["Rolled gauze bandage with a loose tail unrolled.",
              "The tail is one cell (1.25 cm) thick, an intentional exaggeration of real gauze."])
def bandage_roll():
    W = 10                                               # roll width along X (12.5 cm)
    g = Grid(W, 13, 8)
    for x in range(W):
        for (j, k) in g.disc_cells(4.0, 4.0, 4.0):
            g.set(x, j, k, "porcelain_hi")
    for x in (0, W - 1):                                 # end faces: wound layers and core
        for (j, k) in g.disc_cells(4.0, 4.0, 4.0):
            d = math.hypot(j + 0.5 - 4.0, k + 0.5 - 4.0)
            if d < 1.2:
                g.set(x, j, k, "porcelain_shadow")      # cardboard-free core
            elif d < 2.9:
                g.set(x, j, k, "porcelain_mid")         # tightly wound inner layers
            else:
                g.set(x, j, k, "porcelain")             # looser outer layers
    # loose tail leaving the bottom front of the roll, a soft fold, frayed end
    g.box(1, 6, 0, W - 2, 11, 0, "porcelain_hi")
    g.clear(1, 9, 0, W - 2, 9, 0)
    g.box(1, 9, 1, W - 2, 9, 1, "porcelain")             # soft fold lifting off the floor
    g.box(1, 8, 1, W - 2, 8, 1, "porcelain_hi")
    g.box(1, 10, 1, W - 2, 10, 1, "porcelain_hi")
    g.paint(1, 11, 0, W - 2, 11, 0, "porcelain")
    for x in (2, 5, 7):
        g.set(x, 12, 0, "porcelain")                     # loose threads
    g.paint(1, 6, 0, W - 2, 6, 0, "porcelain")           # shadowed lip under the roll
    return g


# ---------------------------------------------------------------------------
# first-aid kit
# ---------------------------------------------------------------------------
@model("first_aid_kit", name="First-Aid Kit",
       story="A hard-case first-aid kit that hung on a utility-room wall for years and was "
             "carried out to the car when things went wrong. The off-white plastic is grubby "
             "along the bottom and scuffed at the corners; it still closes.",
       details=["Off-white clamshell case with rounded corners and a visible parting line",
                "Large red cross on the front", "Dark carry handle and two latches on top",
                "Hinge knuckles along the bottom, wall-hanging slots on the back",
                "Grubby bottom edge and scuffed corners"],
       exclusions=["No text, symbols other than the cross, or brand"],
       notes=["Off-white hard case with a red cross, latch and handle."])
def first_aid_kit():
    L, D, H = 30, 11, 18
    g = Grid(L, D, H + 3)
    body = "porcelain"
    g.rbox(0, 0, 0, L - 1, D - 1, H - 1, body, r=2)
    for (x0, x1) in ((0, 1), (L - 2, L - 1)):            # rounded top and bottom corners
        g.clear(x0, 0, H - 1, x1, D - 1, H - 1)
        g.clear(x0, 0, 0, x1, D - 1, 0)
    g.clear(0, 0, H - 2, 0, D - 1, H - 2)
    g.clear(L - 1, 0, H - 2, L - 1, D - 1, H - 2)
    # parting line between the two shells (y = 5) all round; the slab's interior is hidden
    g.paint(0, 5, 0, L - 1, 5, H - 1, "porcelain_mid")
    # red cross on the front face
    cx0, cz0 = L // 2 - 2, H // 2 - 2                      # 4 x 4 centre square
    g.paint(cx0, D - 1, cz0 - 4, cx0 + 3, D - 1, cz0 + 7, "signal_red")
    g.paint(cx0 - 4, D - 1, cz0, cx0 + 7, D - 1, cz0 + 3, "signal_red")
    # handle and latches on top
    g.box(11, 4, H, 11, 6, H + 1, "charcoal")
    g.box(18, 4, H, 18, 6, H + 1, "charcoal")
    g.box(11, 4, H + 2, 18, 6, H + 2, "charcoal")
    g.paint(12, 4, H + 2, 17, 6, H + 2, "iron_edge")      # rubbed grip
    for x in (5, 23):
        g.box(x, 4, H, x + 1, 6, H, "porcelain_shadow")
    for x in (5, 23):                                     # latch tongues over the front edge
        g.box(x, D - 1, H - 2, x + 1, D - 1, H - 2, "porcelain_deep")
    # hinge knuckles along the bottom back, wall slots on the back
    for x in (6, 7, 22, 23):
        g.paint(x, 0, 0, x, 0, 1, "porcelain_shadow")
    g.paint(13, 0, 13, 16, 0, 14, "porcelain_deep")
    # wear: grubby bottom edge, scuffed front corners
    g.paint(0, 0, 0, L - 1, D - 1, 0, "porcelain_mid")
    g.paint(2, D - 1, 1, 3, D - 1, 2, "porcelain_shadow")
    g.paint(L - 3, D - 1, 1, L - 3, D - 1, 3, "porcelain_shadow")
    g.paint(0, D - 3, 3, 0, D - 3, 5, "porcelain_shadow")
    return g


# ---------------------------------------------------------------------------
# medicine bottle
# ---------------------------------------------------------------------------
@model("medicine_bottle", name="Medicine Bottle",
       story="A large amber pharmacy stock bottle of painkillers from a ransacked pharmacy "
             "counter. Handled a lot: the white label has a torn corner and the cap is scuffed.",
       details=["Clean 8-cell round amber bottle with a narrower neck",
                "White child-proof cap with grip ridges",
                "Plain white label wrapped round with a blue band; torn top corner"],
       exclusions=["No text, dosage or pharmacy name", "No loose pills"],
       notes=["Amber pharmacy bottle with white cap and plain label.",
              "Sized as a pharmacy stock bottle (10 x 19 cm), the largest believable size, so it "
              "stays in scale with the cans beside it."])
def medicine_bottle():
    g = Grid(8, 8, 15)
    c = 4.0
    can_body(g, 0, 0, c, c, 4.0, 0, 11, "rust")
    g.paint(0, 0, 0, 7, 7, 0, "rust_dark")               # thick glass base
    g.paint(0, 0, 11, 7, 7, 11, "rust_dark")              # shoulder
    can_body(g, 0, 0, c, c, 3.0, 12, 12, "rust_dark")    # neck
    can_body(g, 0, 0, c, c, 4.0, 13, 14, "porcelain_hi") # cap
    for (i, j) in g.ring_cells(c, c, 4.0):               # grip ridges around the cap
        if (i + j) % 2 == 0:
            g.paint_cell(i, j, 13, "porcelain_mid")
    rim(g, c, c, 4.0, 14, "porcelain")
    # label: wraps almost all round (ends meet at the back), blue band near the top,
    # torn top corner on the front-left
    for (i, j) in g.ring_cells(c, c, 4.0):
        if -105 <= angle_of(i, j, c, c) <= -75:
            continue
        for z in range(2, 10):
            g.paint_cell(i, j, z, "paper")
        g.paint_cell(i, j, 8, "label_blue")
    for (i, j, z) in [(1, 6, 9), (1, 6, 8), (2, 7, 9), (0, 5, 9)]:
        g.paint_cell(i, j, z, "rust")
    return g


# ---------------------------------------------------------------------------
# tablet packet
# ---------------------------------------------------------------------------
@model("tablet_packet", name="Tablet Packet",
       story="A small carton of tablets found in a coat pocket. The end flap is open and the "
             "blister strip has slid half out; two tablets are already gone.",
       details=["White card carton lying flat with a muted blue band",
                "Open end flap standing up", "Blister strip sliding out, foil side down",
                "Grid of tablets in clear blisters; one empty blister and one torn-out cell"],
       exclusions=["No text, dosage or brand", "No loose tablets"],
       notes=["Small carton with a blister strip sliding out.",
              "Lies flat as a dropped carton would, so it is lower than GPT's 10 cm reference."])
def tablet_packet():
    g = Grid(16, 7, 6)
    CL = 9                                               # carton length x 0..8
    g.box(0, 0, 0, CL - 1, 6, 2, "paper")
    g.clear(1, 1, 1, CL - 1, 5, 1)                       # open at the +X end
    g.paint(2, 0, 2, 3, 6, 2, "label_blue")              # blue band over the top
    g.paint(2, 6, 0, 3, 6, 2, "label_blue")
    g.paint(2, 0, 0, 3, 0, 2, "label_blue")
    g.paint(5, 2, 2, 7, 4, 2, "porcelain_mid")           # plain panel block
    g.box(CL - 1, 1, 3, CL - 1, 5, 5, "paper")           # end flap standing open
    g.paint(CL - 1, 1, 5, CL - 1, 5, 5, "porcelain_mid")
    # blister strip: inside on the carton floor, sliding out and dropping to the ground
    g.box(3, 1, 1, CL + 1, 5, 1, "foil")
    g.box(CL + 1, 1, 0, CL + 6, 5, 0, "foil")
    pills = {(CL + 1, 2, 2), (CL + 1, 4, 2), (CL + 3, 2, 1), (CL + 3, 4, 1), (CL + 5, 2, 1),
             (CL + 5, 4, 1)}
    for (x, y, z) in pills:
        g.set(x, y, z, "porcelain_hi")                   # tablets seen through the blisters
    g.set(CL + 1, 2, 1, "bottle_hi")                     # blister walls on the bend
    g.set(CL + 1, 4, 1, "bottle_hi")
    g.set(CL + 5, 4, 1, "bottle_hi")                     # empty blister
    g.set(CL + 3, 2, 1, 0)                               # tablet pushed through:
    g.set(CL + 3, 2, 0, "steel_dark")                    # torn foil
    return g


# ---------------------------------------------------------------------------
# medical bag (paramedic duffel)
# ---------------------------------------------------------------------------
@model("medical_bag", name="Medical Bag", cell=0.0125,
       why="Overridden from 2.5 cm to 1.25 cm (the medical family's tier): zips, webbing and "
           "the cross patch are 1-3 cm features that would all become 2.5 cm bars, and the "
           "cross would shrink to a 3-cell plus.",
       story="A paramedic's duffel left in the back of an ambulance at a roadblock. It has "
             "been opened and closed many times since: the zips are intact, the base is grimy "
             "and the reflective band has dulled.",
       details=["Soft navy duffel with a rounded top and flat base",
                "Front zip pocket carrying a white patch with a red cross",
                "Zip end pockets", "Main zip along the top with a pull tab",
                "Two webbing carry handles joined by a wrap",
                "Shoulder strap clipped to both ends, lying along the top",
                "Dulled reflective band around the body"],
       exclusions=["No text, service names or badges", "No visible medical contents"],
       notes=["Paramedic duffel with a red cross patch, zip pockets and strap."])
def medical_bag():
    g = Grid(33, 20, 25)
    body, dark, deep = "navy", "navy_dark", "blue_deep"
    yc, zc, a, b = 8.5, 9.5, 8.0, 10.0                   # cross-section centre / half-sizes

    def half_width(z):
        if z == 0:
            return a - 1
        if z <= zc:
            return a
        return a * max(0.0, 1.0 - abs((z + 0.5 - zc) / b) ** 4) ** 0.25

    for x in range(1, 32):
        shrink = 1 if x in (1, 31) else 0
        for z in range(0, 20 - shrink):
            w = half_width(z + shrink) - shrink
            ya, yb = int(math.ceil(yc - w - 0.5)), int(math.floor(yc + w - 0.5))
            if yb >= ya:
                g.box(x, ya, z, x, yb, z, body)
    g.paint(0, 0, 0, 32, 19, 0, dark)                    # grimy base seam
    # reflective band around the body (above the pockets)
    g.paint(1, 0, 15, 31, 19, 16, "galv")
    # front zip pocket with the cross patch
    g.box(6, 17, 1, 26, 18, 14, body)
    g.clear(6, 18, 14, 6, 18, 14)
    g.clear(26, 18, 14, 26, 18, 14)
    g.paint(6, 17, 14, 26, 18, 14, "black")              # zip along the top edge
    g.paint(6, 18, 1, 26, 18, 1, dark)
    g.paint(12, 18, 4, 20, 18, 12, "paper")              # white patch
    g.paint(15, 18, 5, 17, 18, 11, "signal_red")         # cross, 3-cell arms
    g.paint(13, 18, 7, 19, 18, 9, "signal_red")
    g.paint(6, 18, 2, 7, 18, 3, "blue_dark")             # scuffed pocket corner
    # end pockets with zips
    for x in (0, 32):
        g.box(x, 4, 2, x, 13, 13, body)
        g.paint(x, 4, 13, x, 13, 13, "black")
        g.paint(x, 4, 2, x, 13, 2, dark)
    # main zip along the top, pull tab
    g.paint(4, 8, 19, 28, 9, 19, "black")
    g.box(28, 10, 19, 28, 11, 19, "steel_light")
    # carry handles joined by a wrap
    for y0 in (5, 10):
        for x0 in (10, 21):
            g.box(x0, y0, 19, x0 + 1, y0 + 1, 22, "charcoal")
        g.box(10, y0, 23, 22, y0 + 1, 23, "charcoal")
    g.box(14, 5, 23, 18, 11, 24, dark)                   # velcro wrap
    g.paint(14, 5, 24, 18, 11, 24, deep)
    # shoulder strap: clipped to both ends, lying along the back of the top
    g.box(3, 12, 20, 29, 13, 20, "charcoal")
    g.box(13, 12, 20, 19, 14, 21, "iron")                # shoulder pad
    for (xa, xb, xc) in ((0, 1, 2), (31, 32, 30)):
        g.box(xc, 12, 18, xc, 13, 20, "charcoal")
        g.box(xa, 12, 15, xb, 13, 18, "steel")           # clip on the D-ring
    return g


# ---------------------------------------------------------------------------
# emergency supply box
# ---------------------------------------------------------------------------
@model("emergency_supply_box", name="Emergency Supply Box",
       story="A heavy-duty plastic tote packed by a careful neighbour as an emergency kit and "
             "strapped shut. It was never opened: the straps are tight, the plastic is clean "
             "and the stencilled crosses are crisp.",
       details=["Grey tote with a lighter lid, end hand-holds and a lid parting line",
                "Two webbing straps over the lid and down the front, cam buckles",
                "Red stencilled cross on the lid and on the front"],
       exclusions=["No text or brand", "No visible contents"],
       notes=["Sturdy plastic tote with a stencilled cross, lid strapped down."])
def emergency_supply_box():
    g = Grid(22, 15, 16)
    body, lid, dark = "slate_dark", "slate", "slate_deep"
    g.rbox(1, 1, 0, 20, 12, 12, body, r=1)
    g.paint(1, 1, 0, 20, 12, 0, dark)                     # foot
    g.rbox(1, 1, 13, 20, 12, 14, lid, r=1)               # lid
    g.paint(1, 1, 13, 20, 12, 13, "slate_hi")             # lid skirt edge
    for x in (0, 21):                                     # moulded end hand-holds
        g.box(x, 4, 10, x, 9, 11, body)
        g.paint(x, 4, 10, x, 9, 10, dark)
    # straps over the lid and down front and back, cam buckles on the front
    for x0 in (4, 15):
        g.box(x0, 1, 15, x0 + 1, 12, 15, "charcoal")
        g.box(x0, 13, 1, x0 + 1, 13, 15, "charcoal")
        g.box(x0, 0, 1, x0 + 1, 0, 15, "charcoal")
        g.box(x0, 14, 6, x0 + 1, 14, 7, "steel")
        g.paint(x0, 14, 6, x0 + 1, 14, 6, "steel_dark")
    # stencilled crosses: lid top and front face, 6 x 6 with 2-cell arms
    g.paint(10, 4, 14, 11, 9, 14, "signal_red")
    g.paint(8, 6, 14, 13, 7, 14, "signal_red")
    g.paint(10, 12, 3, 11, 12, 8, "signal_red")
    g.paint(8, 12, 5, 13, 12, 6, "signal_red")
    return g
