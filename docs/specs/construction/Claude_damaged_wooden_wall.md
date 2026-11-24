# Damaged Wooden Wall
- Asset ID: Claude_damaged_wooden_wall
- Base ID: damaged_wooden_wall
- Creator: Claude
- Category: construction
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_B
- Scale family: full
- Intended uses: Damage reference for wooden_wall_section (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
The same scavenged-board wall after something heavy came through it: four boards were smashed out of the left bay, the noggin behind them snapped, the pine offcut swung down on its last nail and the broken pieces still lie at the foot.

Condition: **damaged**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 1.0 m
- Depth (Y): 0.4 m
- Height (Z): 2.6 m
- Grid: 10 x 4 x 26 cells at 0.1 m (standard tier), 348 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the outside face; the module fills its full span.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [5.0, 1.0, 0.0])
- Resolution rationale: 10 cm cells (the game's structural grid): large silhouettes such as walls, vehicles and trees read clearly without inflating the voxel count.

## Materials and colors
`break_fresh`, `cream_shadow`, `iron`, `pine_aged`, `pine_dark`, `pine_light`, `pine_mid`, `sage_dark`, `sage_deep`, `siding_cream`, `snag_light`, `wgrey`, `wgrey_dark`, `wgrey_deep`, `wgrey_hi`, `wgrey_mid`, `wgrey_warm`

## Details included
- Same frame, boards and colours as Claude_wooden_wall_section
- Hole through the left bay (camera side) with ragged, fresh-coloured board ends
- Snapped noggin behind the hole
- The pine offcut hanging vertically from its last nail
- Top board torn off at one corner, top plate showing
- Broken board pieces lying and leaning against the foot of the wall (attached)

## Details excluded
- No fire damage
- No loose confetti debris

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 1.0 x 0.2 m

## Outputs
- `models/construction/Claude_damaged_wooden_wall/Claude_damaged_wooden_wall.vox` (editable master)
- `models/construction/Claude_damaged_wooden_wall/model.json`
- `models/construction/Claude_damaged_wooden_wall/Claude_damaged_wooden_wall.glb` (derived)
- `previews/construction/Claude_damaged_wooden_wall/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/b3_construction.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
