# Stone Foundation
- Asset ID: Claude_stone_foundation
- Base ID: stone_foundation
- Creator: Claude
- Category: construction
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_B
- Scale family: full
- Intended uses: Stone foundation module (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A levelled fieldstone footing block from the same mason: rough stones on the sides, the top dressed flat with big flags so a floor frame can sit on it.

Condition: **new**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 1.0 m
- Depth (Y): 1.0 m
- Height (Z): 0.3 m
- Grid: 10 x 10 x 3 cells at 0.1 m (standard tier), 233 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the outside face; the module fills its full span.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [5.0, 5.0, 0.0])
- Resolution rationale: 10 cm cells (the game's structural grid): large silhouettes such as walls, vehicles and trees read clearly without inflating the voxel count.

## Materials and colors
`bark_hi`, `concrete`, `concrete_dark`, `concrete_deep`, `cream_deep`, `cream_mid`, `stone`, `stone_dark`, `wgrey`, `wgrey_warm`

## Details included
- One course of full-height fieldstones on all four sides, lime mortar joints open to the top
- Flat top: four large flags with flush joints inside the ring of side stones
- Flag layout repeats every 1 m in both directions so modules tile

## Details excluded
- No moss (new)

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 1.0 x 1.0 m

## Outputs
- `models/construction/Claude_stone_foundation/Claude_stone_foundation.vox` (editable master)
- `models/construction/Claude_stone_foundation/model.json`
- `models/construction/Claude_stone_foundation/Claude_stone_foundation.glb` (derived)
- `previews/construction/Claude_stone_foundation/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/b3_construction.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
