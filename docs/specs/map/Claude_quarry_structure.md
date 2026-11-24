# Quarry Structures
- Asset ID: Claude_quarry_structure
- Base ID: quarry_structure
- Creator: Claude
- Category: map
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_E
- Scale family: full
- Intended uses: Regional-map destination (Construction) (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A gravel quarry's processing plant. The crusher stopped with a load still in its hopper; weeds have taken the cut rock bench and the site office door hangs open.

Condition: **abandoned**.

## Silhouette
Orange crusher on a steel frame under a flared hopper, a conveyor rising to a gravel heap, a cut rock bench.

## Dimensions and orientation
- Width (X): 15.0 m
- Depth (Y): 12.0 m
- Height (Z): 7.0 m
- Grid: 30 x 24 x 14 cells at 0.5 m (map tier), 1,751 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the street side / main entrance.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [15.0, 12.0, 0.0])
- Resolution rationale: 50 cm cells: regional-map scale, real-world metres with far fewer voxels; only massing, roofs, entrances and one identifying feature are modelled.

## Materials and colors
`almond`, `black`, `charcoal`, `concrete_dark`, `galv`, `glass_dark`, `gravel`, `khaki`, `moss`, `rust_dark`, `safety_orange_dark`, `steel`, `steel_dark`, `stone`, `stone_dark`

## Details included
- Crusher on a four-leg steel frame with a flared hopper
- Inclined conveyor feeding a rounded gravel stockpile
- Second, smaller sand pile
- Cut rock bench with weeds along the back
- Portable site office with steps

## Details excluded
- No vehicles
- No readable text

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 15.0 x 12.0 m

## Outputs
- `models/map/Claude_quarry_structure/Claude_quarry_structure.vox` (editable master)
- `models/map/Claude_quarry_structure/model.json`
- `models/map/Claude_quarry_structure/Claude_quarry_structure.glb` (derived)
- `previews/map/Claude_quarry_structure/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/e1_map_buildings.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
