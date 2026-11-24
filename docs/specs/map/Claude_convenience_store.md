# Convenience Store
- Asset ID: Claude_convenience_store
- Base ID: convenience_store
- Creator: Claude
- Category: map
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_E
- Scale family: full
- Intended uses: Regional-map destination (Food) (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A corner convenience store that was looted on the second night: two of the front panes were smashed and later boarded by the owner, the ice chest is still chained by the door.

Condition: **abandoned**.

## Silhouette
Small flat-roofed box with a raised false front, blue sign band and a glazed, partly boarded shopfront.

## Dimensions and orientation
- Width (X): 8.0 m
- Depth (Y): 9.0 m
- Height (Z): 5.0 m
- Grid: 16 x 18 x 10 cells at 0.5 m (map tier), 814 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the street side / main entrance.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [8.0, 9.0, 0.0])
- Resolution rationale: 50 cm cells: regional-map scale, real-world metres with far fewer voxels; only massing, roofs, entrances and one identifying feature are modelled.

## Materials and colors
`asphalt`, `concrete_dark`, `concrete_hi`, `galv_dark`, `galv_hi`, `glass`, `glass_dark`, `label_blue`, `line_white`, `paint_white`, `pine_light`, `plaster`, `roof`, `steel_dark`

## Details included
- Flat roof behind a raised front parapet with a blank colour sign band
- Mullioned glass shopfront, two panes boarded with plywood
- Ice chest and propane cage beside the door
- Small lot with three stalls

## Details excluded
- No readable text or logo on the sign band

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 8.0 x 9.0 m

## Outputs
- `models/map/Claude_convenience_store/Claude_convenience_store.vox` (editable master)
- `models/map/Claude_convenience_store/model.json`
- `models/map/Claude_convenience_store/Claude_convenience_store.glb` (derived)
- `previews/map/Claude_convenience_store/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/e1_map_buildings.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
