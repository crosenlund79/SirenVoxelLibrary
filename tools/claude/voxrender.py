"""Small numpy voxel ray tracer used for Claude's preview images.

It renders the *actual* voxel cells loaded from .vox files (no meshes, no concept
art): orthographic cameras, a soft-shadowed sun, sky occlusion with a crude one-bounce
term, and a seamless studio floor that only shows occlusion. Creator-neutral: it can
render any MagicaVoxel v150 file, so it is usable for side-by-side comparisons.

Dependencies: numpy, Pillow.
"""
from __future__ import annotations

import ctypes
import math
import os
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

# ---------------------------------------------------------------------------
# optional C kernel (falls back to the numpy DDA if gcc is unavailable)
# ---------------------------------------------------------------------------
_HERE = Path(__file__).resolve().parent
_LIB = None


def _load_kernel():
    global _LIB
    if _LIB is not None or os.environ.get("VOXRENDER_NUMPY"):
        return _LIB
    src = _HERE / "vtrace.c"
    out = _HERE / "__pycache__" / "vtrace.so"
    try:
        if not out.exists() or out.stat().st_mtime < src.stat().st_mtime:
            out.parent.mkdir(exist_ok=True)
            subprocess.run(["gcc", "-O3", "-fopenmp", "-shared", "-fPIC", str(src), "-o",
                            str(out), "-lm"], check=True, capture_output=True)
        lib = ctypes.CDLL(str(out))
        P = np.ctypeslib.ndpointer
        lib.vtrace.argtypes = [P(np.uint16, flags="C"), ctypes.c_int, ctypes.c_int, ctypes.c_int,
                               P(np.float64, flags="C"), P(np.float64, flags="C"), ctypes.c_long,
                               ctypes.c_double, P(np.uint8, flags="C"), P(np.float64, flags="C"),
                               P(np.int8, flags="C"), P(np.int8, flags="C"),
                               P(np.uint16, flags="C")]
        lib.vtrace.restype = None
        _LIB = lib
    except Exception:  # pragma: no cover - environment dependent
        _LIB = False
    return _LIB

# ---------------------------------------------------------------------------
# colour helpers
# ---------------------------------------------------------------------------

def srgb_to_lin(c):
    c = np.asarray(c, np.float64) / 255.0
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def lin_to_srgb8(c):
    c = np.clip(c, 0.0, 1.0)
    s = np.where(c <= 0.0031308, c * 12.92, 1.055 * np.power(c, 1 / 2.4) - 0.055)
    return np.clip(np.round(s * 255.0), 0, 255).astype(np.uint8)


def hex_lin(h):
    return srgb_to_lin([int(h[i:i + 2], 16) for i in (1, 3, 5)])


# ---------------------------------------------------------------------------
# scene
# ---------------------------------------------------------------------------
@dataclass
class Item:
    grid: np.ndarray          # (nx, ny, nz) uint8 palette indices, 0 = empty
    palette: np.ndarray       # (256, 3) uint8 sRGB
    cell: float               # metres per cell
    origin: tuple             # world position (m) of the grid's minimum corner
    name: str = ""


def rot_item_z(grid: np.ndarray, quarter_turns: int) -> np.ndarray:
    """Rotate a voxel grid about +Z by 90 degree steps (counter-clockwise seen from above)."""
    return np.rot90(grid, k=quarter_turns % 4, axes=(0, 1)).copy()


class Scene:
    """All items resampled onto one world grid at the finest cell size present."""

    def __init__(self, items: list[Item], base_cell: float | None = None):
        self.items = items
        self.cell = base_cell or min(it.cell for it in items)
        lo = np.array([np.inf] * 3)
        hi = -lo
        for it in items:
            o = np.array(it.origin, float)
            lo = np.minimum(lo, o)
            hi = np.maximum(hi, o + np.array(it.grid.shape) * it.cell)
        lo[2] = 0.0
        self.origin = lo
        dims = np.ceil((hi - lo) / self.cell - 1e-6).astype(int)
        self.dims = dims
        self.grid = np.zeros(dims, np.uint16)
        colors = [np.zeros(3)]
        for k, it in enumerate(items):
            f = it.cell / self.cell
            fi = int(round(f))
            assert abs(f - fi) < 1e-6, "item cell must be a multiple of the base cell"
            g = it.grid
            if fi > 1:
                g = np.repeat(np.repeat(np.repeat(g, fi, 0), fi, 1), fi, 2)
            off = np.round((np.array(it.origin) - lo) / self.cell).astype(int)
            base = len(colors) - 1
            colors.extend(list(srgb_to_lin(it.palette[1:256])))
            sub = self.grid[off[0]:off[0] + g.shape[0], off[1]:off[1] + g.shape[1],
                            off[2]:off[2] + g.shape[2]]
            m = g > 0
            sub[m] = g[m].astype(np.uint16) + base
        self.colors = np.array(colors)
        self.flat = self.grid.ravel()
        self.strides = np.array([dims[1] * dims[2], dims[2], 1], np.int64)

    # -- world <-> grid -----------------------------------------------------
    def to_cells(self, p):
        return (p - self.origin) / self.cell

    def occupied_corners(self):
        idx = np.argwhere(self.grid > 0)
        lo = idx.min(0)
        hi = idx.max(0) + 1
        # use the occupied voxels' convex extent via a coarse sample of points
        pts = idx.astype(float)
        if len(pts) > 60000:
            pts = pts[np.linspace(0, len(pts) - 1, 60000).astype(int)]
        corners = []
        for dx in (0, 1):
            for dy in (0, 1):
                for dz in (0, 1):
                    corners.append(pts + np.array([dx, dy, dz]))
        allp = np.concatenate(corners) * self.cell + self.origin
        return allp, lo, hi

    # -- DDA ray traversal --------------------------------------------------
    def trace(self, o, d, tmax=None):
        """o, d in cell units (N,3). Returns hit, t, axis, sign, colour index."""
        lib = _load_kernel()
        if lib:
            N = len(o)
            o = np.ascontiguousarray(o, np.float64)
            d = np.ascontiguousarray(d, np.float64)
            hit = np.zeros(N, np.uint8)
            t_out = np.empty(N)
            axis_out = np.empty(N, np.int8)
            sign_out = np.empty(N, np.int8)
            col_out = np.empty(N, np.uint16)
            nx, ny, nz = (int(v) for v in self.dims)
            lib.vtrace(self.flat, nx, ny, nz, o, d, N, np.inf if tmax is None else float(tmax),
                       hit, t_out, axis_out, sign_out, col_out)
            return hit.astype(bool), t_out, axis_out, sign_out, col_out
        return self._trace_numpy(o, d, tmax)

    def _trace_numpy(self, o, d, tmax=None):
        N = len(o)
        hit = np.zeros(N, bool)
        t_out = np.full(N, np.inf)
        axis_out = np.zeros(N, np.int8)
        sign_out = np.zeros(N, np.int8)
        col_out = np.zeros(N, np.uint16)
        if N == 0:
            return hit, t_out, axis_out, sign_out, col_out
        d = np.where(np.abs(d) < 1e-12, 1e-12, d)
        inv = 1.0 / d
        dims = self.dims.astype(float)
        t1 = -o * inv
        t2 = (dims - o) * inv
        tn = np.minimum(t1, t2)
        tf = np.maximum(t1, t2)
        t_enter = tn.max(1)
        t_exit = tf.min(1)
        if tmax is not None:
            t_exit = np.minimum(t_exit, tmax)
        inside0 = t_enter <= 0
        t_enter = np.maximum(t_enter, 0.0)
        ids = np.nonzero(t_enter < t_exit)[0]
        if ids.size == 0:
            return hit, t_out, axis_out, sign_out, col_out
        oo = o[ids]
        dd = d[ids]
        iv = inv[ids]
        tc = t_enter[ids]
        te = t_exit[ids]
        p = oo + dd * (tc + 1e-6)[:, None]
        dimi = self.dims.astype(np.int64)
        cell = np.clip(np.floor(p).astype(np.int64), 0, dimi - 1)
        step = np.where(dd > 0, 1, -1).astype(np.int64)
        tdel = np.abs(iv)
        nb = np.where(step > 0, cell + 1, cell).astype(float)
        tm = (nb - oo) * iv
        ax = tn[ids].argmax(1).astype(np.int64)
        ax = np.where(inside0[ids], -1, ax)
        flat = self.flat
        strides = self.strides
        while ids.size:
            c = flat[cell @ strides]
            h = c > 0
            if h.any():
                hi = ids[h]
                hit[hi] = True
                t_out[hi] = tc[h]
                a = ax[h]
                a2 = np.where(a < 0, 2, a)
                axis_out[hi] = a2
                sign_out[hi] = -step[h][np.arange(h.sum()), a2]
                col_out[hi] = c[h]
                k = ~h
                ids, cell, step, tdel, tm, tc, te = (ids[k], cell[k], step[k], tdel[k],
                                                      tm[k], tc[k], te[k])
                if ids.size == 0:
                    break
            r = np.arange(ids.size)
            a = tm.argmin(1)
            tc = tm[r, a]
            cell[r, a] += step[r, a]
            tm[r, a] += tdel[r, a]
            ax = a
            ca = cell[r, a]
            alive = (tc < te) & (ca >= 0) & (ca < dimi[a])
            if not alive.all():
                ids, cell, step, tdel, tm, tc, te, ax = (ids[alive], cell[alive], step[alive],
                                                          tdel[alive], tm[alive], tc[alive],
                                                          te[alive], ax[alive])
        return hit, t_out, axis_out, sign_out, col_out


# ---------------------------------------------------------------------------
# camera
# ---------------------------------------------------------------------------
@dataclass
class Camera:
    az: float            # degrees; 0 = camera in front (+Y) looking toward -Y
    el: float            # degrees above horizon
    width: int
    height: int
    ppm: float = 100.0   # pixels per metre (orthographic)
    center: np.ndarray = field(default_factory=lambda: np.zeros(3))

    def basis(self):
        a = math.radians(self.az)
        e = math.radians(self.el)
        back = np.array([math.cos(e) * math.sin(a), math.cos(e) * math.cos(a), math.sin(e)])
        f = -back
        r = np.cross(f, [0, 0, 1.0])
        r /= np.linalg.norm(r)
        u = np.cross(r, f)
        return f, r, u

    def fit(self, pts, margin=0.08, max_ppm=None):
        """Frame a point cloud (world m) with a fractional margin."""
        f, r, u = self.basis()
        pr = pts @ r
        pu = pts @ u
        w = pr.max() - pr.min()
        h = pu.max() - pu.min()
        ppm = min(self.width * (1 - 2 * margin) / max(w, 1e-6),
                  self.height * (1 - 2 * margin) / max(h, 1e-6))
        if max_ppm:
            ppm = min(ppm, max_ppm)
        self.ppm = ppm
        cr = (pr.max() + pr.min()) / 2
        cu = (pu.max() + pu.min()) / 2
        self.center = cr * r + cu * u
        return self

    def project(self, p):
        f, r, u = self.basis()
        p = np.asarray(p, float) - self.center
        x = self.width / 2 + (p @ r) * self.ppm
        y = self.height / 2 - (p @ u) * self.ppm
        return x, y


# ---------------------------------------------------------------------------
# lighting / render
# ---------------------------------------------------------------------------
@dataclass
class Light:
    sun_az: float = 40.0
    sun_el: float = 50.0
    sun_color: tuple = (1.0, 0.955, 0.88)
    sun_power: float = 2.35
    sun_radius_deg: float = 3.0
    sky_color: tuple = (0.80, 0.88, 1.0)
    sky_power: float = 1.05
    fill_power: float = 0.30           # unshadowed (but sky-occluded) fill from behind camera-left
    bounce: float = 0.55               # radiance multiplier for sky rays that hit other voxels
    ground_albedo: float = 0.30
    background: str = "#B4B5B0"
    floor: str = "#B4B5B0"


def _sun_dir(light, rng=None, n=1):
    a = math.radians(light.sun_az)
    e = math.radians(light.sun_el)
    base = np.array([math.cos(e) * math.sin(a), math.cos(e) * math.cos(a), math.sin(e)])
    if rng is None:
        return base
    t1 = np.cross(base, [0, 0, 1.0])
    t1 /= np.linalg.norm(t1)
    t2 = np.cross(base, t1)
    rad = math.radians(light.sun_radius_deg)
    r = rad * np.sqrt(rng.random(n))
    th = 2 * math.pi * rng.random(n)
    v = base[None] + (r * np.cos(th))[:, None] * t1 + (r * np.sin(th))[:, None] * t2
    return v / np.linalg.norm(v, axis=1, keepdims=True)


def _frames(n):
    a = np.where(np.abs(n[:, 2:3]) < 0.9, np.array([[0, 0, 1.0]]), np.array([[1.0, 0, 0]]))
    t1 = np.cross(n, a)
    t1 /= np.linalg.norm(t1, axis=1, keepdims=True)
    t2 = np.cross(n, t1)
    return t1, t2


def render(scene: Scene, cam: Camera, light: Light = Light(), aa: int = 4, k: int = 8,
           seed: int = 1, grid_lines: float | None = None):
    """Returns (H, W, 3) linear RGB and an alpha-like coverage mask of voxel hits."""
    rng = np.random.default_rng(seed)
    W, H = cam.width, cam.height
    f, r, u = cam.basis()
    sun0 = _sun_dir(light)
    sun_c = np.array(light.sun_color) * light.sun_power
    sky_c = np.array(light.sky_color) * light.sky_power
    fa = math.radians(light.sun_az + 180 + 35)
    fill_dir = np.array([math.cos(math.radians(25)) * math.sin(fa),
                         math.cos(math.radians(25)) * math.cos(fa), math.sin(math.radians(25))])
    fill_c = np.array([1.0, 0.97, 0.94]) * light.fill_power
    floor_lin = hex_lin(light.floor)
    bg_lin = hex_lin(light.background)
    ground_rad = light.ground_albedo * (sun_c * max(sun0[2], 0) + sky_c)
    ref = sun_c * max(sun0[2], 0) + sky_c + fill_c * max(fill_dir[2], 0)
    floor_open = sun_c * max(sun0[2], 0) + sky_c

    acc = np.zeros((H, W, 3))
    cover = np.zeros((H, W))
    jj, ii = np.mgrid[0:H, 0:W]
    ii = ii.ravel().astype(float)
    jj = jj.ravel().astype(float)
    na = int(math.ceil(math.sqrt(aa)))
    cell = scene.cell
    far = 1000.0
    for s in range(aa):
        sx = ((s % na) + rng.random(ii.size)) / na
        sy = ((s // na) + rng.random(ii.size)) / na
        px = (ii + sx - W / 2) / cam.ppm
        py = -(jj + sy - H / 2) / cam.ppm
        ow = cam.center[None] + px[:, None] * r[None] + py[:, None] * u[None] - f[None] * far
        oc = scene.to_cells(ow)
        dc = np.broadcast_to(f, oc.shape).copy()
        hit, t, axis, sgn, col = scene.trace(oc, dc)
        # ground plane z = 0 (world) -> cell z = -origin_z/cell = 0
        tz = np.where(dc[:, 2] < -1e-9, -oc[:, 2] / np.minimum(dc[:, 2], -1e-9), np.inf)
        surf = hit & (t <= tz)
        gnd = (~surf) & np.isfinite(tz)
        out = np.tile(bg_lin, (ii.size, 1))
        # ---- surfaces and floor share the lighting loop
        sel = np.nonzero(surf | gnd)[0]
        if sel.size:
            ts = np.where(surf[sel], t[sel], tz[sel])
            P = oc[sel] + dc[sel] * ts[:, None]
            Nn = np.zeros((sel.size, 3))
            is_s = surf[sel]
            ax = axis[sel]
            Nn[is_s, ax[is_s]] = sgn[sel][is_s]
            Nn[~is_s, 2] = 1.0
            alb = np.where(is_s[:, None], scene.colors[col[sel]], light.ground_albedo)
            P0 = P + Nn * 1e-4
            t1, t2 = _frames(Nn)
            sun_acc = np.zeros(sel.size)
            sky_acc = np.zeros((sel.size, 3))
            vis_acc = np.zeros(sel.size)
            for kk in range(k):
                # soft sun shadow
                sd = _sun_dir(light, rng, sel.size)
                ndl = np.maximum((Nn * sd).sum(1), 0)
                m = ndl > 0
                sh = np.zeros(sel.size)
                if m.any():
                    h2, *_ = scene.trace(P0[m], sd[m])
                    sh[m] = np.where(h2, 0.0, ndl[m])
                sun_acc += sh
                # cosine hemisphere sky sample (stratified in one dimension)
                u1 = (kk + rng.random(sel.size)) / k
                u2 = rng.random(sel.size)
                rr = np.sqrt(u1)
                ph = 2 * math.pi * u2
                lx = rr * np.cos(ph)
                ly = rr * np.sin(ph)
                lz = np.sqrt(np.maximum(0, 1 - u1))
                dirs = lx[:, None] * t1 + ly[:, None] * t2 + lz[:, None] * Nn
                h3, t3, _, _, c3 = scene.trace(P0, dirs)
                rad = np.tile(sky_c, (sel.size, 1))
                down = dirs[:, 2] < 0
                rad[down] = ground_rad
                rad[h3] = scene.colors[c3[h3]] * light.bounce * (sun_c * 0.45 + sky_c * 0.6)
                vis_acc += (~h3)
                sky_acc += rad
            sun_t = (sun_acc / k)[:, None] * sun_c[None]
            sky_t = sky_acc / k
            vis = vis_acc / k
            fill_t = (np.maximum((Nn * fill_dir).sum(1), 0) * (0.35 + 0.65 * vis))[:, None] * fill_c
            L = sun_t + sky_t + fill_t
            col_s = alb * L / ref
            # floor: show only occlusion over the backdrop colour
            gl = sun_t + sky_t
            ratio = gl / floor_open
            fl = floor_lin[None] * np.clip(ratio, 0, 1.2)
            if grid_lines:
                wx = P[:, 0] * cell + scene.origin[0]
                wy = P[:, 1] * cell + scene.origin[1]
                lw = 0.012
                on = ((np.abs((wx + grid_lines / 2) % grid_lines - grid_lines / 2) < lw) |
                      (np.abs((wy + grid_lines / 2) % grid_lines - grid_lines / 2) < lw))
                fl = np.where(on[:, None], fl * 0.88, fl)
            out[sel] = np.where(is_s[:, None], col_s, fl)
            cv = np.zeros(ii.size)
            cv[sel[is_s]] = 1
            cover += cv.reshape(H, W)
        acc += out.reshape(H, W, 3)
    return acc / aa, cover / aa


def tonemap(lin):
    """Linear below 0.8, soft shoulder above; then sRGB."""
    x = np.maximum(lin, 0)
    knee = 0.8
    y = np.where(x < knee, x, knee + (1 - knee) * (1 - np.exp(-(x - knee) / (1 - knee))))
    return lin_to_srgb8(y)


# ---------------------------------------------------------------------------
# 1.75 m reference mannequin (preview helper, not a library asset)
# ---------------------------------------------------------------------------

def mannequin():
    """Neutral 1.75 m figure at 0.05 m cells, facing +Y. Returns (grid, palette)."""
    pal = np.zeros((256, 3), np.uint8)
    pal[1] = (172, 178, 179)   # skin/body
    pal[2] = (126, 133, 136)   # trousers
    pal[3] = (98, 104, 107)    # shoes
    pal[4] = (150, 157, 160)   # shirt
    g = np.zeros((13, 6, 35), np.uint8)
    # legs (x 3-5 and 7-9) with shoes stepping forward
    for x0 in (3, 7):
        g[x0:x0 + 3, 1:4, 2:17] = 2
        g[x0:x0 + 3, 1:5, 0:2] = 3
    g[3:10, 1:4, 15:18] = 2          # hips
    g[3:10, 1:5, 18:25] = 4          # torso
    g[2:11, 1:5, 24:28] = 4          # shoulders
    for x0 in (0, 11):               # arms + hands
        g[x0:x0 + 2, 2:4, 15:27] = 4
        g[x0:x0 + 2, 2:4, 12:15] = 1
    g[5:8, 2:4, 28:30] = 1           # neck
    g[5:8, 1:5, 30:35] = 1           # head (top of z=34 -> 1.75 m)
    return g, pal
