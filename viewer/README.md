# Browser Voxel Viewer

## Online viewing with GitHub Pages

After GitHub Pages has been enabled for this repository, the public viewer URL is:

**https://crosenlund79.github.io/SirenVoxelLibrary/**

The repo contains `.github/workflows/publish-voxel-viewer.yml`, which builds and deploys a static website whenever `main` changes its viewer, `catalog.json`, models or previews. The published site serves only the viewer, catalog, and model/preview files. No backend or account is required.

**One-time GitHub setting (repository owner):**

1. Open `https://github.com/crosenlund79/SirenVoxelLibrary/settings/pages`.
2. Under **Build and deployment**, choose **Source → GitHub Actions**.
3. Open the repository **Actions** tab and re-run the **Publish Voxel Viewer** workflow if the initial run failed before Pages was enabled.
4. Verify the live website above.

GitHub Pages must actually deploy successfully before the URL is considered live. Without the one-time setting, the workflow may fail at `configure-pages`; simply committing a workflow is not enough.


**Open `viewer/index.html` by double-clicking it.** It is one self-contained HTML file: no Godot, MagicaVoxel, Python, npm, external libraries, or installation required.

## Using it

1. Download or clone this repository (or download the `viewer/index.html` file).
2. Open `viewer/index.html` in a current Chrome, Edge, or Firefox browser.
3. Use **Choose .vox file** or drag a `.vox` file from `models/...` into the view.
4. Drag to rotate; use the wheel to zoom; Shift+drag to pan.
5. Toggle the ground grid, reset the camera, or save the current viewport to PNG.

The built-in sample workbench merely demonstrates that the viewer is working; it is **not** an actual GPT or Claude candidate.

## Browse the library catalog

If the repository is hosted as a static website, the viewer also reads `../catalog.json` and offers a dropdown of actual catalogued models. The catalog requires the usual fields including `source_path`; `model.json` metadata is used if `metadata_path` exists.

**Deep links:** `viewer/?model=<asset_id>` (for example `viewer/?model=Claude_dining_table`) opens that catalogued model directly; the Claude catalog page (`catalog/index.html`) links every model this way.

When opened directly as a local `file://` page, browser security normally blocks automatic catalog loading. **The file picker still works offline.**

For optional catalog browsing from a local clone, serve the repository root with any static web server, e.g. run `python -m http.server 8000` in the repo and visit `http://localhost:8000/viewer/`. A server is **not** required for the ordinary file picker.

## What it supports

- Genuine MagicaVoxel `.vox` files with `SIZE`, `XYZI`, optional `RGBA` palette.
- 3D orbit/zoom/pan using a dependency-free JavaScript canvas renderer.
- Culling interior faces, simple directional shading, a ground grid and PNG snapshots.
- Single-model files and choosing individual parts of basic multi-model files.
- Dimensions in voxel cells, occupied cell count and exposed face count.
- Real-world cell size when loaded through the catalog with `model.json`.

## Known limits

- **Read-only inspection**, not a voxel editor.
- Multi-model scene hierarchy and transformations (`nTRN`, `nGRP`, `nSHP`) are **not assembled**. Instead choose individual models in the parts dropdown.
- Intended for the pilot library's modest, single-model items; dense/very large models can render slowly because it uses software Canvas 2D rather than a 3D engine. The viewer caps a part at 80,000 occupied voxels.
- No advanced transparent materials, MagicaVoxel-specific shader/rendering or animation.
- A `.vox` does not contain a universal metres-per-voxel value. Use `model.json` for physical size.
- The format parser supports ordinary `MAIN` child chunks; nested scene-graph extensions are not interpreted.
- Not yet a polished cross-browser performance benchmark. A small representative VOX file was loaded and rendered with no browser errors, but large model rendering has not been benchmarked.

**Library review remains independent:** neither opening a model nor saving its screenshot approves or integrates it into Sirens Went Quiet.
