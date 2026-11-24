# Wooden Wall Section
- Asset ID: Claude_wooden_wall_section
- Base ID: wooden_wall_section
- Creator: Claude
- Category: construction
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_B
- Scale family: full
- Intended uses: Build piece 'Wooden wall' 1 m (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
Put up in an afternoon by survivors closing a gap between two houses: a 2x4 frame with whatever boards the street gave them - fence pickets gone grey, offcuts of fresh pine, a strip of cream siding and a green board from a garden shed.

Condition: **improvised**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 1.0 m
- Depth (Y): 0.2 m
- Height (Z): 2.6 m
- Grid: 10 x 2 x 26 cells at 0.1 m (standard tier), 357 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the outside face; the module fills its full span.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [5.0, 1.0, 0.0])
- Resolution rationale: 10 cm cells (the game's structural grid): large silhouettes such as walls, vehicles and trees read clearly without inflating the voxel count.

## Materials and colors
`cream_shadow`, `pine_aged`, `pine_dark`, `pine_light`, `pine_mid`, `sage_dark`, `sage_deep`, `siding_cream`, `wgrey`, `wgrey_dark`, `wgrey_deep`, `wgrey_hi`, `wgrey_mid`, `wgrey_warm`

## Details included
- Studs, bottom and top plate and staggered noggins on the inside (-Y) face
- Thirteen horizontal boards two cells (0.2 m) tall on the outside (+Y), mismatched by origin, two butt-jointed on the middle stud
- Nail heads on every stud line
- One board end stops short of the right edge, showing the stud behind

## Details excluded
- No paint graffiti or text
- No window or door cut-out (separate modules)

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 1.0 x 0.2 m

## Outputs
- `models/construction/Claude_wooden_wall_section/Claude_wooden_wall_section.vox` (editable master)
- `models/construction/Claude_wooden_wall_section/model.json`
- `models/construction/Claude_wooden_wall_section/Claude_wooden_wall_section.glb` (derived)
- `previews/construction/Claude_wooden_wall_section/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/b3_construction.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
