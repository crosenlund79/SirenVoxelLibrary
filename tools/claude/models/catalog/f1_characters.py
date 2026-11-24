"""Batch F1 - characters and enemies (creator: Claude). X right, Y front (+Y), Z up; inclusive cells.

Static reference figures for an exhibition house: neutral display pose (standing on both feet,
feet apart, arms slightly away from the body), 0.05 m cells like the game's character rig.
The character's right side is +X; the hero camera sees the front and the character's LEFT
(-X) side, so asymmetric story details go there.
"""
from catalog_registry import MANIFEST, model
from voxkit import Grid

CAPSULE = ("Upright capsule about 0.3 m in radius and dimensions_m[2] tall, centred on the "
           "pivot; static reference figure, no rig.")


def notes(base_id, dims_note):
    """Manifest brief plus a note on where the figure departs from the reference size."""
    return [MANIFEST[base_id]["brief"], dims_note]


# ---------------------------------------------------------------------------
# shared body helpers
# ---------------------------------------------------------------------------
def box(g, x0, x1, y0, y1, z0, z1, c):
    """Box with ranges grouped per axis (reads better for limbs than Grid.box)."""
    g.box(x0, y0, z0, x1, y1, z1, c)


def paint(g, x0, x1, y0, y1, z0, z1, c):
    g.paint(x0, y0, z0, x1, y1, z1, c)


def insert_layer(g, z):
    """Lengthen a figure by repeating layer z (used to give a tall figure longer shins
    without re-deriving every coordinate above the knee)."""
    import numpy as np
    g.v = np.insert(g.v, z, g.v[:, :, z], axis=2)


def soft_box(g, x0, x1, y0, y1, z0, z1, c):
    """Box with its four vertical edges chamfered: torsos, packs, heads."""
    g.rbox(x0, y0, z0, x1, y1, z1, c, 1)


def boot(g, x0, x1, yh, yt, top, upper, sole, toe=None):
    """Closed shoe/boot: sole row, toe box, shaft over the heel up to `top`."""
    box(g, x0, x1, yh, yt, 0, 0, sole)
    box(g, x0, x1, yh, yt, 1, 1, toe or upper)
    if top >= 2:
        box(g, x0, x1, yh, yh + 2, 2, top, upper)
    if x1 - x0 >= 2:                       # round the toe cap
        g.clear(x0, yt, 1, x0, yt, 1)
        g.clear(x1, yt, 1, x1, yt, 1)


def hand(g, xi, xo, y0, ztop, skin, shade, length=4, thumb=True):
    """Relaxed hand hanging at the side, palm facing the thigh.
    xi = column next to the body, xo = outer column; y0..y0+1 is the palm width.
    The back of the hand (outer column) is full length, the inner column is the palm and
    thumb ball; the fingertips taper to one column."""
    box(g, xo, xo, y0, y0 + 1, ztop - length + 1, ztop, skin)         # back of hand + fingers
    box(g, xi, xi, y0, y0 + 1, ztop - 1, ztop, skin)                  # palm
    g.clear(xo, y0 + 1, ztop - length + 1, xo, y0 + 1, ztop - length + 1)   # fingertip taper
    paint(g, xo, xo, y0, y0 + 1, ztop - length + 1, ztop - length + 2, shade)  # curled fingers
    if thumb:
        g.set(xi, y0 + 2, ztop - 1, skin)                             # thumb, forward


def face(g, c, yf, zeye, skin, shade, eye, nose=True, mouth=True):
    """Carve a face into a 3-wide head whose front plane is yf: recessed dark eyes either side
    of the nose bridge, optionally a one-cell protruding nose tip and a mouth shadow (the
    figures mostly set nose and mouth as flush value cells instead)."""
    for s in (-1, 1):
        g.clear(c + s, yf, zeye, c + s, yf, zeye)
        g.set(c + s, yf - 1, zeye, eye)
    g.set(c, yf, zeye, skin)
    if nose:
        g.set(c, yf + 1, zeye - 1, skin)
    if mouth:
        g.set(c, yf, zeye - 2, shade)


# ---------------------------------------------------------------------------
# Player survivor
# ---------------------------------------------------------------------------
@model("survivor",
       story="Someone who was ordinary before the sirens stopped: a dark work jacket, cargo "
             "trousers worn pale at the knees from kneeling, the orange beanie and scarf they "
             "were wearing that morning, and a pack they now never take off.",
       details=["Orange knitted beanie with a rolled cuff and a matching scarf, tail hanging "
                "over the left chest (the one warm accent)",
                "Dark zipped jacket with ribbed hem and cuffs",
                "Brown leather backpack shoulder straps with a sternum strap",
                "Olive canvas backpack with a front pocket, top lid, grab loop and a rolled "
                "wool bedroll strapped underneath",
                "Metal bottle in the pack's left side pocket",
                "Cargo pocket on the left thigh; knees rubbed pale",
                "Leather work boots with scuffed toe caps"],
       exclusions=["No weapon or tool in the hands (separate catalog models)",
                   "No logos, patches or readable text"],
       pivot_note="Between the feet at ground level.",
       silhouette="Rounded beanie head, sloped shoulders with a pack hump behind, bedroll "
                  "under the pack, arms held slightly away, feet apart.",
       collision_hint=CAPSULE,
       notes=notes("survivor", "Height is the 1.75 m player height. Narrower than the "
                   "0.85 m reference because the arms hang only slightly away from the body; "
                   "deeper than 0.36 m because the pack and bedroll add ~0.15 m behind it."))
def survivor():
    c = 8                                   # centre column; body is symmetric about it
    g = Grid(2 * c + 1, 12, 35)
    YB = 4                                  # back of torso; pack sits behind it
    jacket, jdark, jlite = "slate_dark", "slate_deep", "slate"
    trou, trou_l = "khaki_dark", "khaki"
    skin, skin_s = "skin1", "skin1_shadow"

    # --- boots (feet apart, toes forward)
    for s in (-1, 1):
        x0, x1 = sorted((c + s * 2, c + s * 4))
        boot(g, x0, x1, YB, YB + 5, 2, "leather_dark", "black")
        paint(g, x0, x1, YB + 3, YB + 5, 1, 1, "leather")             # toe caps scuffed
        box(g, x0, x1, YB + 1, YB + 3, 3, 8, trou)                    # shins
        x0t, x1t = sorted((c + s * 1, c + s * 3))
        box(g, x0t, x1t, YB + 1, YB + 3, 9, 14, trou)                 # thighs
        xk0, xk1 = sorted((c + s * 2, c + s * 3))
        paint(g, xk0, xk1, YB + 3, YB + 3, 8, 9, trou_l)              # knees rubbed pale
        paint(g, x0, x1, YB + 1, YB + 3, 3, 3, "card_deep")           # trouser hem over boots
    box(g, c - 3, c + 3, YB + 1, YB + 3, 13, 15, trou)                # seat / crotch
    # cargo pocket on the left thigh (camera side)
    box(g, c - 4, c - 4, YB + 1, YB + 2, 10, 12, trou)
    paint(g, c - 4, c - 4, YB + 1, YB + 2, 12, 12, "card_deep")

    # --- jacket torso
    soft_box(g, c - 3, c + 3, YB, YB + 4, 14, 27, jacket)
    paint(g, c - 3, c + 3, YB, YB + 4, 14, 14, jdark)                  # ribbed hem
    paint(g, c, c, YB + 4, YB + 4, 15, 26, "charcoal")                 # zip
    for x0 in (c - 2, c + 1):
        paint(g, x0, x0 + 1, YB + 4, YB + 4, 18, 18, jdark)            # hand-pocket welts
    paint(g, c - 3, c + 3, YB, YB + 4, 27, 27, jlite)                  # shoulder tops catch light
    # shoulder straps (brown leather) over the shoulders and down the chest
    for x in (c - 2, c + 2):
        paint(g, x, x, YB, YB + 4, 27, 27, "leather")
        paint(g, x, x, YB + 4, YB + 4, 20, 27, "leather")
        paint(g, x, x, YB + 4, YB + 4, 20, 20, "brass_dark")           # strap buckle
    paint(g, c - 2, c + 2, YB + 4, YB + 4, 24, 24, "leather_dark")      # sternum strap

    # --- arms: upper arm close to the body, forearm and hand angled slightly out
    for s in (-1, 1):
        xa0, xa1 = sorted((c + s * 4, c + s * 5))
        box(g, xa0, xa1, YB + 1, YB + 2, 22, 26, jacket)
        g.clear(c + s * 5, YB + 1, 26, c + s * 5, YB + 2, 26)           # rounded shoulder
        paint(g, c + s * 4, c + s * 4, YB + 1, YB + 2, 26, 26, jlite)
        xf0, xf1 = sorted((c + s * 5, c + s * 6))
        box(g, xf0, xf1, YB + 1, YB + 2, 17, 21, jacket)
        paint(g, xf0, xf1, YB + 1, YB + 2, 17, 17, jdark)               # cuff
        hand(g, c + s * 5, c + s * 6, YB + 1, 16, skin, skin_s)

    # --- scarf wrapped high round the neck, tail over the left chest
    soft_box(g, c - 2, c + 2, YB, YB + 4, 28, 29, "rust")
    paint(g, c - 2, c + 2, YB, YB + 4, 28, 28, "rust_dark")
    box(g, c - 2, c - 1, YB + 5, YB + 5, 21, 28, "rust")
    paint(g, c - 2, c - 1, YB + 5, YB + 5, 21, 21, "rust_dark")        # fringe end
    paint(g, c - 1, c - 1, YB + 5, YB + 5, 24, 26, "rust_dark")        # fold

    # --- head: 3-wide face plane, cheeks/ears set back one cell, beanie
    box(g, c - 1, c + 1, YB + 1, YB + 4, 30, 32, skin)
    for s in (-1, 1):
        box(g, c + s * 2, c + s * 2, YB + 1, YB + 3, 31, 32, skin)     # cheeks / temples
        box(g, c + s * 2, c + s * 2, YB + 1, YB + 2, 30, 30, skin)     # jaw angle
        g.set(c + s * 2, YB + 2, 31, skin_s)                           # ear
        box(g, c + s * 2, c + s * 2, YB + 1, YB + 2, 32, 32, "hair_brown")
    paint(g, c - 2, c + 2, YB + 1, YB + 1, 31, 32, "hair_brown")       # hair at the nape
    face(g, c, YB + 4, 32, skin, skin_s, "hair_black", nose=False)
    g.set(c, YB + 4, 31, "skin1_hi")                                   # nose
    soft_box(g, c - 2, c + 2, YB, YB + 4, 33, 33, "rust_dark")          # rolled cuff
    soft_box(g, c - 2, c + 2, YB, YB + 3, 34, 34, "rust")               # crown, slouched back

    # --- backpack, bedroll, bottle in the left side pocket
    box(g, c - 4, c - 4, 1, YB - 1, 17, 19, "olive_dark")
    box(g, c - 4, c - 4, 2, 2, 20, 21, "galv_dark")
    soft_box(g, c - 3, c + 3, 1, YB - 1, 17, 28, "olive")
    soft_box(g, c - 3, c + 3, 1, YB - 1, 28, 29, "olive_dark")         # top lid
    g.set(c, 2, 30, "leather")                                         # grab loop
    box(g, c - 2, c + 2, 0, 0, 19, 23, "olive")                        # front pocket
    paint(g, c - 2, c + 2, 0, 0, 23, 23, "olive_dark")                 # pocket flap
    for x in (c - 2, c + 2):
        paint(g, x, x, 0, 1, 17, 25, "leather_dark")                   # compression straps
    g.cyl_x(2.5, 15.5, 1.6, c - 4, c + 4, "wool")                      # bedroll
    paint(g, c - 4, c - 4, 0, YB, 14, 17, "wool_dark")
    paint(g, c + 4, c + 4, 0, YB, 14, 17, "wool_dark")
    for x in (c - 2, c + 2):
        paint(g, x, x, 0, YB - 1, 14, 16, "leather_dark")
    return {"grid": g, "pivot_cells": (c + 0.5, YB + 3.0, 0.0)}


# ---------------------------------------------------------------------------
# Ordinary psycho
# ---------------------------------------------------------------------------
@model("ordinary_psycho",
       story="An office worker who walked out of the building the day the sirens stopped and "
             "never went home: the same pale shirt, the tie still knotted, one shoe lost "
             "somewhere along the way. Whatever happened to them happened on the inside.",
       details=["Hunched upper back, neck and head jutting forward and down",
                "Long arms hanging forward, left shoulder dropped",
                "Limping left leg: knee bent, heel lifted, shoe lost (sock foot)",
                "Pale office shirt half untucked, loosened tie hanging away from the chest",
                "Warm grey suit trousers torn at the left knee",
                "Grime at the shirt hem, cuffs and dragged trouser hems; one restrained "
                "dried spill down the right chest",
                "Pallid skin, thinning greying hair, slack mouth"],
       exclusions=["Not a zombie: no wounds, exposed bone or rotting flesh",
                   "No gore beyond restrained stains", "No weapon"],
       pivot_note="Between the feet at ground level.",
       silhouette="Forward-bowed figure: rounded upper back, head below the shoulder-line "
                  "plane and ahead of the chest, arms dangling in front of the thighs, one "
                  "bent trailing leg.",
       collision_hint=CAPSULE,
       notes=notes("ordinary_psycho", "A tall man stooped to 1.80 m (reference 1.82 m). "
                   "Narrower than the 0.85 m reference because the arms hang forward in front "
                   "of the thighs instead of out to the sides."))
def ordinary_psycho():
    c = 8
    g = Grid(2 * c + 1, 13, 36)
    shirt, shirt_s = "blue_hi", "blue"
    trou, trou_s = "wgrey_dark", "wgrey_deep"
    skin, skin_s = "skin_pallid", "porcelain_deep"
    grime = "wool_dark"
    hair = "ash_dark"                       # greying, thinning

    # --- right leg: straight, weight-bearing, dress shoe
    boot(g, c + 1, c + 3, 3, 8, 1, "iron_dark", "black")
    box(g, c + 1, c + 3, 3, 4, 2, 2, "iron_dark")                     # heel counter
    box(g, c + 1, c + 3, 4, 6, 2, 14, trou)
    paint(g, c + 1, c + 3, 4, 6, 2, 2, grime)                         # dragged hem
    # --- left leg: knee bent, heel lifted, shoe lost (sock foot)
    sock = "cream_deep"
    box(g, c - 4, c - 2, 4, 8, 0, 0, "wool_dark")                     # grimy sole, toes down
    box(g, c - 4, c - 2, 3, 7, 1, 1, sock)                            # heel lifted
    g.clear(c - 4, 8, 0, c - 4, 8, 0)
    g.clear(c - 2, 8, 0, c - 2, 8, 0)
    box(g, c - 4, c - 2, 3, 5, 2, 4, trou)                            # shin, slanting back
    box(g, c - 4, c - 2, 4, 6, 5, 7, trou)
    paint(g, c - 4, c - 2, 3, 5, 2, 2, grime)                         # dragged hem
    box(g, c - 3, c - 1, 5, 7, 8, 10, trou)                           # knee bent forward
    box(g, c - 3, c - 1, 4, 6, 11, 14, trou)                          # thigh
    g.clear(c - 2, 7, 9, c - 1, 7, 9)                                 # torn knee: a hole
    paint(g, c - 2, c - 1, 6, 6, 9, 9, skin)                          # pallid skin inside it
    paint(g, c - 3, c - 1, 7, 7, 10, 10, trou_s)                      # frayed edge
    box(g, c - 3, c + 3, 4, 6, 13, 15, trou)                          # seat
    box(g, c - 3, c + 3, 3, 7, 15, 15, "black")                       # belt

    # --- torso bowed forward: belly upright, chest and shoulders rolled forward, hump behind
    box(g, c - 3, c + 3, 3, 7, 16, 21, shirt)
    box(g, c - 3, c + 3, 3, 8, 22, 24, shirt)
    box(g, c - 3, c + 3, 4, 9, 25, 27, shirt)
    for x in (c - 3, c + 3):                                          # soften the back edges only
        g.clear(x, 3, 16, x, 3, 24)
        g.clear(x, 4, 25, x, 4, 27)
    box(g, c - 2, c + 2, 2, 2, 22, 26, shirt)                         # rounded upper back
    for x in (c - 2, c + 2):
        g.clear(x, 2, 22, x, 2, 22)
        g.clear(x, 2, 26, x, 2, 26)
    soft_box(g, c - 2, c + 2, 4, 9, 28, 28, shirt)                    # collar slope to the neck
    # untucked shirt tail on the left, tucked on the right
    box(g, c - 3, c - 1, 3, 7, 14, 15, shirt)
    g.clear(c - 3, 3, 14, c - 3, 3, 15)
    g.clear(c - 3, 7, 14, c - 3, 7, 15)
    paint(g, c - 3, c - 1, 3, 7, 14, 14, grime)                       # grimy hem
    paint(g, c, c, 7, 7, 16, 21, shirt_s)                             # button placket
    paint(g, c, c, 8, 8, 22, 24, shirt_s)
    paint(g, c, c, 9, 9, 25, 28, shirt_s)
    paint(g, c - 3, c - 1, 7, 7, 16, 16, grime)                       # dirt where the tail hangs
    paint(g, c + 1, c + 1, 8, 8, 22, 24, grime)                       # dried spill down the chest
    paint(g, c + 2, c + 2, 8, 8, 24, 24, grime)
    paint(g, c + 1, c + 1, 9, 9, 25, 25, grime)
    paint(g, c + 3, c + 3, 4, 6, 16, 20, shirt_s)                     # side crease
    # loosened tie: knot pulled left, blade hanging free of the concave belly
    g.set(c - 1, 10, 28, "maroon_dark")
    box(g, c - 1, c - 1, 10, 10, 20, 27, "maroon_dark")
    g.set(c - 1, 10, 20, "maroon")

    # --- arms hanging forward from the rolled shoulders; left shoulder dropped
    for s, drop in ((-1, 1), (1, 0)):
        xa0, xa1 = sorted((c + s * 4, c + s * 5))
        box(g, xa0, xa1, 5, 6, 21 - drop, 26 - drop, shirt)
        g.clear(c + s * 5, 5, 26 - drop, c + s * 5, 6, 26 - drop)
        box(g, xa0, xa1, 6, 7, 16 - drop, 20 - drop, shirt)            # forearm, forward
        paint(g, xa0, xa1, 6, 7, 16 - drop, 16 - drop, grime)           # grimy cuff
        hand(g, c + s * 4, c + s * 5, 7, 15 - drop, skin, skin_s)
    g.clear(c - 3, 4, 27, c - 3, 9, 27)                                # dropped left shoulder
    paint(g, c - 3, c - 3, 4, 9, 26, 26, shirt_s)

    # --- neck jutting forward out of an open collar, head low and ahead of the chest
    box(g, c - 1, c + 1, 6, 9, 29, 29, skin)
    box(g, c - 1, c + 1, 7, 8, 30, 30, skin)
    for x in (c - 2, c + 2):
        box(g, x, x, 6, 9, 29, 29, shirt)                              # collar points
    hy = 8                                                             # back of the head
    box(g, c - 1, c + 1, hy, hy + 3, 30, 34, skin)
    for s in (-1, 1):
        box(g, c + s * 2, c + s * 2, hy, hy + 2, 31, 33, skin)         # cheeks / temples
        g.set(c + s * 2, hy + 1, 32, "porcelain_mid")                  # ear
        box(g, c + s * 2, c + s * 2, hy, hy, 31, 34, hair)      # hair over the ears
        g.set(c + s * 2, hy + 1, 33, hair)
    face(g, c, hy + 3, 33, skin, skin_s, "stone_dark", nose=False, mouth=False)
    for s in (-1, 1):
        g.set(c + s, hy + 3, 34, skin_s)                        # brow shadow
    g.set(c, hy + 3, 32, "porcelain_mid")                              # nose
    g.set(c, hy + 3, 31, "porcelain_deep")                             # slack mouth
    # thinning hair: greying at the back and sides, scalp showing on top, overgrown nape
    paint(g, c - 2, c + 2, hy, hy, 30, 34, hair)
    box(g, c - 1, c + 1, hy - 1, hy - 1, 31, 34, hair)
    paint(g, c - 1, c + 1, hy, hy + 1, 34, 34, hair)
    box(g, c - 1, c + 1, hy - 1, hy - 1, 30, 30, hair)          # overgrown at the nape
    insert_layer(g, 6)                     # a tall man: shins one cell longer (1.80 m stooped)
    return {"grid": g, "pivot_cells": (c + 0.5, 6.0, 0.0)}


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------
@model("runner",
       story="Out on a morning run when the sirens stopped, and still running in a way: the "
             "same light kit, torn now, worn for weeks. Lean to the point of gauntness, always "
             "tipped forward as if the next step has already started.",
       details=["Whole body tipped forward from the ankles; head low and ahead of the chest",
                "Staggered stance: left foot forward, right heel lifted behind",
                "Thin bare arms bent slightly at the elbow, hands loosely closed",
                "Faded running tee with a ragged hem, the left sleeve torn away and a rip at "
                "the side", "Dark running shorts with a frayed leg", "Worn pale running shoes",
                "Close-cropped dark hair, gaunt face"],
       exclusions=["No gore", "No weapon", "No logos or stripes on the shoes or kit"],
       pivot_note="Between the feet at ground level.",
       silhouette="The leanest, most forward-tilted figure of the set: narrow shoulders, "
                  "stick-thin limbs and a long stride-ready stance.",
       collision_hint=CAPSULE,
       notes=notes("runner", "Still display version of the sprint lean: both feet on the "
                   "ground, staggered. Narrower than the 0.85 m reference (lean build, arms "
                   "close) and deeper (0.60 m) because of the stagger and forward tilt."))
def runner():
    c = 8
    g = Grid(2 * c + 1, 14, 35)
    skin, skin_s = "skin2", "skin2_shadow"
    tee, tee_s = "paint_white_shadow", "porcelain_deep"
    shorts, shorts_s = "navy", "navy_dark"
    shoe, sole = "porcelain_mid", "charcoal"

    # --- left leg: forward, foot flat, knee a little bent
    xl0, xl1 = c - 2, c - 1
    boot(g, xl0 - 1, xl1, 7, 12, 1, shoe, sole)                        # left shoe (3 wide)
    box(g, xl0 - 1, xl1, 7, 8, 2, 2, shoe)                            # heel collar
    box(g, xl0, xl1, 7, 9, 2, 8, skin)                                # shin
    box(g, xl0, xl1, 7, 9, 9, 11, skin)                               # knee forward
    box(g, xl0, xl1, 6, 8, 12, 13, skin)                              # thigh
    # --- right leg: behind, heel lifted, leg slanting back
    xr0, xr1 = c + 1, c + 2
    box(g, xr0, xr1 + 1, 3, 6, 0, 0, sole)                            # ball of the foot
    box(g, xr0, xr1 + 1, 1, 6, 1, 1, shoe)
    g.clear(xr0, 6, 1, xr0, 6, 1)
    g.clear(xr1 + 1, 6, 1, xr1 + 1, 6, 1)
    box(g, xr0, xr1 + 1, 1, 2, 2, 2, shoe)                            # raised heel
    box(g, xr0, xr1, 2, 4, 3, 6, skin)                                # shin
    box(g, xr0, xr1, 3, 5, 7, 10, skin)
    box(g, xr0, xr1, 5, 7, 11, 13, skin)                              # thigh
    box(g, xr0, xr1, 4, 6, 11, 11, skin)
    # --- shorts
    box(g, c - 2, c + 2, 5, 8, 12, 16, shorts)
    box(g, c - 2, c - 1, 6, 9, 11, 12, shorts)                        # left leg opening
    box(g, c + 1, c + 2, 4, 7, 11, 12, shorts)                        # right leg opening
    paint(g, c - 2, c - 1, 9, 9, 11, 11, shorts_s)                    # frayed hem
    paint(g, c - 2, c + 2, 5, 8, 16, 16, shorts_s)                    # waistband

    # --- torso tipped forward: hips over the feet, chest and head ahead
    soft_box(g, c - 2, c + 2, 5, 8, 17, 20, tee)
    soft_box(g, c - 2, c + 2, 6, 9, 21, 24, tee)
    soft_box(g, c - 3, c + 3, 7, 10, 25, 27, tee)                     # shoulders
    box(g, c - 2, c + 2, 7, 9, 23, 24, tee)
    for (x, z) in ((c - 2, 16), (c, 16), (c + 1, 16), (c + 2, 16)):   # ragged hem over shorts
        box(g, x, x, 6, 8, z, z, tee)
    g.set(c - 1, 8, 17, 0)                                            # tear at the hem
    paint(g, c - 2, c - 2, 7, 8, 21, 22, skin)                        # rip at the left side
    paint(g, c + 2, c + 2, 6, 8, 18, 19, tee_s)                       # sweat-dark side
    # collar opening and neck
    box(g, c - 1, c + 1, 8, 10, 28, 28, skin)
    paint(g, c - 1, c + 1, 10, 10, 27, 27, tee_s)

    # --- arms: thin, hanging from the forward shoulders, elbows slightly bent
    for s in (-1, 1):
        xu = c + s * 4
        box(g, xu, xu, 7, 8, 20, 26, skin)                            # upper arm
        g.set(c + s * 3, 8, 26, skin)
        box(g, c + s * 5, c + s * 5, 8, 9, 17, 19, skin)              # forearm out and forward
        box(g, xu, xu, 8, 8, 19, 19, skin)                            # elbow
        box(g, c + s * 5, c + s * 5, 9, 10, 14, 16, skin)             # loosely closed hand
        g.set(c + s * 4, 10, 15, skin)                                # thumb side
        paint(g, c + s * 5, c + s * 5, 9, 10, 14, 14, skin_s)
    box(g, c + 4, c + 4, 7, 8, 24, 26, tee)                           # right sleeve
    paint(g, c + 4, c + 4, 7, 8, 24, 24, tee_s)
    paint(g, c - 3, c - 3, 7, 10, 25, 27, skin)                       # left sleeve torn away
    paint(g, c - 3, c - 3, 7, 10, 25, 25, tee_s)                      # ragged armhole

    # --- head low and forward, close-cropped hair
    hy = 9
    box(g, c - 1, c + 1, 8, 10, 29, 29, skin)                         # neck
    box(g, c - 1, c + 1, hy, hy + 3, 30, 33, skin)
    for s in (-1, 1):
        box(g, c + s * 2, c + s * 2, hy, hy + 2, 31, 32, skin)
        g.set(c + s * 2, hy + 1, 31, skin_s)                          # ear
        box(g, c + s * 2, c + s * 2, hy, hy + 1, 32, 33, "hair_black")
    face(g, c, hy + 3, 32, skin, skin_s, "hair_black", nose=False, mouth=False)
    g.set(c, hy + 3, 31, "skin1_shadow")                              # nose
    g.set(c, hy + 3, 30, skin_s)                                      # mouth
    paint(g, c - 1, c + 1, hy + 3, hy + 3, 33, 33, skin)              # forehead
    paint(g, c - 2, c + 2, hy, hy, 31, 33, "hair_black")              # cropped back and sides
    box(g, c - 1, c + 1, hy, hy + 2, 34, 34, "hair_black")            # cropped crown
    return {"grid": g, "pivot_cells": (c + 0.5, 7.0, 0.0)}


# ---------------------------------------------------------------------------
# Brute
# ---------------------------------------------------------------------------
@model("brute",
       story="A huge man who worked the cutting floor of a meat-packing plant on the edge of "
             "town; he was still in his overalls and heavy leather apron when it happened. "
             "Slow now, heavy-footed, carrying his weight forward.",
       details=["2.1 m tall, broad sloping trapezius and a short thick neck",
                "Heavy barrel chest and belly; arms hanging wide of the body",
                "Thick bare forearms below rolled thermal sleeves; big hands",
                "Faded denim bib overalls, straps over the shoulders",
                "Knee-length dark leather apron with a neck strap and waist ties, a front "
                "pocket, worn pale edges and a rubbed patch where he wipes his hands",
                "Shaved head, short beard, small deep-set eyes",
                "Wide stance in big work boots"],
       exclusions=["No blood, stains of the trade or gore",
                   "No tool or weapon (separate catalog models)"],
       pivot_note="Between the feet at ground level.",
       silhouette="The widest and tallest figure: a heavy trapezoid of shoulders over a "
                  "barrel body, small head pushed forward, a long apron, arms held wide.",
       collision_hint=CAPSULE.replace("0.3 m", "0.45 m"),
       notes=notes("brute", "2.10 m as the reference. Width 0.95 m rather than 1.12 m: the "
                   "heavy arms hang beside the body rather than held out."))
def brute():
    c = 11
    g = Grid(2 * c + 1, 12, 42)
    skin, skin_s = "skin2", "skin2_shadow"
    over, over_d, over_l = "denim_dark", "navy_dark", "denim"
    shirt, shirt_d = "wool", "wool_dark"
    apron, apron_d, apron_l = "leather_deep", "leather_dark", "leather"

    # --- boots and legs: wide stance
    for s in (-1, 1):
        x0, x1 = sorted((c + s * 2, c + s * 5))
        boot(g, x0, x1, 2, 8, 3, "leather_dark", "black")
        paint(g, x0, x1, 2, 8, 1, 1, "leather_deep")                  # welt
        paint(g, x0, x1, 6, 8, 1, 1, "leather")                       # scuffed toe caps
        box(g, x0, x1, 3, 6, 4, 10, over)                             # shins
        paint(g, x0, x1, 3, 6, 4, 4, over_d)                          # turned-up hem
        xt0, xt1 = sorted((c + s * 1, c + s * 4))
        box(g, xt0, xt1, 3, 6, 11, 18, over)                          # thighs
        paint(g, x0, x1, 6, 6, 9, 11, over_l)                         # faded knees
    box(g, c - 4, c + 4, 2, 6, 17, 19, over)                          # seat

    # --- barrel torso: overalls at the waist, thermal shirt above, belly forward
    soft_box(g, c - 5, c + 5, 1, 7, 19, 28, over)
    box(g, c - 4, c + 4, 8, 8, 20, 27, over)                          # belly
    soft_box(g, c - 5, c + 5, 2, 8, 29, 34, shirt)                    # chest, rolled forward
    box(g, c - 4, c + 4, 1, 1, 29, 32, shirt)                         # upper back
    soft_box(g, c - 6, c + 6, 2, 7, 35, 35, shirt)                    # heavy trapezius
    soft_box(g, c - 4, c + 4, 3, 7, 36, 36, shirt)
    paint(g, c - 5, c + 5, 1, 8, 28, 28, over_d)                      # overall bib top edge
    for x in (c - 4, c + 4):                                          # overall straps
        paint(g, x, x, 1, 2, 28, 34, over)
        paint(g, x, x, 2, 7, 35, 35, over)
        paint(g, x, x, 3, 7, 36, 36, over)

    # --- apron: bib on the chest, skirt over the belly hanging to below the knee
    box(g, c - 3, c + 3, 9, 9, 29, 33, apron)                         # bib
    box(g, c - 4, c + 4, 9, 9, 12, 28, apron)                         # skirt over the belly
    box(g, c - 4, c + 4, 9, 9, 12, 12, apron_d)                       # hem
    for x in (c - 4, c + 4):
        paint(g, x, x, 9, 9, 13, 28, apron_l)                         # worn pale edges
    paint(g, c - 2, c + 2, 9, 9, 21, 23, apron_d)                     # front pocket
    paint(g, c - 2, c + 2, 9, 9, 23, 23, apron_l)                     # pocket lip
    paint(g, c + 3, c + 3, 9, 9, 16, 20, apron_d)                     # rubbed where he wipes his hands
    for x in (c - 3, c + 3):                                          # neck strap
        box(g, x, x, 8, 8, 33, 35, apron_d)
        box(g, x, x, 7, 7, 36, 36, apron_d)
        paint(g, x, x, 3, 7, 36, 36, apron_d)
    box(g, c - 3, c + 3, 3, 3, 37, 37, apron_d)                       # behind the neck
    box(g, c - 4, c - 4, 3, 8, 25, 25, apron_d)                       # waist ties round the sides
    box(g, c + 4, c + 4, 3, 8, 25, 25, apron_d)

    # --- arms: thick, hanging wide; sleeves rolled to the elbow, bare forearms, big hands
    for s in (-1, 1):
        xa0, xa1 = sorted((c + s * 6, c + s * 8))
        box(g, xa0, xa1, 3, 6, 27, 34, shirt)                         # upper arm (deltoid)
        g.clear(c + s * 8, 3, 34, c + s * 8, 6, 34)                   # rounded shoulder
        paint(g, xa0, xa1, 3, 6, 27, 27, shirt_d)                     # rolled sleeve
        xf0, xf1 = sorted((c + s * 7, c + s * 9))
        box(g, xf0, xf1, 4, 6, 21, 26, skin)                          # forearm
        xw0, xw1 = sorted((c + s * 7, c + s * 8))
        box(g, xw0, xw1, 4, 6, 19, 20, skin)                          # wrist
        box(g, xa0, xa1, 4, 6, 26, 26, skin)                          # elbow
        box(g, xf0, xf1, 4, 7, 15, 18, skin)                          # big hand
        g.clear(c + s * 7, 7, 15, c + s * 7, 7, 16)
        paint(g, xf0, xf1, 4, 7, 15, 15, skin_s)                      # curled fingers
        g.clear(c + s * 9, 4, 15, c + s * 9, 7, 15)

    # --- small head sunk into the trapezius, pushed forward; beard, deep-set eyes, shaved scalp
    box(g, c - 2, c + 2, 3, 5, 37, 37, skin)                          # thick neck behind the jaw
    hy = 5
    box(g, c - 1, c + 1, hy, hy + 4, 37, 41, skin)
    for s in (-1, 1):
        box(g, c + s * 2, c + s * 2, hy, hy + 3, 37, 40, skin)        # wide jaw and cheeks
        box(g, c + s * 2, c + s * 2, hy + 1, hy + 2, 41, 41, skin)    # rounded skull
        g.set(c + s * 2, hy + 1, 39, skin_s)                          # ear
    face(g, c, hy + 4, 40, skin, skin_s, "hair_black", nose=False, mouth=False)
    g.set(c, hy + 4, 39, "skin1_shadow")                              # nose
    paint(g, c - 2, c + 2, hy + 1, hy + 4, 37, 37, "hair_brown")      # short beard
    paint(g, c - 2, c + 2, hy + 2, hy + 4, 38, 38, "hair_brown")
    g.set(c, hy + 4, 38, skin_s)                                      # mouth in the beard
    paint(g, c - 2, c + 2, hy, hy + 3, 41, 41, skin_s)                # shaved scalp
    return {"grid": g, "pivot_cells": (c + 0.5, 5.5, 0.0)}


# ---------------------------------------------------------------------------
# Suicide bomber
# ---------------------------------------------------------------------------
@model("suicide_bomber",
       story="Someone who strapped a scavenged hazard rig over their hoodie and walked toward "
             "the walls people had built. The kit is improvised and fictional: striped "
             "canisters on a back frame and a dead warning beacon, meant to be seen coming.",
       details=["Hood up, face in shadow, head slightly lowered",
                "Bulky padded vest over the hoodie with generic packets and pouches and two "
                "plain wire runs (one dark red, one black) on the surface",
                "Steel back frame with two hazard-striped canisters and an unlit warning "
                "beacon on a short mast above the head (the gameplay telegraph)",
                "Jeans and worn trainers; arms held out from the body by the vest"],
       exclusions=["Fictional hazard rig only: no realistic explosive, detonator, switch, "
                   "timer or wiring detail; nothing instructional",
                   "No insignia, slogans or text", "Nothing in the hands"],
       pivot_note="Between the feet at ground level.",
       silhouette="Bulky vested torso, a hooded head, two frame rails and canisters showing "
                  "behind the shoulders and a beacon mast rising above the hood.",
       collision_hint=CAPSULE,
       notes=notes("suicide_bomber", "1.75 m figure; the beacon mast brings the total to "
                   "1.90 m (reference 1.88 m). The back frame adds depth (0.55 m); arms rest "
                   "against the vest, so width is 0.75 m rather than 0.94 m."))
def suicide_bomber():
    c = 9
    g = Grid(2 * c + 1, 13, 38)
    hood, hood_d = "concrete_dark", "concrete_deep"
    vest, vest_d = "olive_dark", "algae_dark"
    jeans, jeans_d = "denim_dark", "navy_dark"
    skin, skin_s = "skin1_shadow", "skin2_shadow"
    YB = 4                                                            # back of the vest

    # --- trainers and jeans
    for s in (-1, 1):
        x0, x1 = sorted((c + s * 2, c + s * 4))
        boot(g, x0, x1, YB + 1, YB + 6, 1, "concrete_hi", "black")
        box(g, x0, x1, YB + 1, YB + 2, 2, 2, "concrete_hi")           # heel collar
        box(g, x0, x1, YB + 2, YB + 4, 2, 8, jeans)                   # shins
        paint(g, x0, x1, YB + 2, YB + 4, 2, 2, jeans_d)               # frayed hem
        x0t, x1t = sorted((c + s * 1, c + s * 3))
        box(g, x0t, x1t, YB + 2, YB + 4, 9, 15, jeans)                # thighs
    paint(g, c - 4, c - 2, YB + 4, YB + 4, 8, 9, "denim")             # worn knee
    box(g, c - 3, c + 3, YB + 2, YB + 4, 13, 15, jeans)               # seat

    # --- hoodie torso, vest over it
    soft_box(g, c - 3, c + 3, YB + 1, YB + 5, 14, 27, hood)
    paint(g, c - 3, c + 3, YB + 1, YB + 5, 14, 14, hood_d)            # ribbed hem
    soft_box(g, c - 4, c + 4, YB, YB + 6, 17, 27, vest)               # padded vest
    paint(g, c - 4, c + 4, YB, YB + 6, 17, 17, vest_d)                # bound lower edge
    paint(g, c, c, YB + 6, YB + 6, 18, 27, vest_d)                    # front closure
    for x in (c - 3, c + 3):                                          # vest shoulder pads
        box(g, x - 1 if x < c else x, x if x < c else x + 1, YB + 1, YB + 5, 28, 28, vest)
    # generic packets and pouches (plain blocks, two rows each side of the front closure)
    pouches = [(-4, -2, 19, 21, "khaki"), (-4, -2, 23, 25, "card_dark"),
               (2, 4, 19, 21, "card_dark"), (2, 4, 23, 25, "khaki")]
    for (a, b, z0, z1, col) in pouches:
        box(g, c + a, c + b, YB + 7, YB + 7, z0, z1, col)
        paint(g, c + a, c + b, YB + 7, YB + 7, z1, z1, "khaki_dark")  # flap
    # two plain wire runs on the surface
    paint(g, c - 2, c - 2, YB + 7, YB + 7, 20, 24, "signal_red_dark")
    paint(g, c - 3, c - 3, YB + 6, YB + 6, 22, 22, "signal_red_dark")
    paint(g, c + 2, c + 2, YB + 7, YB + 7, 20, 24, "black")
    paint(g, c + 3, c + 3, YB + 6, YB + 6, 22, 22, "black")
    paint(g, c - 4, c - 4, YB, YB + 6, 26, 26, "black")               # cable round the left side

    # --- back frame with striped canisters and an unlit beacon on a mast
    for x0 in (c - 3, c + 1):
        box(g, x0, x0 + 2, 1, 3, 18, 29, "hazard_yellow_dark")
        for z in (19, 22, 25, 28):
            paint(g, x0, x0 + 2, 1, 3, z, z, "charcoal")             # hazard bands
        box(g, x0, x0 + 2, 1, 3, 30, 30, "steel")                     # caps
        g.set(x0 + 1, 2, 31, "steel_dark")
    for x in (c - 4, c + 4):                                          # frame rails
        box(g, x, x, 2, 3, 16, 31, "steel_dark")
    box(g, c - 4, c + 4, 3, 3, 17, 17, "steel_dark")                  # cross bars
    box(g, c - 4, c + 4, 3, 3, 31, 31, "steel_dark")
    paint(g, c - 3, c + 3, 1, 3, 24, 24, "steel_dark")                # clamp band
    box(g, c, c, 3, 3, 32, 34, "steel_dark")                          # mast
    box(g, c - 1, c + 1, 2, 4, 35, 35, "black")                       # beacon base
    box(g, c - 1, c + 1, 2, 4, 36, 36, "lamp_red")                    # unlit lens
    g.set(c, 3, 37, "black")                                          # cap

    # --- arms held out by the vest bulk
    for s in (-1, 1):
        xa0, xa1 = sorted((c + s * 5, c + s * 6))
        box(g, xa0, xa1, YB + 2, YB + 3, 21, 27, hood)
        g.clear(c + s * 6, YB + 2, 27, c + s * 6, YB + 3, 27)
        xf0, xf1 = sorted((c + s * 6, c + s * 7))
        box(g, xf0, xf1, YB + 2, YB + 3, 16, 20, hood)
        paint(g, xf0, xf1, YB + 2, YB + 3, 16, 16, hood_d)            # cuff
        hand(g, c + s * 6, c + s * 7, YB + 2, 15, skin, skin_s)

    # --- hood up, face set back in its shadow
    soft_box(g, c - 2, c + 2, YB + 1, YB + 5, 28, 29, hood)            # hood drape on the shoulders
    soft_box(g, c - 2, c + 2, YB + 1, YB + 6, 30, 33, hood)
    soft_box(g, c - 2, c + 2, YB + 1, YB + 5, 34, 34, hood)
    g.clear(c - 1, YB + 6, 30, c + 1, YB + 6, 33)                     # face opening
    box(g, c - 1, c + 1, YB + 5, YB + 5, 30, 33, skin)                # face, one cell back
    box(g, c - 2, c - 2, YB + 6, YB + 6, 30, 33, hood_d)              # hood rim
    box(g, c + 2, c + 2, YB + 6, YB + 6, 30, 33, hood_d)
    box(g, c - 1, c + 1, YB + 6, YB + 6, 33, 33, hood_d)              # brim over the brow
    for s in (-1, 1):
        g.set(c + s, YB + 5, 32, "hair_black")                        # eyes in shadow
    g.set(c, YB + 5, 30, skin_s)                                      # mouth
    g.set(c, YB + 5, 33, skin_s)                                      # brow shadow
    paint(g, c - 1, c + 1, YB + 5, YB + 5, 28, 29, hood_d)            # hood throat shadow
    return {"grid": g, "pivot_cells": (c + 0.5, YB + 4.0, 0.0)}
