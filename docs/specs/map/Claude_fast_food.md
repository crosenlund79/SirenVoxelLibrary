# Fast-Food Restaurant
- Asset ID: Claude_fast_food
- Base ID: fast_food
- Creator: Claude
- Category: map
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_E
- Scale family: full
- Intended uses: Regional-map destination (Food) (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A drive-through burger restaurant at the edge of the strip. The drive-through lane is still marked, the menu board is blank and the tall pole sign has been dark since the power went.

Condition: **abandoned**.

## Silhouette
Compact box under a projecting terracotta mansard band, wrapped by a drive-through lane, tall empty pole sign.

## Dimensions and orientation
- Width (X): 9.0 m
- Depth (Y): 10.0 m
- Height (Z): 6.0 m
- Grid: 18 x 20 x 12 cells at 0.5 m (map tier), 807 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the street side / main entrance.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [9.0, 10.0, 0.0])
- Resolution rationale: 50 cm cells: regional-map scale, real-world metres with far fewer voxels; only massing, roofs, entrances and one identifying feature are modelled.

## Materials and colors
`asphalt`, `asphalt_dark`, `charcoal`, `concrete_dark`, `concrete_hi`, `curb`, `galv_hi`, `glass`, `glass_dark`, `grass`, `line_white`, `line_yellow`, `plaster`, `roof`, `steel`, `steel_dark`, `terra`, `terra_dark`

## Details included
- Flat-roofed box with a terracotta mansard band
- Drive-through lane wrapping the +X side with a pick-up window canopy and a blank menu board
- Tall pole sign with a blank dark panel
- Glazed front, parking stalls

## Details excluded
- No readable text or logo

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 9.0 x 10.0 m

## Outputs
- `models/map/Claude_fast_food/Claude_fast_food.vox` (editable master)
- `models/map/Claude_fast_food/model.json`
- `models/map/Claude_fast_food/Claude_fast_food.glb` (derived)
- `previews/map/Claude_fast_food/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/e1_map_buildings.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
