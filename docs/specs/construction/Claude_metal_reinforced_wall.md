# Metal-Reinforced Wall
- Asset ID: Claude_metal_reinforced_wall
- Base ID: metal_reinforced_wall
- Creator: Claude
- Category: construction
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_B
- Scale family: full
- Intended uses: Upgrade 'Metal sheathing' (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
The scavenged-board wall after its owners got scared: they bolted whatever steel they could carry over the outside - a galvanised roofing sheet, a rusty plate and an old almond appliance panel - and left the top boards bare.

Condition: **improvised**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 1.0 m
- Depth (Y): 0.3 m
- Height (Z): 2.6 m
- Grid: 10 x 3 x 26 cells at 0.1 m (standard tier), 538 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the outside face; the module fills its full span.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [5.0, 1.5, 0.0])
- Resolution rationale: 10 cm cells (the game's structural grid): large silhouettes such as walls, vehicles and trees read clearly without inflating the voxel count.

## Materials and colors
`almond`, `almond_dark`, `cream_shadow`, `galv`, `galv_dark`, `galv_hi`, `iron_warm`, `pine_aged`, `pine_dark`, `pine_light`, `pine_mid`, `rust_dark`, `rust_deep`, `sage_dark`, `sage_deep`, `siding_cream`, `steel`, `steel_dark`, `steel_light`, `wgrey`, `wgrey_dark`, `wgrey_deep`, `wgrey_hi`, `wgrey_mid`, `wgrey_warm`

## Details included
- Same timber frame and boards as Claude_wooden_wall_section behind
- Corrugated galvanised sheet (vertical ribs) over the lower camera-side bay
- Rusty steel plate lapping it, rust bleeding from its bolts
- Old almond appliance panel higher up, bare boards visible above and between
- Bolt heads in rows on the stud lines

## Details excluded
- No barbed wire
- No graffiti

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 1.0 x 0.3 m

## Outputs
- `models/construction/Claude_metal_reinforced_wall/Claude_metal_reinforced_wall.vox` (editable master)
- `models/construction/Claude_metal_reinforced_wall/model.json`
- `models/construction/Claude_metal_reinforced_wall/Claude_metal_reinforced_wall.glb` (derived)
- `previews/construction/Claude_metal_reinforced_wall/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/b3_construction.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
