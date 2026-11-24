"""Derive a Godot-ready .glb from a library .vox (creator-neutral).

* Greedy meshing per face direction, per slice, per palette colour (no hidden faces).
* Library voxel axes (X right, Y front, Z up) -> glTF/Godot (X right, Y up, -Z front):
  godot = ((vx - px) * s, (vz - pz) * s, -(vy - py) * s), with the metadata pivot (px, py, pz).
  This mapping is a proper rotation (det = +1), so CCW winding is preserved.
* Colours as linear-space COLOR_0 vertex colours (glTF spec) on one rough, non-metal material.
  Faceted normals; no smoothing.
"""
from __future__ import annotations

import json
import struct

import numpy as np


def _srgb_to_lin(c):
    c = np.asarray(c, np.float64) / 255.0
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def exterior_air(grid: np.ndarray) -> np.ndarray:
    """Padded boolean mask of empty cells connected (6-way) to the outside of the grid.
    Sealed interior voids (hollowed shells) are excluded, so no faces are emitted into them;
    cavities open to the outside (a firebox seen through a flue) are kept."""
    from collections import deque
    occ = np.pad(grid > 0, 1)
    air = np.zeros_like(occ)
    q = deque([(0, 0, 0)])
    air[0, 0, 0] = True
    shp = occ.shape
    while q:
        x, y, z = q.popleft()
        for dx, dy, dz in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)):
            n = (x + dx, y + dy, z + dz)
            if 0 <= n[0] < shp[0] and 0 <= n[1] < shp[1] and 0 <= n[2] < shp[2] \
                    and not occ[n] and not air[n]:
                air[n] = True
                q.append(n)
    return air


def greedy_quads(grid: np.ndarray, exterior_only: bool = True):
    """Yield (axis, sign, plane, u0, u1, v0, v1, colour) for merged exposed faces.
    exterior_only: only faces bordering air connected to the outside."""
    dims = grid.shape
    padded = np.zeros(tuple(d + 2 for d in dims), grid.dtype)
    padded[1:-1, 1:-1, 1:-1] = grid
    air = exterior_air(grid) if exterior_only else (padded == 0)
    for d in range(3):
        u, v = (d + 1) % 3, (d + 2) % 3
        for sign in (1, -1):
            for k in range(dims[d]):
                sl = [slice(1, -1)] * 3
                sl[d] = k + 1
                cur = padded[tuple(sl)]
                sl[d] = k + 1 + sign
                nb = air[tuple(sl)]
                mask = np.where((cur > 0) & nb, cur, 0)
                # mask axes are the two remaining source axes in increasing order
                axes = [a for a in range(3) if a != d]
                if axes != [u, v]:          # reorder to (u, v)
                    mask = mask.T
                mask = mask.copy()
                nu, nv = mask.shape
                for i in range(nu):
                    j = 0
                    while j < nv:
                        c = mask[i, j]
                        if c == 0:
                            j += 1
                            continue
                        w = 1
                        while j + w < nv and mask[i, j + w] == c:
                            w += 1
                        h = 1
                        while i + h < nu and np.all(mask[i + h, j:j + w] == c):
                            h += 1
                        mask[i:i + h, j:j + w] = 0
                        plane = k + 1 if sign > 0 else k
                        yield d, sign, plane, i, i + h, j, j + w, int(c)
                        j += w


def build_mesh(grid, palette_rgb, cell, pivot):
    pos, nrm, col, idx = [], [], [], []
    lin = _srgb_to_lin(palette_rgb)
    nquads = 0
    for d, sign, plane, u0, u1, v0, v1, c in greedy_quads(grid):
        u, v = (d + 1) % 3, (d + 2) % 3
        corners = [(u0, v0), (u1, v0), (u1, v1), (u0, v1)]
        if sign < 0:
            corners = corners[::-1]
        base = len(pos)
        n_src = [0.0, 0.0, 0.0]
        n_src[d] = float(sign)
        for (a, b) in corners:
            p = [0.0, 0.0, 0.0]
            p[d] = plane
            p[u] = a
            p[v] = b
            x, y, z = ((p[0] - pivot[0]) * cell, (p[1] - pivot[1]) * cell,
                       (p[2] - pivot[2]) * cell)
            pos.append((x, z, -y))
            nrm.append((n_src[0], n_src[2], -n_src[1]))
            col.append(tuple(lin[c]))
        idx += [base, base + 1, base + 2, base, base + 2, base + 3]
        nquads += 1
    return (np.array(pos, np.float32), np.array(nrm, np.float32), np.array(col, np.float32),
            np.array(idx, np.uint32), nquads)


def write_glb(path, asset_id, grid, palette_rgb, cell, pivot, extras=None):
    pos, nrm, col, idx, nquads = build_mesh(grid, palette_rgb, cell, pivot)
    blobs = []
    views = []
    accessors = []

    def add(arr, target, comp, typ, minmax=False):
        data = arr.tobytes()
        off = sum(len(b) for b in blobs)
        pad = (-len(data)) % 4
        blobs.append(data + b"\x00" * pad)
        views.append({"buffer": 0, "byteOffset": off, "byteLength": len(data), "target": target})
        acc = {"bufferView": len(views) - 1, "componentType": comp, "count": len(arr), "type": typ}
        if minmax:
            acc["min"] = [float(v) for v in arr.min(0)]
            acc["max"] = [float(v) for v in arr.max(0)]
        accessors.append(acc)
        return len(accessors) - 1

    a_pos = add(pos, 34962, 5126, "VEC3", minmax=True)
    a_nrm = add(nrm, 34962, 5126, "VEC3")
    a_col = add(col, 34962, 5126, "VEC3")
    a_idx = add(idx, 34963, 5125, "SCALAR")
    bin_data = b"".join(blobs)
    gltf = {
        "asset": {"version": "2.0",
                  "generator": "SirenVoxelLibrary tools/claude/export_glb.py (derived from .vox)"},
        "scene": 0,
        "scenes": [{"name": asset_id, "nodes": [0]}],
        "nodes": [{"name": asset_id, "mesh": 0}],
        "meshes": [{"name": asset_id, "primitives": [{
            "attributes": {"POSITION": a_pos, "NORMAL": a_nrm, "COLOR_0": a_col},
            "indices": a_idx, "material": 0, "mode": 4}]}],
        "materials": [{"name": f"{asset_id}_vertex_colour",
                       "pbrMetallicRoughness": {"baseColorFactor": [1, 1, 1, 1],
                                                "metallicFactor": 0.0, "roughnessFactor": 0.92}}],
        "accessors": accessors,
        "bufferViews": views,
        "buffers": [{"byteLength": len(bin_data)}],
    }
    if extras:
        gltf["asset"]["extras"] = extras
    js = json.dumps(gltf, separators=(",", ":")).encode()
    js += b" " * ((-len(js)) % 4)
    total = 12 + 8 + len(js) + 8 + len(bin_data)
    with open(path, "wb") as f:
        f.write(struct.pack("<III", 0x46546C67, 2, total))
        f.write(struct.pack("<II", len(js), 0x4E4F534A))
        f.write(js)
        f.write(struct.pack("<II", len(bin_data), 0x004E4942))
        f.write(bin_data)
    return {"vertices": int(len(pos)), "triangles": int(len(idx) // 3), "quads": nquads}
