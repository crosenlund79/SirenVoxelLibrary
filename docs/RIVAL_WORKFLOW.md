# Rival Model Workshop — GPT vs Claude

Two independent creators build **competing interpretations of the same model briefs**. The user decides which models, if any, join the approved library or a game. The competition is intended to improve craft, not encourage speed or volume.

## Exact creator prefixes

| Creator | Required model ID prefix | Example model ID |
|---|---|---|
| ChatGPT / GPT | `GPT_` | `GPT_workbench_worn` |
| Claude | `Claude_` | `Claude_workbench_worn` |

**Capitalization is mandatory.** The remaining base ID is lowercase `snake_case`. Do not use `gpt_`, `claude_`, `ChatGPT_`, unprefixed model IDs, or names that imply the other creator made the asset.

**The prefix applies to the model ID, model directory, canonical VOX filename, derived GLB filename, spec filename, and named contact-sheet outputs.** Supporting generic files (`model.json`, `hero.png`, `front.png`, etc.) live inside the prefixed directory and need not repeat it.

Example paired assets:

```text
models/furniture/GPT_workbench_worn/
  GPT_workbench_worn.vox
  GPT_workbench_worn.glb       # optional
  model.json
models/furniture/Claude_workbench_worn/
  Claude_workbench_worn.vox
  Claude_workbench_worn.glb    # optional
  model.json
previews/furniture/GPT_workbench_worn/{hero,front,side,scale}.png
previews/furniture/Claude_workbench_worn/{hero,front,side,scale}.png
docs/specs/furniture/GPT_workbench_worn.md
docs/specs/furniture/Claude_workbench_worn.md
previews/batches/GPT_pilot_001.png
previews/batches/Claude_pilot_001.png
```

A single model's canonical source is always the file named `<asset_id>.vox`. Do not create competing `source.vox` masters in the same model folder.

## Fair comparison and independent craftsmanship

- **Same briefs:** GPT and Claude should target the same base assets from `docs/PILOT_BATCH.md`, with the same approximate dimensions, functional requirements, shared art bible, coordinate contract and resolution guidelines.
- **Independent execution:** Each creator designs the actual voxel geometry independently. Reviewing the other's final work may inform discussion, but **do not copy/trace/modify the competitor's voxel grid or generators** and pass it off as a new model.
- **Original implementations:** Generator scripts, if used, should identify the creator clearly and avoid overwriting either creator's outputs. Shared generic validation/rendering tools are fine.
- **No model is pre-approved:** Every asset enters as `candidate` and needs explicit user approval. The user can approve either version, both, neither, or request a mixed follow-up design.
- **No forced winner:** Label visual comparisons by creator, not by predetermined rank. Review silhouette, coherence, material treatment, usability, occupied cell count and real game-camera readability.
- **Comparable previews:** Use the same camera angles, neutral backdrop, lighting, reference human, and **world-space scale** for side-by-side renders. Tall items may need an additional full-height inset.
- **Do not overwrite rival files:** GPT writes only `GPT_`-owned model directories/specs/contact sheets; Claude writes only `Claude_`-owned equivalents. Both may update shared documentation or catalog carefully by reconciling concurrent changes.
- **No silent promotion or integration:** Approval for a model is not permission to copy it into Sirens Went Quiet. An integration needs its own explicit request.

## Metadata and catalog

Each `model.json` uses:
- `id`: prefixed ID, e.g. `Claude_workbench_worn`.
- `base_id`: unprefixed shared brief, e.g. `workbench_worn`.
- `creator`: exactly `GPT` or `Claude`.
- `source`: matching prefixed filename, e.g. `Claude_workbench_worn.vox`.
- Existing `category`, `voxel_size_m`, `pivot_voxel`, `dimensions_m`, `occupied_voxels`, `status`, `revision`, etc.

Each `catalog.json` model record includes `id`, `base_id`, `creator`, `category`, `status`, `revision`, `source_path`, `metadata_path`, `preview_path`, and `game_integrations`. The initial catalog remains empty until actual files exist.

When adding a candidate, modify the catalog **without deleting another creator's entries**. If the branch has moved, refresh the current file and reconcile before retrying.

## Suggested review format

For each base asset:

| Base asset | GPT interpretation | Claude interpretation |
|---|---|---|
| `workbench_worn` | Actual GPT render or `not produced` | Actual Claude render or `not produced` |

Never substitute generated concept images as evidence of actual voxel geometry.

Record human decisions with the **exact ID and revision**. The final game may choose `GPT_workbench_worn` for one category and `Claude_wood_stove_compact` for another, or keep both.

## Scope and Git safety

A written pilot list is not itself an implementation order. A direct user prompt may commission one creator to produce its five candidates. Producing Claude's five does not authorize producing GPT's five, and vice versa.

Use a working branch where practical. Never force-push, merge into `main`, delete the rival's work, or modify an already approved revision without approval. Keep the library independent of all game repositories.
