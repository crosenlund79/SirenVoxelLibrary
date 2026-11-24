"""Claude's small voxel kit for SirenVoxelLibrary.

Creator: Claude. Used only by the Claude_ generators in tools/claude/models/.
Contains:
  * PALETTE  - the shared Claude pilot palette, laid out as one material ramp
               per 8-swatch row so it reads cleanly in MagicaVoxel's palette grid.
  * Grid     - a numpy voxel canvas with a handful of drawing primitives.
  * write_vox / read_vox - MagicaVoxel VOX v150 (SIZE / XYZI / RGBA) I/O.

Library convention (docs/VOXEL_ART_BIBLE.md): X = right, Y = front, Z = up.
Grid index 0 means empty; 1..255 are palette indices (MagicaVoxel style).
"""
from __future__ import annotations

import math
import struct
from pathlib import Path

import numpy as np

# ---------------------------------------------------------------------------
# Palette: rows of up to 8 swatches; each row is one material family, light->dark.
# Anchor colours from the art bible are marked (A).
# ---------------------------------------------------------------------------
_ROWS: list[list[tuple[str, str]]] = [
    # 1-8 interior pine / workshop timber
    [("pine_hi", "#CDA77D"), ("pine_light", "#BC9670"),  # (A) warm pale wood
     ("pine_mid", "#AA8562"), ("pine_aged", "#967455"),  # (A) aged pine
     ("pine_dark", "#7D5F45"), ("wood_stain", "#5E4839"),  # (A) dark stained wood
     ("wood_deep", "#46362B"), ("sawdust", "#D6C19C")],
    # 9-16 weathered outdoor timber (silvered)
    [("wgrey_hi", "#A59E91"), ("wgrey", "#8B8478"), ("wgrey_mid", "#766F64"),
     ("wgrey_dark", "#5E5850"), ("wgrey_deep", "#46423C"), ("wgrey_green", "#6C705F"),
     ("wgrey_warm", "#94806A"), ("wgrey_wet", "#524C45")],
    # 17-24 pine bark and exposed dead wood
    [("bark_hi", "#8D837A"), ("bark", "#73695F"), ("bark_mid", "#5F564E"),
     ("bark_dark", "#4B443E"), ("bark_deep", "#37322E"), ("snag_light", "#BFB39F"),
     ("snag", "#A79B87"), ("snag_dark", "#8A7F6E")],
    # 25-32 tree accents
    [("break_fresh", "#C9B08A"), ("needle_olive", "#6E7251"), ("needle_dry", "#877A53"),
     ("needle_rust", "#86684C"), ("needle_dark", "#50573F"), ("lichen", "#8E9979"),
     ("soil", "#4F453C"), ("soil_dark", "#3B342E")],
    # 33-40 steel
    [("steel_hi", "#ADB4B2"),  # (A) pale metal highlight
     ("steel_light", "#8C9496"), ("steel", "#687072"),  # (A) worn steel
     ("steel_dark", "#4F5658"), ("charcoal", "#363C3D"),  # (A) deep charcoal metal
     ("black", "#252A2B"),  # (A) near-black shadow
     ("galv_hi", "#B5BAB5"), ("galv", "#989E9A")],
    # 41-48 cast iron
    [("iron_edge", "#5B605F"), ("iron", "#3C4040"), ("iron_dark", "#2E3232"),
     ("iron_deep", "#222626"), ("soot", "#1B1D1D"), ("galv_dark", "#7A807C"),
     ("iron_warm", "#4A4440"), ("iron_blue", "#3D4447")],
    # 49-56 rust and brass
    [("rust_hi", "#C28052"), ("rust", "#B36E44"),  # (A) rust / orange accent
     ("rust_dark", "#8B5336"), ("rust_deep", "#674230"), ("brass_hi", "#C2A468"),
     ("brass", "#A3874E"), ("brass_dark", "#786439"), ("copper", "#9A6448")],
    # 57-64 fire
    [("ember_hot", "#E8A85A"), ("ember", "#D3843F"), ("ember_dark", "#9F4F2C"),
     ("coal", "#4A2E26"), ("ash", "#8F8A83"), ("ash_dark", "#66615C"),
     ("char", "#2B2522"), ("ash_light", "#B0ABA3")],
    # 65-72 muted green paint / plastic
    [("green_hi", "#7C9385"), ("green_light", "#69806F"), ("green", "#566C60"),  # (A)
     ("green_dark", "#46584F"), ("green_deep", "#36443D"), ("green_faded", "#8A9A8C"),
     ("algae", "#5D6A4E"), ("algae_dark", "#4A553E")],
    # 73-80 cold blue-grey and water
    [("bluegrey_hi", "#8698A1"), ("bluegrey", "#687A82"),  # (A)
     ("bluegrey_dark", "#53636A"), ("bluegrey_deep", "#404C52"), ("water_hi", "#5E747B"),
     ("water", "#3E5359"), ("water_dark", "#2C3B40"), ("mesh", "#4B5254")],
    # 81-88 brick red, olive canvas, ochre accents
    [("red_hi", "#B26D5C"), ("red", "#9A594B"),  # (A) dusty brick red
     ("red_dark", "#7B463B"), ("red_deep", "#5C352D"), ("olive_hi", "#8E926A"),
     ("olive", "#777B55"),  # (A) olive canvas
     ("olive_dark", "#5F6244"), ("ochre", "#A98A4C")],
    # 89-96 cream fabric and plaster
    [("cream_hi", "#E4DCCB"), ("cream", "#D7CDB9"),  # (A) soft cream fabric
     ("cream_mid", "#C7BCA6"), ("cream_shadow", "#B3A791"), ("cream_deep", "#988C77"),
     ("plaster", "#CCC5B6"),  # (A) warm plaster
     ("paper", "#DDD6C6"), ("ochre_dark", "#826A3A")],
    # 97-104 desaturated blue fabric
    [("blue_hi", "#8497A4"), ("blue", "#697D8B"),  # (A) desaturated blue fabric
     ("blue_mid", "#5D707D"), ("blue_dark", "#4E5F6B"), ("blue_deep", "#3E4C56"),
     ("blue_seam", "#566874"), ("wool", "#9A8E7C"), ("wool_dark", "#7E7363")],
    # 105-112 concrete / stone
    [("concrete_hi", "#A7A8A0"), ("concrete", "#90918A"),  # (A) weathered concrete
     ("concrete_dark", "#76776F"), ("concrete_deep", "#5D5E58"), ("stone", "#827E76"),
     ("stone_dark", "#68645E"), ("moss", "#646C4F"), ("moss_dark", "#4E5540")],
]

# ---------------------------------------------------------------------------
# Palette v2 (catalog): rows 15-29 append new material families. Rows 1-14 are the
# pilot palette and never change, so pilot colours keep their exact indices.
# ---------------------------------------------------------------------------
_ROWS_V2: list[list[tuple[str, str]]] = [
    # 113-120 ceramic, enamel and old "almond" appliances
    [("porcelain_hi", "#EAE7DF"), ("porcelain", "#DAD6CC"), ("porcelain_mid", "#C5C0B5"),
     ("porcelain_shadow", "#ABA69B"), ("porcelain_deep", "#8D897F"), ("almond", "#CFC5AC"),
     ("almond_dark", "#AFA58D"), ("chrome", "#C4C9C7")],
    # 121-128 glass, screens, mirror, lamp glass (opaque stylisation, no transparency)
    [("glass_hi", "#A7BDC2"), ("glass", "#829A9F"), ("glass_dark", "#5E7378"),
     ("glass_deep", "#42535A"), ("screen", "#262C2F"), ("screen_sheen", "#48555A"),
     ("mirror", "#BAC6C6"), ("bulb_warm", "#E2CF9C")],
    # 129-136 upholstery: slate (sofa) and mauve (bedding) - matches the game's prop colours
    [("slate_hi", "#74848B"), ("slate", "#5E6D74"), ("slate_dark", "#4B585E"),
     ("slate_deep", "#3A4449"), ("mauve_hi", "#BFA3A0"), ("mauve", "#A98C89"),
     ("mauve_dark", "#8C7270"), ("mauve_deep", "#6C5856")],
    # 137-144 upholstery: mustard and terracotta / rust fabric
    [("mustard_hi", "#C3A05A"), ("mustard", "#AA8847"), ("mustard_dark", "#876B38"),
     ("mustard_deep", "#63502C"), ("terra_hi", "#AA6E52"), ("terra", "#925A41"),
     ("terra_dark", "#744733"), ("terra_deep", "#573628")],
    # 145-152 kitchen sage and faded teal paint
    [("sage_hi", "#93A193"), ("sage", "#7A887B"), ("sage_dark", "#637064"),
     ("sage_deep", "#4C574D"), ("teal_hi", "#6F8C8A"), ("teal", "#587372"),
     ("teal_dark", "#445A59"), ("teal_deep", "#334443")],
    # 153-160 leather and cardboard
    [("leather_hi", "#94694B"), ("leather", "#7A553C"), ("leather_dark", "#5E402E"),
     ("leather_deep", "#432E22"), ("card_hi", "#C2A47A"), ("card", "#A88A62"),
     ("card_dark", "#8A714F"), ("card_deep", "#6A573E")],
    # 161-168 skin tones (three ramps) and a pallid tone for the psychos
    [("skin1_hi", "#DDB99E"), ("skin1", "#C9A085"), ("skin1_shadow", "#AC846B"),
     ("skin2", "#A97A5D"), ("skin2_shadow", "#8B6249"), ("skin3", "#74513D"),
     ("skin3_shadow", "#5A3E2F"), ("skin_pallid", "#B9AFA0")],
    # 169-176 hair and everyday clothing
    [("hair_black", "#2A2524"), ("hair_brown", "#594230"), ("hair_grey", "#8C8781"),
     ("denim_hi", "#6A7C8E"), ("denim", "#536476"), ("denim_dark", "#414F5E"),
     ("khaki", "#9C8D6E"), ("khaki_dark", "#7B6F57")],
    # 177-184 living leaves and grass
    [("leaf_hi", "#869B63"), ("leaf", "#6F8551"), ("leaf_mid", "#5C7044"),
     ("leaf_dark", "#495B37"), ("leaf_deep", "#37452B"), ("grass_hi", "#94A066"),
     ("grass", "#7B8851"), ("grass_dry", "#A79D6B")],
    # 185-192 healthy conifer greens, dead leaves and twigs
    [("conifer_hi", "#627D5C"), ("conifer", "#4E6849"), ("conifer_mid", "#41583F"),
     ("conifer_dark", "#344835"), ("conifer_deep", "#283629"), ("dead_leaf", "#9C7F55"),
     ("dead_leaf_dark", "#7A6243"), ("twig", "#6A5A47")],
    # 193-200 asphalt, road paint, kerbs and gravel
    [("asphalt_hi", "#626463"), ("asphalt", "#4F5151"), ("asphalt_dark", "#3F4142"),
     ("asphalt_deep", "#313334"), ("line_white", "#CDCBC1"), ("line_yellow", "#BFA352"),
     ("curb", "#A09F97"), ("gravel", "#8C877D")],
    # 201-208 signal accents - rare and purposeful (medical cross, hazard, cones, lightbars)
    [("signal_red", "#A8463B"), ("signal_red_dark", "#7E3229"), ("hazard_yellow", "#C8A63F"),
     ("hazard_yellow_dark", "#9A7E2D"), ("safety_orange", "#C26C36"),
     ("safety_orange_dark", "#91512A"), ("lamp_blue", "#4E78A3"), ("lamp_red", "#B04B43")],
    # 209-216 vehicle and painted-metal finishes
    [("paint_white", "#D0CEC6"), ("paint_white_shadow", "#B0AEA6"), ("navy", "#3E4A5B"),
     ("navy_dark", "#2F3846"), ("maroon", "#703F3C"), ("maroon_dark", "#57302E"),
     ("beige", "#AA9D80"), ("beige_dark", "#8B8068")],
    # 217-224 roofing and siding (construction and map buildings)
    [("roof_hi", "#6E7274"), ("roof", "#5A5E61"), ("roof_dark", "#474B4E"),
     ("shingle_brown", "#6B5A4D"), ("siding_cream", "#C9C2AE"), ("siding_blue", "#8D9DA2"),
     ("siding_sage", "#94A091"), ("siding_yellow", "#BBAA80")],
    # 225-232 plastics, labels and foil
    [("bottle_hi", "#A3BBC4"), ("bottle", "#7F9CA8"), ("bottle_cap", "#4E6E86"),
     ("label_red", "#9C4A3A"), ("label_green", "#5F7752"), ("label_blue", "#556F8A"),
     ("label_cream", "#D9CFB3"), ("foil", "#9EA3A1")],
]


def _build_palette(rows):
    roles: dict[str, int] = {}
    rgb: list[tuple[int, int, int]] = []
    for r, row in enumerate(rows):
        assert len(row) <= 8
        for c in range(8):
            idx = r * 8 + c + 1
            if c < len(row):
                name, hexv = row[c]
                assert name not in roles, name
                roles[name] = idx
                rgb.append(tuple(int(hexv[i:i + 2], 16) for i in (1, 3, 5)))
            else:  # unused slot in a material row: neutral grey
                rgb.append((128, 128, 128))
    # Remaining slots: a smooth neutral ramp so the palette stays usable in an editor.
    while len(rgb) < 255:
        k = len(rgb) - len(rows) * 8
        n = 255 - len(rows) * 8
        v = int(round(250 - 230 * k / max(1, n - 1)))
        rgb.append((v, v, v))
    pal = np.array([(0, 0, 0)] + rgb, dtype=np.uint8)  # index 0 = empty
    assert pal.shape == (256, 3)
    return roles, pal


# v1: the pilot palette (Claude_pilot_001 files embed exactly this).
_ROLES_V1, PALETTE_RGB_V1 = _build_palette(_ROWS)
# v2: the catalog palette = v1 rows + the new rows. Default for every new model.
PALETTE_ROLES, PALETTE_RGB = _build_palette(_ROWS + _ROWS_V2)
assert np.array_equal(PALETTE_RGB[1:113], PALETTE_RGB_V1[1:113])
assert len({tuple(c) for c in PALETTE_RGB[1:]}) == 255, "palette v2 colours must be unique"
PALETTES = {1: PALETTE_RGB_V1, 2: PALETTE_RGB}


def P(name: str) -> int:
    """Palette index for a named role."""
    return PALETTE_ROLES[name]


def role_of(index: int) -> str | None:
    for k, v in PALETTE_ROLES.items():
        if v == index:
            return k
    return None


def palette_table() -> list[dict]:
    """All named palette roles (index, role, hex) - for documentation."""
    return [{"index": i, "role": k, "hex": "#%02X%02X%02X" % tuple(PALETTE_RGB[i])}
            for k, i in sorted(PALETTE_ROLES.items(), key=lambda kv: kv[1])]


def hash01(*args: int, seed: int = 0) -> float:
    """Deterministic integer hash -> [0, 1). Used for controlled, sparse wear decisions."""
    h = (seed * 0x9E3779B1) & 0xFFFFFFFF
    for a in args:
        h ^= (int(a) * 0x85EBCA6B) & 0xFFFFFFFF
        h = ((h << 13) | (h >> 19)) & 0xFFFFFFFF
        h = (h * 5 + 0xE6546B64) & 0xFFFFFFFF
    h ^= h >> 16
    h = (h * 0x7FEB352D) & 0xFFFFFFFF
    h ^= h >> 15
    return (h & 0xFFFFFF) / float(1 << 24)


# ---------------------------------------------------------------------------
# Grid
# ---------------------------------------------------------------------------
class Grid:
    """Voxel canvas. Coordinates are integer cells, (x, y, z), inclusive ranges."""

    def __init__(self, nx: int, ny: int, nz: int):
        self.v = np.zeros((nx, ny, nz), dtype=np.uint8)

    @property
    def shape(self):
        return self.v.shape

    def inside(self, x, y, z) -> bool:
        nx, ny, nz = self.v.shape
        return 0 <= x < nx and 0 <= y < ny and 0 <= z < nz

    def set(self, x, y, z, c):
        if self.inside(x, y, z):
            self.v[x, y, z] = P(c) if isinstance(c, str) else c

    def get(self, x, y, z) -> int:
        return int(self.v[x, y, z]) if self.inside(x, y, z) else 0

    def _sl(self, a0, a1, n):
        lo, hi = min(a0, a1), max(a0, a1)
        return slice(max(lo, 0), min(hi + 1, n))

    def box(self, x0, y0, z0, x1, y1, z1, c):
        nx, ny, nz = self.v.shape
        self.v[self._sl(x0, x1, nx), self._sl(y0, y1, ny), self._sl(z0, z1, nz)] = (
            P(c) if isinstance(c, str) else c)

    def clear(self, x0, y0, z0, x1, y1, z1):
        self.box(x0, y0, z0, x1, y1, z1, 0)

    def paint(self, x0, y0, z0, x1, y1, z1, c):
        """Recolour only occupied cells in a box."""
        nx, ny, nz = self.v.shape
        s = (self._sl(x0, x1, nx), self._sl(y0, y1, ny), self._sl(z0, z1, nz))
        sub = self.v[s]
        sub[sub > 0] = P(c) if isinstance(c, str) else c

    def paint_cell(self, x, y, z, c):
        if self.get(x, y, z):
            self.set(x, y, z, c)

    def line(self, p0, p1, c, thick: int = 0):
        """3D line between cell centres (inclusive), optional cubic thickness radius."""
        p0 = np.array(p0, float)
        p1 = np.array(p1, float)
        n = int(max(abs(p1 - p0).max(), 1) * 2) + 1
        last = None
        for t in np.linspace(0.0, 1.0, n):
            q = tuple(int(math.floor(v + 0.5)) for v in p0 + (p1 - p0) * t)
            if q == last:
                continue
            last = q
            if thick:
                self.box(q[0] - thick, q[1] - thick, q[2] - thick,
                         q[0] + thick, q[1] + thick, q[2] + thick, c)
            else:
                self.set(*q, c)

    def disc_cells(self, cx: float, cy: float, r: float):
        """Cells (i, j) whose centres fall inside a circle (centre in cell units)."""
        out = []
        for i in range(int(math.floor(cx - r)) - 1, int(math.ceil(cx + r)) + 2):
            for j in range(int(math.floor(cy - r)) - 1, int(math.ceil(cy + r)) + 2):
                if (i + 0.5 - cx) ** 2 + (j + 0.5 - cy) ** 2 <= r * r:
                    out.append((i, j))
        return out

    def cyl_z(self, cx, cy, r, z0, z1, c, wall: float | None = None):
        """Vertical cylinder; if wall is given, only cells within `wall` of the rim."""
        for (i, j) in self.disc_cells(cx, cy, r):
            if wall is not None:
                d = math.hypot(i + 0.5 - cx, j + 0.5 - cy)
                if d < r - wall:
                    continue
            self.box(i, j, z0, i, j, z1, c)

    def ring_cells(self, cx: float, cy: float, r: float):
        """Face-connected outline of a disc: disc cells with any 8-neighbour outside it.
        (A plain 1-cell ring only touches itself diagonally at 45 degrees.)"""
        disc = set(self.disc_cells(cx, cy, r))
        return [(i, j) for (i, j) in disc
                if any((i + di, j + dj) not in disc
                       for di in (-1, 0, 1) for dj in (-1, 0, 1) if di or dj)]

    def count(self) -> int:
        return int(np.count_nonzero(self.v))

    def bounds(self):
        idx = np.argwhere(self.v > 0)
        return idx.min(0), idx.max(0)

    def cropped(self):
        """Return (new Grid cropped to occupancy, offset)."""
        lo, hi = self.bounds()
        g = Grid(*(hi - lo + 1))
        g.v[:] = self.v[lo[0]:hi[0] + 1, lo[1]:hi[1] + 1, lo[2]:hi[2] + 1]
        return g, lo


# ---------------------------------------------------------------------------
# MagicaVoxel VOX I/O (version 150: MAIN > SIZE, XYZI, RGBA)
# ---------------------------------------------------------------------------
def _chunk(cid: bytes, content: bytes, children: bytes = b"") -> bytes:
    return cid + struct.pack("<ii", len(content), len(children)) + content + children


def write_vox(path, grid: Grid, palette_rgb: np.ndarray = PALETTE_RGB) -> None:
    v = grid.v
    nx, ny, nz = v.shape
    if max(nx, ny, nz) > 256:
        raise ValueError("VOX single-model limit is 256 cells per axis")
    xs, ys, zs = np.nonzero(v)
    order = np.lexsort((xs, ys, zs))  # deterministic z, y, x ordering
    xs, ys, zs = xs[order], ys[order], zs[order]
    cs = v[xs, ys, zs]
    xyzi = struct.pack("<i", len(xs)) + np.stack([xs, ys, zs, cs], 1).astype(np.uint8).tobytes()
    rgba = np.zeros((256, 4), np.uint8)
    rgba[:255, :3] = palette_rgb[1:256]  # file entry i -> palette index i + 1
    rgba[:255, 3] = 255
    children = (_chunk(b"SIZE", struct.pack("<iii", nx, ny, nz)) +
                _chunk(b"XYZI", xyzi) +
                _chunk(b"RGBA", rgba.tobytes()))
    data = b"VOX " + struct.pack("<i", 150) + _chunk(b"MAIN", b"", children)
    Path(path).write_bytes(data)


def read_vox(path):
    """Minimal strict reader. Returns dict(size, voxels[N,4] uint8, palette[256,4], chunks)."""
    b = Path(path).read_bytes()
    if b[:4] != b"VOX ":
        raise ValueError("not a VOX file")
    version = struct.unpack_from("<i", b, 4)[0]
    if b[8:12] != b"MAIN":
        raise ValueError("missing MAIN chunk")
    main_content, main_children = struct.unpack_from("<ii", b, 12)
    pos = 20 + main_content
    end = pos + main_children
    if end != len(b):
        raise ValueError(f"MAIN children size {main_children} does not match file length")
    out = {"version": version, "chunks": [], "size": None, "voxels": None, "palette": None}
    while pos < end:
        cid = b[pos:pos + 4]
        n, m = struct.unpack_from("<ii", b, pos + 4)
        content = b[pos + 12:pos + 12 + n]
        out["chunks"].append(cid.decode("ascii"))
        if cid == b"SIZE":
            out["size"] = struct.unpack("<iii", content)
        elif cid == b"XYZI":
            cnt = struct.unpack_from("<i", content)[0]
            if len(content) != 4 + 4 * cnt:
                raise ValueError("XYZI length mismatch")
            out["voxels"] = np.frombuffer(content[4:], np.uint8).reshape(cnt, 4).copy()
        elif cid == b"RGBA":
            raw = np.frombuffer(content, np.uint8).reshape(256, 4)
            pal = np.zeros((256, 4), np.uint8)
            pal[1:] = raw[:255]
            out["palette"] = pal
        pos += 12 + n + m
    if pos != end:
        raise ValueError("chunk walk overran MAIN")
    return out


def vox_to_grid(info) -> np.ndarray:
    nx, ny, nz = info["size"]
    g = np.zeros((nx, ny, nz), np.uint8)
    vx = info["voxels"]
    g[vx[:, 0], vx[:, 1], vx[:, 2]] = vx[:, 3]
    return g


# ---------------------------------------------------------------------------
# Extra drawing helpers (catalog). Methods are attached to Grid so generators
# can call g.cyl_x(...), g.ellipsoid(...), etc. All ranges are inclusive cells.
# ---------------------------------------------------------------------------
def _cyl_axis(self, axis: int, ca: float, cb: float, r: float, t0: int, t1: int, c,
              wall: float | None = None):
    """Cylinder along `axis` (0=x, 1=y, 2=z); (ca, cb) is the centre in the other two
    axes (in increasing axis order), in cell units (use n + 0.5 for a cell centre)."""
    lo, hi = min(t0, t1), max(t0, t1)
    for (i, j) in self.disc_cells(ca, cb, r):
        if wall is not None and math.hypot(i + 0.5 - ca, j + 0.5 - cb) < r - wall:
            continue
        if axis == 0:
            self.box(lo, i, j, hi, i, j, c)
        elif axis == 1:
            self.box(i, lo, j, i, hi, j, c)
        else:
            self.box(i, j, lo, i, j, hi, c)


def _cyl_x(self, cy, cz, r, x0, x1, c, wall=None):
    """Horizontal cylinder along X; centre (cy, cz) in cell units."""
    _cyl_axis(self, 0, cy, cz, r, x0, x1, c, wall)


def _cyl_y(self, cx, cz, r, y0, y1, c, wall=None):
    """Horizontal cylinder along Y; centre (cx, cz) in cell units."""
    _cyl_axis(self, 1, cx, cz, r, y0, y1, c, wall)


def _ellipsoid(self, cx, cy, cz, rx, ry, rz, c, shell: float | None = None, only_empty=False):
    """Ellipsoid centred at (cx, cy, cz) in cell units (cell centres at n + 0.5).
    shell: keep only cells within that normalised thickness of the surface (0..1)."""
    for x in range(int(math.floor(cx - rx)), int(math.ceil(cx + rx)) + 1):
        for y in range(int(math.floor(cy - ry)), int(math.ceil(cy + ry)) + 1):
            for z in range(int(math.floor(cz - rz)), int(math.ceil(cz + rz)) + 1):
                d = (((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - cy) / ry) ** 2 +
                     ((z + 0.5 - cz) / rz) ** 2)
                if d > 1.0:
                    continue
                if shell is not None and d < (1.0 - shell) ** 2:
                    continue
                if only_empty and self.get(x, y, z):
                    continue
                self.set(x, y, z, c)


def _rbox(self, x0, y0, z0, x1, y1, z1, c, r: int = 1):
    """Box whose four vertical edges are chamfered by r cells (softens silhouettes)."""
    self.box(x0, y0, z0, x1, y1, z1, c)
    for k in range(r):
        cut = r - k
        for (xa, xb) in ((x0 + k, x0 + k), (x1 - k, x1 - k)):
            for (ya, yb) in ((y0, y0 + cut - 1), (y1 - cut + 1, y1)):
                self.clear(xa, ya, z0, xb, yb, z1)


def _place(self, other, x, y, z, skip_empty=True):
    """Paste another Grid / ndarray with its minimum corner at (x, y, z)."""
    a = other.v if hasattr(other, "v") else np.asarray(other)
    nx, ny, nz = self.v.shape
    for (i, j, k) in np.argwhere(a > 0) if skip_empty else np.argwhere(np.ones_like(a)):
        X, Y, Z = x + i, y + j, z + k
        if 0 <= X < nx and 0 <= Y < ny and 0 <= Z < nz:
            self.v[X, Y, Z] = a[i, j, k]


def _mirror_x(self, x_mid2: int):
    """Mirror the occupied cells across the plane x = x_mid2 / 2 (in cell-edge units),
    only filling empty target cells. E.g. a model spanning 0..19 uses x_mid2 = 19."""
    for (i, j, k) in np.argwhere(self.v > 0):
        t = x_mid2 - i
        if 0 <= t < self.v.shape[0] and not self.v[t, j, k]:
            self.v[t, j, k] = self.v[i, j, k]


Grid.cyl_x = _cyl_x
Grid.cyl_y = _cyl_y
Grid.ellipsoid = _ellipsoid
Grid.rbox = _rbox
Grid.place = _place
Grid.mirror_x = _mirror_x
