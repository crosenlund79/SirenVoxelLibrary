# Partially Broken Brick Wall
- Asset ID: Claude_broken_brick_wall
- Base ID: broken_brick_wall
- Creator: Claude
- Category: construction
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_B
- Scale family: full
- Intended uses: Damage reference for brick_wall_section (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
The garden wall after a vehicle clipped its top: the upper courses broke away along the mortar in steps, taking the coping with them, and the bricks lie in a heap at the foot where they fell.

Condition: **damaged**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 1.0 m
- Depth (Y): 0.7 m
- Height (Z): 2.3 m
- Grid: 10 x 7 x 23 cells at 0.1 m (standard tier), 394 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the outside face; the module fills its full span.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [5.0, 1.0, 0.0])
- Resolution rationale: 10 cm cells (the game's structural grid): large silhouettes such as walls, vehicles and trees read clearly without inflating the voxel count.

## Materials and colors
`concrete`, `concrete_dark`, `concrete_hi`, `cream_deep`, `maroon_dark`, `red`, `red_dark`, `red_deep`, `red_hi`, `terra`, `terra_dark`, `terra_hi`

## Details included
- Same bond, plinth, sill course and tones as Claude_brick_wall_section
- Upper part knocked out along a stepped break that follows the brick joints, higher at the far end, broken half-bricks on the edge
- Rubble heap at the foot, deepest under the low end: dust-dulled bricks in alternating directions, loose bricks sticking out, a lump of mortar and the broken coping at its toe
- One loosened brick pushed half out of the face

## Details excluded
- No scorch marks
- No loose single-cell confetti

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 1.0 x 0.2 m

## Outputs
- `models/construction/Claude_broken_brick_wall/Claude_broken_brick_wall.vox` (editable master)
- `models/construction/Claude_broken_brick_wall/model.json`
- `models/construction/Claude_broken_brick_wall/Claude_broken_brick_wall.glb` (derived)
- `previews/construction/Claude_broken_brick_wall/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/b3_construction.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
