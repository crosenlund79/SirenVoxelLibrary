"""Validate Claude's candidates against the library rules (docs/EXPORT_RULES.md section 5).

    python3 tools/claude/validate.py [ids...] [--batch catalog_A] [--fast] [--json out.json]

Required: numpy. Optional independent checks run when available and are reported as
'skipped' otherwise:
  * py-vox-io (`import pyvox`)            - third-party VOX parser
  * Goxel 0.11 + xvfb-run                 - independent editor import (VOX -> .txt export)
  * pygltflib / trimesh                   - third-party glTF loaders
  * Khronos glTF-Validator (npm)          - set GLTF_VALIDATOR_DIR to a node_modules parent
A self-written parser alone does not prove MagicaVoxel compatibility; GUI checks stay
'unverified' in model.json until a person opens the files in MagicaVoxel / Godot.
"""
from __future__ import annotations

import json
import os
import shutil
import struct
import subprocess
import sys
import tempfile
from collections import Counter, deque
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
import voxkit as vk  # noqa: E402

AXIS_TO_GODOT = np.array([[1, 0, 0], [0, 0, 1], [0, -1, 0]], float)  # godot = M @ (x, y, z)


def components(grid):
    """6-connected components of occupied cells -> list of sizes (descending)."""
    occ = grid > 0
    seen = np.zeros_like(occ)
    sizes = []
    for start in map(tuple, np.argwhere(occ)):
        if seen[start]:
            continue
        q = deque([start])
        seen[start] = True
        n = 0
        while q:
            c = q.popleft()
            n += 1
            for d in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)):
                nb = (c[0] + d[0], c[1] + d[1], c[2] + d[2])
                if all(0 <= nb[i] < occ.shape[i] for i in range(3)) and occ[nb] and not seen[nb]:
                    seen[nb] = True
                    q.append(nb)
        sizes.append(n)
    return sorted(sizes, reverse=True)


def exposed_faces_by_colour(grid, exterior_only=True):
    """Faces bordering empty space; exterior_only counts only air connected to the outside
    (the GLB exporter skips faces lining sealed, hollowed interiors)."""
    from export_glb import exterior_air
    p = np.pad(grid, 1)
    air = exterior_air(grid) if exterior_only else (p == 0)
    core = p[1:-1, 1:-1, 1:-1]
    out = Counter()
    for ax in range(3):
        for sgn in (1, -1):
            nb = np.roll(air, -sgn, axis=ax)[1:-1, 1:-1, 1:-1]
            m = (core > 0) & nb
            out.update(Counter(core[m].tolist()))
    return out


def check_vox(meta, path):
    res = {}
    info = vk.read_vox(path)              # strict: raises on malformed chunk structure
    res["header_version"] = info["version"]
    res["chunks"] = info["chunks"]
    assert info["chunks"] == ["SIZE", "XYZI", "RGBA"], info["chunks"]
    size = tuple(info["size"])
    vox = info["voxels"].astype(int)
    pal = info["palette"]
    assert max(size) <= 256, "exceeds VOX 256-cell axis limit"
    assert (vox[:, :3] >= 0).all() and (vox[:, :3] < np.array(size)).all(), "voxel out of bounds"
    keys = vox[:, 0] * size[1] * size[2] + vox[:, 1] * size[2] + vox[:, 2]
    assert len(np.unique(keys)) == len(vox), "duplicate voxel coordinates"
    assert (vox[:, 3] >= 1).all(), "colour index 0 used for an occupied voxel"
    assert (pal[vox[:, 3], 3] == 255).all(), "voxel references an undefined palette entry"
    pv = meta.get("palette_version", 1)
    assert np.array_equal(pal[1:, :3], vk.PALETTES[pv][1:]), f"palette differs from Claude palette v{pv}"
    grid = vk.vox_to_grid(info)
    cell = meta["voxel_size_m"]
    assert len(vox) == meta["occupied_voxels"], (len(vox), meta["occupied_voxels"])
    assert list(size) == meta["grid_size_cells"], (size, meta["grid_size_cells"])
    dims = [round(s * cell, 3) for s in size]
    assert dims == meta["dimensions_m"], (dims, meta["dimensions_m"])
    lo, hi = vox[:, :3].min(0), vox[:, :3].max(0)
    assert (lo == 0).all() and (hi == np.array(size) - 1).all(), "bounds are not tight to occupancy"
    px, py, pz = meta["pivot_voxel"]
    assert pz == 0 and 0 <= px <= size[0] and 0 <= py <= size[1], "pivot outside footprint"
    base = grid[:, :, 0] > 0
    assert base.any(), "nothing touches the ground plane"
    comps = components(grid)
    res.update({"size": size, "count": int(len(vox)), "dimensions_m": dims,
                "ground_cells": int(base.sum()), "components_6conn": comps[:5],
                "single_connected_piece": len(comps) == 1,
                "palette_indices_used": int(len(np.unique(vox[:, 3])))})
    allowed = int(meta.get("allowed_components", 1))
    if allowed > 1:
        assert meta.get("components_reason"), "allowed_components needs components_reason"
        res["single_connected_piece"] = f"{len(comps)} pieces, documented: {meta['components_reason']}"
    assert len(comps) <= allowed, f"disconnected pieces: {comps[:6]} (allowed {allowed})"
    # art lint: interior cells that can never be seen (all 6 neighbours occupied)
    occ = np.pad(grid > 0, 1)
    core = occ[1:-1, 1:-1, 1:-1]
    hidden = core.copy()
    for ax in range(3):
        for sh in (1, -1):
            hidden &= np.roll(occ, sh, axis=ax)[1:-1, 1:-1, 1:-1]
    res["hidden_interior_voxels"] = int(hidden.sum())
    res["hidden_ratio"] = round(float(hidden.sum()) / len(vox), 3)
    return res, grid, pal


def check_pyvox(path, grid, pal):
    try:
        from pyvox.parser import VoxParser
    except ImportError:
        return "skipped (py-vox-io not installed)"
    m = VoxParser(str(path)).parse()
    model = m.models[0]
    s = (model.size.x, model.size.y, model.size.z)
    assert s == grid.shape, (s, grid.shape)
    theirs = {(v.x, v.y, v.z): v.c for v in model.voxels}
    ours = {tuple(map(int, c)): int(grid[tuple(c)]) for c in np.argwhere(grid > 0)}
    assert theirs == ours, "py-vox-io voxel set differs"
    tp = np.array([[c.r, c.g, c.b] for c in m.palette])
    assert np.array_equal(tp[1:256], pal[1:256, :3]) or np.array_equal(tp[:255], pal[1:256, :3]), \
        "py-vox-io palette differs"
    return f"pass ({len(theirs)} voxels, size {s}, palette identical)"


def check_goxel(path, grid, pal):
    if not (shutil.which("goxel") and shutil.which("xvfb-run")):
        return "skipped (goxel / xvfb-run not installed)"
    with tempfile.TemporaryDirectory() as td:
        src = Path(td) / path.name
        shutil.copy(path, src)
        out = Path(td) / "export.txt"
        subprocess.run(["xvfb-run", "-a", "goxel", str(src), "-e", str(out)], cwd=td,
                       capture_output=True, timeout=120)
        if not out.exists():
            return "fail (goxel produced no export)"
        rows = [ln.split() for ln in out.read_text().splitlines() if ln and not ln.startswith("#")]
    pts = np.array([[int(a), int(b), int(c)] for a, b, c, _ in rows])
    cols = [r[3].lower() for r in rows]
    ours = {}
    for c in np.argwhere(grid > 0):
        ours[tuple(map(int, c))] = "%02x%02x%02x" % tuple(pal[grid[tuple(c)], :3])
    pts = pts - pts.min(0)
    theirs = {tuple(map(int, p)): col for p, col in zip(pts, cols)}
    assert len(theirs) == len(ours), (len(theirs), len(ours))
    assert theirs == ours, "goxel voxel positions/colours differ (axis or palette mismatch)"
    return f"pass (imported and re-exported {len(theirs)} voxels; positions and colours identical)"


def read_glb(path):
    b = Path(path).read_bytes()
    magic, ver, length = struct.unpack_from("<III", b, 0)
    assert magic == 0x46546C67 and ver == 2 and length == len(b), "bad GLB header"
    jl, jt = struct.unpack_from("<II", b, 12)
    assert jt == 0x4E4F534A
    js = json.loads(b[20:20 + jl])
    bl, bt = struct.unpack_from("<II", b, 20 + jl)
    assert bt == 0x004E4942
    binc = b[28 + jl:28 + jl + bl]

    def acc(i, dtype, ncomp):
        a = js["accessors"][i]
        v = js["bufferViews"][a["bufferView"]]
        arr = np.frombuffer(binc, dtype, a["count"] * ncomp, v["byteOffset"] + a.get("byteOffset", 0))
        return arr.reshape(a["count"], ncomp) if ncomp > 1 else arr

    prim = js["meshes"][0]["primitives"][0]
    pos = acc(prim["attributes"]["POSITION"], np.float32, 3)
    col = acc(prim["attributes"]["COLOR_0"], np.float32, 3)
    nrm = acc(prim["attributes"]["NORMAL"], np.float32, 3)
    idx = acc(prim["indices"], np.uint32, 1)
    return js, pos, nrm, col, idx


def check_glb(meta, path, grid, pal):
    js, pos, nrm, col, idx = read_glb(path)
    cell = meta["voxel_size_m"]
    piv = np.array(meta["pivot_voxel"], float)
    # expected bounds: source grid box -> pivot -> Godot axes
    corners = np.array([[x, y, z] for x in (0, grid.shape[0]) for y in (0, grid.shape[1])
                        for z in (0, grid.shape[2])], float)
    exp = ((corners - piv) * cell) @ AXIS_TO_GODOT.T
    assert np.allclose(pos.min(0), exp.min(0), atol=1e-4), (pos.min(0), exp.min(0))
    assert np.allclose(pos.max(0), exp.max(0), atol=1e-4), (pos.max(0), exp.max(0))
    assert abs(pos[:, 1].min()) < 1e-6, "model does not stand on Godot y = 0"
    # every triangle faces outward along its stored normal (CCW winding)
    tri = pos[idx].reshape(-1, 3, 3)
    n_geo = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
    n_st = nrm[idx].reshape(-1, 3, 3)[:, 0]
    assert (np.einsum("ij,ij->i", n_geo, n_st) > 0).all(), "winding/normal mismatch"
    # per-colour face area equals exposed voxel faces -> no missing or extra faces
    lin = np.where(pal[:, :3] / 255.0 <= 0.04045, pal[:, :3] / 255.0 / 12.92,
                   ((pal[:, :3] / 255.0 + 0.055) / 1.055) ** 2.4)
    tri_col = col[idx].reshape(-1, 3, 3)[:, 0]
    area = 0.5 * np.linalg.norm(n_geo, axis=1) / (cell * cell)
    got = Counter()
    for ci in np.unique(grid[grid > 0]):
        m = np.all(np.abs(tri_col - lin[ci]) < 1e-5, axis=1)
        got[int(ci)] = int(round(area[m].sum()))
    # exterior-only faces (current exporter) or all faces (frozen pilot GLBs)
    from export_glb import exterior_air
    got = {int(k): int(v) for k, v in got.items()}
    mode = None
    for ext in (True, False):
        want = {int(k): int(v) for k, v in exposed_faces_by_colour(grid, ext).items()}
        if got == want:
            mode = ext
            break
    assert mode is not None, "face area mismatch"
    # orientation: library front (+Y) must become Godot -Z
    air = exterior_air(grid) if mode else (np.pad(grid, 1) == 0)
    src_front = int(air[1:-1, 2:, 1:-1][grid > 0].sum())
    glb_front = int(round(area[n_st[:, 2] < -0.5].sum()))
    assert src_front == glb_front, ("front-facing area", src_front, glb_front)
    res = {"triangles": int(len(idx) // 3), "vertices": int(len(pos)),
           "bounds_godot_m": [[round(float(v), 3) for v in pos.min(0)],
                              [round(float(v), 3) for v in pos.max(0)]],
           "exposed_faces": int(sum(want.values())), "front_faces_to_-Z": glb_front,
           "faces_exported": "exterior only" if mode else "all (pilot)"}
    try:
        import trimesh
        sc = trimesh.load(str(path))
        g = list(sc.geometry.values())[0] if hasattr(sc, "geometry") else sc
        assert np.allclose(g.bounds, [pos.min(0), pos.max(0)], atol=1e-4)
        res["trimesh"] = f"pass (loaded, {len(g.faces)} faces, bounds match)"
    except ImportError:
        res["trimesh"] = "skipped (not installed)"
    try:
        import pygltflib
        pygltflib.GLTF2().load(str(path))
        res["pygltflib"] = "pass (loaded)"
    except ImportError:
        res["pygltflib"] = "skipped (not installed)"
    res["khronos_gltf_validator"] = khronos(path)
    return res


def khronos(path):
    d = os.environ.get("GLTF_VALIDATOR_DIR")
    if not d or not shutil.which("node"):
        return "skipped (set GLTF_VALIDATOR_DIR to a dir with node_modules/gltf-validator)"
    js = ("const v=require('gltf-validator');const fs=require('fs');"
          "v.validateBytes(new Uint8Array(fs.readFileSync(process.argv[1])))"
          ".then(r=>console.log(JSON.stringify(r.issues)))")
    out = subprocess.run(["node", "-e", js, str(path)], cwd=d, capture_output=True, text=True,
                         timeout=120)
    issues = json.loads(out.stdout)
    status = "pass" if issues["numErrors"] == 0 else "FAIL"
    return (f"{status} ({issues['numErrors']} errors, {issues['numWarnings']} warnings, "
            f"{issues['numInfos']} infos, {issues['numHints']} hints)")


def check_naming(m, meta):
    a = meta["id"]
    assert a == f"Claude_{meta['base_id']}" and meta["creator"] == "Claude"
    assert meta["source"] == f"{a}.vox" and meta["derived"]["glb"] == f"{a}.glb"
    assert meta["status"] == "candidate", "must stay candidate"
    if m is not None:
        assert m["source_path"] == f"models/{meta['category']}/{a}/{a}.vox"
        assert m["status"] == "candidate", "catalog entry must stay candidate"
    if meta.get("spec"):
        assert (ROOT / meta["spec"]).exists(), f"missing spec {meta['spec']}"
    for v in ("hero", "front", "side", "scale"):
        p = ROOT / "previews" / meta["category"] / a / f"{v}.png"
        assert p.exists(), f"missing preview {p}"
    return "pass"


BUDGET = {0.0125: 12000, 0.025: 15000, 0.05: 20000, 0.1: 30000, 0.2: 30000, 0.5: 30000}
PILOT = {"workbench_worn", "rain_collector_basic", "wood_stove_compact", "single_bed_unmade",
         "pine_dead_small"}


def lint(meta, vres):
    """Art/tech warnings that do not fail the build but must be looked at."""
    w = []
    n = meta["occupied_voxels"]
    budget = BUDGET.get(meta["voxel_size_m"], 20000)
    if n > budget:
        w.append(f"{n} voxels exceeds the {budget} guide for {meta['voxel_size_m']} m cells")
    if n > 80000:
        w.append("over the viewer's 80,000-voxel part cap")
    if vres.get("hidden_ratio", 0) > 0.25:
        w.append(f"{vres['hidden_ratio']:.0%} of voxels are invisible interior fill - hollow it out")
    if n < 40:
        w.append("fewer than 40 voxels - is it readable?")
    return w


def main():
    args = sys.argv[1:]
    fast = "--fast" in args
    skip = {args[args.index(f) + 1] for f in ("--json", "--batch") if f in args}
    want = [a for a in args if not a.startswith("--") and a not in skip]
    batch = args[args.index("--batch") + 1] if "--batch" in args else None
    cat = json.loads((ROOT / "catalog.json").read_text())
    by_id = {m["id"]: m for m in cat["models"]}
    report = {"models": {}, "catalog": {}}
    ok = True
    creators = Counter(m["creator"] for m in cat["models"])
    report["catalog"] = {"entries_by_creator": dict(creators)}
    metas = []
    for mp in sorted(ROOT.glob("models/*/Claude_*/model.json")):
        meta = json.loads(mp.read_text())
        if want and meta["base_id"] not in want and meta["id"] not in want:
            continue
        if batch and meta.get("batch") not in (batch, f"Claude_{batch}"):
            continue
        metas.append((mp, meta))
    for mp, meta in metas:
        m = by_id.get(meta["id"])          # catalog entry, if synced yet
        path = mp.parent / meta["source"]
        r = {}
        try:
            r["naming_and_status"] = check_naming(m, meta)
            r["vox"], grid, pal = check_vox(meta, path)
            r["py_vox_io"] = check_pyvox(path, grid, pal)
            r["goxel_import"] = "skipped (--fast)" if fast else check_goxel(path, grid, pal)
            glb = mp.parent / meta["derived"]["glb"]
            if fast:
                os.environ.pop("GLTF_VALIDATOR_DIR", None)
            r["glb"] = check_glb(meta, glb, grid, pal)
            if not fast:
                assert r["glb"]["khronos_gltf_validator"].startswith(("pass", "skipped")), \
                    r["glb"]["khronos_gltf_validator"]
            r["warnings"] = lint(meta, r["vox"])
            r["result"] = "pass" + (f" ({len(r['warnings'])} warnings)" if r["warnings"] else "")
        except AssertionError as e:
            ok = False
            r["result"] = f"FAIL: {e}"
        report["models"][meta["id"]] = r
        print(f"{meta['id']:40s} {r['result']}")
        for w in r.get("warnings", []):
            print(f"{'':40s}   warning: {w}")
    # catalog consistency (only when the whole library is checked)
    if not want and not batch:
        on_disk = {meta["id"] for _, meta in metas}
        in_cat = {m["id"] for m in cat["models"] if m["creator"] == "Claude"}
        report["catalog"]["claude_missing_from_catalog"] = sorted(on_disk - in_cat)
        report["catalog"]["claude_catalog_without_files"] = sorted(in_cat - on_disk)
        if on_disk != in_cat:
            ok = False
            print("catalog mismatch:", report["catalog"])
    if "--json" in args:
        Path(args[args.index("--json") + 1]).write_text(json.dumps(report, indent=2, default=str))
    passed = sum(1 for r in report["models"].values() if r["result"].startswith("pass"))
    print(f"{passed}/{len(report['models'])} models pass")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
