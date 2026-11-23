# Candidate, Approval and Integration Workflow

The workshop is independent of any game. Asset creation, creative approval, and adoption into a game are three **different decisions**.

## States

- **Proposed** — an idea or brief only. No asset implied.
- **Candidate** — real editable `.vox` source and previews exist for review.
- **Approved** — the user explicitly accepts a particular model revision for the library.
- **Rejected** — not accepted; keep history, remove from the normal approved selection.
- **Integrated** — a specific approved revision has been copied into a named game and verified there. Track integration *per game*; integration does not replace the library's approval state.

The catalog's `status` field is `candidate`, `approved`, or `rejected`; `game_integrations` is an independent array. A proposed model may live in `docs/specs/` without a catalog record.

## Model journey

1. **Describe** it with `docs/MODEL_SPEC_TEMPLATE.md` and choose a coherent provisional resolution.
2. **Generate** editable source and a complete preview set. Candidate status only.
3. **Validate** file format, dimensions, palette, connectivity, forward/pivot and, if relevant, derived GLB.
4. **Show** a consistent contact sheet with model name, size in metres, voxel resolution, occupied count and category.
5. **Review** aesthetics and practicality. Record user's feedback clearly, without arguing that an automated test proves it looks good.
6. **Approve or revise**. Only the user's explicit instruction changes a model to Approved.
7. **Selectively integrate** a particular approved revision into a game when separately requested.

## Protect approved work

- Never silently replace or significantly restyle an approved asset.
- For a proposed revision, keep the prior approved commit identifiable. Prepare changes on a working branch or in an isolated proposal, and show before/after previews.
- Record revision number and source commit in approval history.
- Do not retroactively change acceptance status just because Claude generated a newer file.
- A model can be Approved and not integrated anywhere; this is normal.

## Catalog rules

`catalog.json` is the searchable inventory of **actual generated assets**. Do not add speculative assets as if they exist. Required record fields: `id`, `base_id`, `creator`, `name`, `category`, `status`, `revision`, `source_path`, `metadata_path`, `preview_path`, `game_integrations`. Append each candidate independently. Never remove or overwrite another creator's record when updating the shared catalog.

Model IDs: **case-sensitive** `GPT_<base_id>` or `Claude_<base_id>`, with `<base_id>` in lowercase `snake_case`; unique and stable. The prefixes identify creator, not winner. Categories initially: `furniture`, `survival`, `vegetation`, `vehicles`, `decorations`, `architecture`. Expand categories only when helpful.

## Rival review

For each shared base ID, present the GPT and Claude versions at the same world scale, lighting and camera angles. If only one exists, label the other **not yet produced**; never invent results. Compare art quality, silhouette, materials, technical validity and performance pragmatically. The user may approve either, both, neither or request a new interpretation. See `docs/RIVAL_WORKFLOW.md`.

## First review standard

Do not manufacture dozens of objects to prove productivity. Produce at most a few representative candidates, inspect their render quality at game camera distance, fix the *art bible* if necessary, then scale up.

A category may need its own resolution and design examples, but all categories must share the coordinate, color-family, preview and approval conventions.

## Ownership and scope

Design instructions and proposed work in this repository are **not automatic authorization**. Claude must work only on the model(s) the user explicitly requests. It must not write into other game repositories unless the user separately approves a specific transfer.
