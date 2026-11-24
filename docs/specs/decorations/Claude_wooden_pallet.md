# Wooden Pallet
- Asset ID: Claude_wooden_pallet
- Base ID: wooden_pallet
- Creator: Claude
- Category: decorations
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_D
- Scale family: full
- Intended uses: Building material / prop (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A stringer pallet that sat out behind a shop for a year. The boards have gone grey, one top board split along its length and lost a corner when it was dropped, and an earlier repair left one fresh pale board.

Condition: **worn**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 1.125 m
- Depth (Y): 0.8 m
- Height (Z): 0.15 m
- Grid: 45 x 32 x 6 cells at 0.025 m (fine tier), 2,193 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y faces the street or the person using it.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [22.5, 16.0, 0.0])
- Resolution rationale: 2.5 cm cells: a handheld or small gear item whose handles, straps and blades would be 2-4x too thick at 5 cm. Deck boards are 2.5 cm thick; at 5 cm the pallet becomes three thick slabs.

## Materials and colors
`break_fresh`, `pine_light`, `pine_mid`, `wgrey`, `wgrey_dark`, `wgrey_deep`, `wgrey_hi`, `wgrey_mid`

## Details included
- Three notched stringers along X with fork notches
- Seven top deck boards and three bottom boards
- One top board split lengthwise with a broken-off corner, pale wood at the break
- One newer replacement board

## Details excluded
- No stamps or markings
- No nail heads

## Construction and placement notes
- Collision suggestion: Box 1.12 x 0.8 x 0.15 m.
- Placement footprint: 1.125 x 0.8 m

## Outputs
- `models/decorations/Claude_wooden_pallet/Claude_wooden_pallet.vox` (editable master)
- `models/decorations/Claude_wooden_pallet/model.json`
- `models/decorations/Claude_wooden_pallet/Claude_wooden_pallet.glb` (derived)
- `previews/decorations/Claude_wooden_pallet/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/d2_street.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
