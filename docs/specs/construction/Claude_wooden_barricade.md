# Wooden Barricade
- Asset ID: Claude_wooden_barricade
- Base ID: wooden_barricade
- Creator: Claude
- Category: construction
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_B
- Scale family: full
- Intended uses: Build piece 'Barricade' 1 m (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
Thrown up across a side passage on the first night: two 4x4 uprights on braced feet and every plank within reach - fence boards, a green shed board, pallet slats. A gap was left at eye height to watch the street.

Condition: **improvised**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 1.0 m
- Depth (Y): 0.4 m
- Height (Z): 2.0 m
- Grid: 20 x 8 x 40 cells at 0.05 m (detail tier), 1,062 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the outside face; the module fills its full span.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [10.0, 4.0, 0.0])
- Resolution rationale: 5 cm cells (the library's furniture/prop tier): real member thicknesses (boards, rails, cushions, doors) stay believable instead of toy-like; matches the game's 0.05 m character rig.

## Materials and colors
`break_fresh`, `iron_edge`, `pine_aged`, `pine_dark`, `pine_hi`, `pine_light`, `pine_mid`, `sage_dark`, `sage_deep`, `wgrey`, `wgrey_dark`, `wgrey_deep`, `wgrey_mid`, `wgrey_warm`

## Details included
- Two 0.1 m uprights on runner feet with diagonal braces behind
- Ten mismatched planks of different widths, lengths and sources, nailed on the outside face, gaps between some
- A viewing slot at about 1.5 m
- Split plank ends, nail heads at each upright

## Details excluded
- No barbed wire
- No sheet metal (see the reinforced barricade)

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 1.0 x 0.4 m

## Outputs
- `models/construction/Claude_wooden_barricade/Claude_wooden_barricade.vox` (editable master)
- `models/construction/Claude_wooden_barricade/model.json`
- `models/construction/Claude_wooden_barricade/Claude_wooden_barricade.glb` (derived)
- `previews/construction/Claude_wooden_barricade/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/b3_construction.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
