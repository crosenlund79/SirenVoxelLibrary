"""REJECTED block-out, kept only as evidence for the resolution decision.

Claude_rain_collector_basic at the suggested 0.10 m (clean, unribbed variant). Reviewed and
rejected: see docs/specs/survival/Claude_rain_collector_basic.md. Not a library asset.
"""
from voxkit import Grid

BASE_ID = "rain_collector_basic"
CATEGORY = "survival"
NAME = "Basic Rain Collector"
CELL = 0.10

CX, CY = 6.0, 5.0        # tank axis on a cell boundary -> true 8 x 8 circle


def build():
    g = Grid(12, 10, 16)

    # ---------------- stand: silvered fence-post timber -------------------------
    posts = [(1, 0), (10, 0), (1, 8), (10, 8)]
    for (px, py) in posts:
        g.box(px, py, 0, px, py, 4, "wgrey_mid")
    g.box(1, 8, 0, 1, 8, 1, 0)                         # front-left leg cut short ...
    g.box(1, 7, 0, 2, 8, 1, "concrete")                # ... and levelled on a block
    g.paint(1, 7, 1, 2, 7, 1, "concrete_hi")
    g.set(2, 8, 0, "concrete_dark")
    g.box(1, 0, 4, 10, 0, 4, "wgrey_dark")             # back beam
    g.box(1, 8, 4, 10, 8, 4, "wgrey")                  # front beam
    g.box(1, 1, 2, 1, 7, 2, "wgrey_dark")              # side rails
    g.box(10, 1, 2, 10, 7, 2, "wgrey_dark")
    g.box(2, 0, 2, 9, 0, 2, "wgrey_deep")              # back rail
    # pallet-board deck running across, a gap where one board split off
    deck = ["wgrey", "wgrey_hi", "wgrey_mid", "wgrey", None, "wgrey_hi", "wgrey_mid",
            "wgrey", "wgrey_warm"]
    for y, c in enumerate(deck):
        if c:
            g.box(1, y, 5, 10, y, 5, c)
    g.box(2, 4, 5, 9, 4, 5, 0)
    g.box(6, 4, 4, 6, 4, 4, "wgrey_deep")              # joist visible through the gap
    # rust bleeding from nail heads at the beam joins
    for (x, y, z) in [(1, 8, 4), (10, 8, 4), (10, 0, 4)]:
        g.set(x, y, z, "rust_deep")
    # the newer post added to carry the inlet pipe
    g.box(6, 0, 0, 6, 0, 14, "pine_aged")
    g.box(6, 0, 0, 6, 0, 1, "pine_dark")

    # ---------------- tank: rounded shoulders, one moulded rib ------------------
    def ring(z, r, c, wall=1.0):
        g.cyl_z(CX, CY, r, z, z, c, wall=wall)

    ring(6, 4.0, "green_dark", wall=None)
    for z in range(7, 13):
        ring(z, 4.0, "green")
    ring(13, 4.0, "green", wall=None)
    g.cyl_z(CX, CY, 2.6, 14, 14, "green_dark")           # screw lid
    # grime: algae on the lowest band, sun-faded crown
    g.paint(0, 0, 7, 11, 10, 7, "green_dark")
    for (i, j) in g.disc_cells(CX, CY, 4.0):
        if g.get(i, j, 13):
            g.set(i, j, 13, "green_light")
    # ratchet strap lashing the tank to the post
    for (i, j) in g.disc_cells(CX, CY, 4.0):
        if g.get(i, j, 8) and ((i + 0.5 - CX) ** 2 + (j + 0.5 - CY) ** 2) > 2.9 ** 2:
            g.set(i, j, 8, "olive")
    g.set(10, 4, 8, "steel")                             # buckle
    g.set(10, 5, 8, "rust_dark")

    # ---------------- inlet: galvanised pipe from the gutter ---------------------
    g.box(6, 0, 15, 6, 3, 15, "galv")                    # runs forward over the lid
    g.set(6, 0, 15, "galv_dark")                         # coupler = gutter connection end
    g.set(5, 0, 14, "steel_dark")                        # bracket on the post
    g.set(7, 0, 14, "rust_dark")
    g.set(6, 4, 15, "galv_hi")                           # elbow
    g.set(6, 4, 14, "galv")                              # drops into the lid
    g.set(5, 4, 14, "mesh")                              # leaf screen
    g.set(5, 5, 14, "mesh")
    g.set(6, 5, 14, "black")

    # ---------------- outlet tap overhanging the front edge ----------------------
    g.set(6, 9, 7, "brass")                              # valve body
    g.set(6, 9, 8, "red")                                # handle
    g.set(6, 9, 6, "brass_dark")                         # spout
    g.set(5, 8, 5, "wgrey_wet")                          # splash-darkened front board
    g.set(6, 8, 5, "wgrey_wet")

    # ---------------- overflow: grey PVC down the -X side ------------------------
    g.set(1, 6, 12, "concrete_hi")                       # spigot through the tank wall
    g.box(0, 6, 1, 0, 6, 12, "concrete_hi")              # down-pipe
    g.set(0, 6, 12, "steel_light")                       # elbow
    g.set(0, 7, 0, "concrete_hi")                        # shoe turned away from the stand
    g.set(0, 6, 0, "concrete_hi")
    g.set(0, 5, 3, "steel_dark")                         # clip to the stand rail
    g.set(0, 5, 2, "steel_dark")

    return {"grid": g, "cell": CELL, "footprint_cells": ((1, 10), (0, 8)),
            "inlet_connection_cell": (6.5, 0.0, 15.5)}
