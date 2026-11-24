# Reinforced Wooden Barricade
- Asset ID: Claude_reinforced_wooden_barricade
- Base ID: reinforced_wooden_barricade
- Creator: Claude
- Category: construction
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_B
- Scale family: full
- Intended uses: Upgraded barricade (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
The side-passage barricade after a bad week: rebuilt on three uprights with a second layer of boards, propped from behind, and patched with whatever steel turned up - a corrugated garage panel and a rusty plate - bolted through.

Condition: **improvised**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 1.0 m
- Depth (Y): 0.5 m
- Height (Z): 2.05 m
- Grid: 20 x 10 x 41 cells at 0.05 m (detail tier), 2,236 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the outside face; the module fills its full span.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [10.0, 4.5, 0.0])
- Resolution rationale: 5 cm cells (the library's furniture/prop tier): real member thicknesses (boards, rails, cushions, doors) stay believable instead of toy-like; matches the game's 0.05 m character rig.

## Materials and colors
`break_fresh`, `galv`, `galv_dark`, `galv_hi`, `iron_edge`, `iron_warm`, `pine_aged`, `pine_dark`, `pine_light`, `pine_mid`, `rust_deep`, `sage_dark`, `sage_deep`, `steel`, `steel_dark`, `steel_light`, `wgrey`, `wgrey_dark`, `wgrey_deep`, `wgrey_mid`, `wgrey_warm`, `wood_stain`

## Details included
- Three uprights, each propped by a heavy angled strut to a ground block
- Double planking: vertical boards behind, horizontal planks in front
- Corrugated galvanised sheet and a rusty steel plate bolted over the planks
- Viewing slot cut through all layers at about 1.7 m
- Uneven board tops above the frame

## Details excluded
- No barbed wire
- No firing ports or weapons

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 1.0 x 0.45 m

## Outputs
- `models/construction/Claude_reinforced_wooden_barricade/Claude_reinforced_wooden_barricade.vox` (editable master)
- `models/construction/Claude_reinforced_wooden_barricade/model.json`
- `models/construction/Claude_reinforced_wooden_barricade/Claude_reinforced_wooden_barricade.glb` (derived)
- `previews/construction/Claude_reinforced_wooden_barricade/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/b3_construction.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
