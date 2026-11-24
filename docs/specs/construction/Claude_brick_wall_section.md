# Brick Wall Section
- Asset ID: Claude_brick_wall_section
- Base ID: brick_wall_section
- Creator: Claude
- Category: construction
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_B
- Scale family: full
- Intended uses: Brick tier wall 1 m (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
Garden-wall brickwork laid new by someone who knew the trade: running bond in mixed reds, a dark engineering-brick plinth, a projecting rowlock sill course at window height, a soldier course and a cast coping.

Condition: **new**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 1.0 m
- Depth (Y): 0.3 m
- Height (Z): 2.6 m
- Grid: 10 x 3 x 26 cells at 0.1 m (standard tier), 540 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the outside face; the module fills its full span.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [5.0, 1.5, 0.0])
- Resolution rationale: 10 cm cells (the game's structural grid): large silhouettes such as walls, vehicles and trees read clearly without inflating the voxel count.

## Materials and colors
`concrete`, `concrete_hi`, `maroon_dark`, `red`, `red_dark`, `red_deep`, `red_hi`, `terra`, `terra_dark`

## Details included
- Running-bond bricks at true size (0.2 x 0.1 m) with per-brick tone variation
- Two-course dark plinth
- Rowlock sill course projecting 0.1 m at 1.0 m
- Soldier course under a cast concrete coping with a front drip

## Details excluded
- No graffiti or posters

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 1.0 x 0.3 m

## Outputs
- `models/construction/Claude_brick_wall_section/Claude_brick_wall_section.vox` (editable master)
- `models/construction/Claude_brick_wall_section/model.json`
- `models/construction/Claude_brick_wall_section/Claude_brick_wall_section.glb` (derived)
- `previews/construction/Claude_brick_wall_section/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/b3_construction.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
