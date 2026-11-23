# SirenVoxelLibrary

**A standalone, curated voxel asset workshop.** Models are designed here, reviewed here, and only then *copied selectively* into games such as [Sirens Went Quiet](https://github.com/crosenlund79/SirensWentQuiet). This repository is **not** a game, a Godot add-on, or a dependency of any game.

## Design goal

Make expressive, readable, hand-crafted voxel models for a believable, slightly stylized modern world. Lived-in rather than pristine; atmospheric rather than excessively grimy. The models should look like they belong to one artist, not a random pack of unrelated primitives.

Voxel art is an **art direction**, not a requirement that every game object uses runtime destructible voxels. The game can render approved assets as conventional meshes or convert suitable assets into its own voxel engine.

## Start here

- [Voxel art bible](docs/VOXEL_ART_BIBLE.md) — visual identity, scale, resolution, materials, and shape language.
- [Model specification template](docs/MODEL_SPEC_TEMPLATE.md) — what each proposed model must define.
- [Production and export rules](docs/EXPORT_RULES.md) — editable source, formats, orientation, conversions, and checks.
- [Review and approval](docs/REVIEW_PROCESS.md) — Candidate → Approved → Integrated.
- [GPT versus Claude rivalry](docs/RIVAL_WORKFLOW.md) — independent rival models, exact prefixes, side-by-side review.
- [First five models](docs/PILOT_BATCH.md) — workbench, rain collector, stove, bed, and dead pine.
- [Claude working instructions](CLAUDE.md) — how to produce models without bypassing review.
- [Voxel Viewer](viewer/README.md) — open and rotate genuine `.vox` models in your browser, offline and without installation.

## Library layout

```text
docs/                  Guidelines, reviews, specs, and pilot briefs
models/<category>/<id>/  A model's source, metadata and derived files
previews/<category>/     Consistent contact sheets and showcase renders
tools/                  Generators, validators, exporters (as introduced)
catalog.json            Machine-readable catalog of model records
viewer/index.html      Self-contained read-only voxel viewer (double-click to open)
```

Every completed model directory contains `<asset_id>.vox` (the editable source), `model.json`, and actual rendered previews (under `previews/`); optional `<asset_id>.glb` exports are generated from that source.

## Two creators, one shared standard 🧱

**ChatGPT models must start with `GPT_`; Claude models must start with `Claude_`.** Preserve the exact capitalization in asset IDs, model folders, `.vox` and `.glb` filenames, specs, and batch contact sheets. The suffix is the same base brief for both creators, e.g. `GPT_workbench_worn` and `Claude_workbench_worn`. Both follow the same art bible but create their geometry independently. Nothing is preferred or approved automatically.

Review paired models side by side and select the better version **per object**, rather than forcing one creator to win the entire library. The two creators must never overwrite or delete each other's models. See [Rival Workflow](docs/RIVAL_WORKFLOW.md).

## Rules of the workshop

1. **Approval is personal.** Claude may create Candidates; the user alone approves models.
2. **One canonical editable source per model.** Exported meshes are derivatives, not the master.
3. **Real files, not rendered pictures pretending to be voxel models.**
4. **Consistent scale, forward direction, pivot, and palette across the library.**
5. **Avoid unnecessary voxel counts.** Resolution is chosen per object, not fixed globally.
6. **Never silently replace an approved asset.** Make a revision and request review.
7. **Do not automatically copy models into Sirens Went Quiet.** Integration is a separate approved action.

The pilot batch is a planned test of these rules, not a request to mass-produce assets.
