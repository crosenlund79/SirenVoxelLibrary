# Stone Wall Section
- Asset ID: Claude_stone_wall_section
- Base ID: stone_wall_section
- Creator: Claude
- Category: construction
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_B
- Scale family: full
- Intended uses: Stone tier wall 1 m (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A new wall of local fieldstone laid by a mason who sorted every load: big stones at the foot, long flat ones on top, set proud of a light lime mortar.

Condition: **new**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 1.0 m
- Depth (Y): 0.3 m
- Height (Z): 2.6 m
- Grid: 10 x 3 x 26 cells at 0.1 m (standard tier), 520 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the outside face; the module fills its full span.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [5.0, 1.5, 0.0])
- Resolution rationale: 10 cm cells (the game's structural grid): large silhouettes such as walls, vehicles and trees read clearly without inflating the voxel count.

## Materials and colors
`bark_hi`, `concrete`, `concrete_dark`, `concrete_deep`, `cream_mid`, `stone`, `stone_dark`, `wgrey`, `wgrey_warm`

## Details included
- Random-coursed fieldstone, stones 0.2-0.5 m in varied grey-brown tones
- Stones stand 0.1 m proud of recessed light lime mortar beds and head joints
- Larger stones have clipped corners so they read rounded, not squared
- Both faces built; long flat cap stones on top
- Course pattern repeats every 1 m so modules continue the wall

## Details excluded
- No moss or graffiti (new wall)

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 1.0 x 0.3 m

## Outputs
- `models/construction/Claude_stone_wall_section/Claude_stone_wall_section.vox` (editable master)
- `models/construction/Claude_stone_wall_section/model.json`
- `models/construction/Claude_stone_wall_section/Claude_stone_wall_section.glb` (derived)
- `previews/construction/Claude_stone_wall_section/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/b3_construction.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
