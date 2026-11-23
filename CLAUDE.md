# Claude Instructions — SirenVoxelLibrary

This is an **independent voxel art repository**, not the Sirens Went Quiet game. Your job is to produce **original, coherent, editable 3D voxel assets** when the user explicitly commissions them.

## Read before acting

1. `README.md` — purpose and navigation.
2. `docs/VOXEL_ART_BIBLE.md` — authoritative style, scale, palette and resolution guidance.
3. `docs/MODEL_SPEC_TEMPLATE.md` — model briefs and acceptance checks.
4. `docs/EXPORT_RULES.md` — real `.vox` source, metadata, previews, derived `.glb` and validation.
5. `docs/REVIEW_PROCESS.md` — candidate/approval/integration responsibilities.
6. `docs/PILOT_BATCH.md` — **proposed** first five objects, not automatically authorized.
7. `docs/RIVAL_WORKFLOW.md` — **mandatory GPT_ / Claude_ ownership and comparison conventions**.
8. `viewer/README.md` — built-in read-only `.vox` inspector for creator review.

## Required preflight

- Verify repository identity, branch and clean/dirty status. Preserve unrelated work.
- Identify the **specific user-approved batch** for the current instruction; a proposed list in docs is not authorization.
- You are **Claude** in a friendly model-making rivalry. Only author models named `Claude_<base_id>` (exact case); ChatGPT owns the `GPT_` namespace. For the first batch, follow the identical shared briefs independently; do not copy GPT's voxel data, generator implementation, or final geometry.
- Never create, overwrite, move, or remove `GPT_` model assets, specs, or previews. If GPT models already exist, preserve them. Shared catalog entries must be merged safely.
- Work in a suitable working branch; don't overwrite previously approved source, push to main, merge or copy into game repos without user approval.
- Make a concise plan and state what will be produced and how it will be verified.
- Check available tools before promising actual MagicaVoxel or Godot GUI verification.

## Making models

- Build physically plausible 3D voxel geometry, **not PNG concept images or ordinary uneditable GLBs**.
- Generate real MagicaVoxel-compatible `.vox` files with actual cell occupancy, palette and bounds.
- Canonical source names are `Claude_<base_id>.vox` inside `models/<category>/Claude_<base_id>/`, with matching `Claude_<base_id>.glb` only if exported. Keep `model.json` in that directory and previews in `previews/<category>/Claude_<base_id>/`.
- Metadata must record `creator: "Claude"`, `base_id`, prefixed `id` and matching prefixed `source` filename. Add only actual candidates to the catalog; preserve existing GPT records.
- Prefer reproducible generator scripts where it improves iteration; keep source files editable and recognizable without the generator.
- Work at the coarsest resolution that supports recognizable details. Choose resolution separately for each model.
- Create corresponding `model.json` records, actual renders, and an updated `catalog.json` with status `candidate`.
- Use `viewer/index.html` for a quick visual inspection of the genuine `.vox` output where a browser is available. It is a convenience viewer, not a format validator and not a replacement for generated preview files or actual MagicaVoxel compatibility testing.
- If exporting `.glb`, derive it from the VOX source and verify orientation, scale and colors. Do not claim Godot integration without testing it.
- Use compatible, documented software available in the environment. If a GUI is not available, validate the VOX structure with a parser and mark external-editor verification pending.
- Keep the library free of unnecessary game logic and tool infrastructure.

## Review boundary

- **Only the user approves a candidate.** Never promote it to `approved` merely because scripts/tests pass.
- Produce a review-ready contact sheet named `Claude_<batch_id>.png` and honest evidence of each actual model. Present side-by-side comparisons only if actual GPT models already exist; do not fabricate GPT results.
- Never automatically transfer assets to Sirens Went Quiet or any other game.
- Treat requested revisions as new proposals against the previously approved revision; no silent replacement.

## Delivery

Commit/push the user-approved work to the authorized branch and report:
- Model IDs, format files and locations.
- Each model's cell size, dimensions and occupied voxel count.
- How previews were produced.
- Validation/tests passed and unverified checks.
- Any visual shortcomings or model-specific compromises.
- Exact branch/commit and the review sheet.
- Explicitly state that assets remain **Candidates** unless the user approved them.
