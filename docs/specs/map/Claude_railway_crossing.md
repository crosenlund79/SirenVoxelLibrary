# Railway Crossing
- Asset ID: Claude_railway_crossing
- Base ID: railway_crossing
- Creator: Claude
- Category: map
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_E
- Scale family: full
- Intended uses: Regional-map infrastructure piece (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A level crossing on the freight line out of town. The barriers came down when the power failed and have stayed down ever since.

Condition: **worn**.

## Silhouette
Road tile crossed by a ballasted track with raised rails, two signal posts and striped barrier arms down.

## Dimensions and orientation
- Width (X): 12.5 m
- Depth (Y): 12.5 m
- Height (Z): 4.0 m
- Grid: 25 x 25 x 8 cells at 0.5 m (map tier), 693 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the street side / main entrance.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [12.5, 12.5, 0.0])
- Resolution rationale: 50 cm cells: regional-map scale, real-world metres with far fewer voxels; only massing, roofs, entrances and one identifying feature are modelled.

## Materials and colors
`asphalt`, `charcoal`, `concrete_dark`, `concrete_hi`, `curb`, `galv`, `galv_dark`, `galv_hi`, `grass`, `gravel`, `lamp_red`, `line_yellow`, `paint_white`, `signal_red`, `steel`, `steel_light`, `wood_stain`

## Details included
- Shared road section along Y crossed by a single track along X
- Ballast bed with timber sleepers, raised rails off the road and flush rails in the crossing panels
- Two crossing signals with paired red lamps and striped barrier arms lowered across the approach lanes
- Relay cabinet beside one signal

## Details excluded
- No readable signs or crossbuck text
- No train

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 12.5 x 12.5 m

## Outputs
- `models/map/Claude_railway_crossing/Claude_railway_crossing.vox` (editable master)
- `models/map/Claude_railway_crossing/model.json`
- `models/map/Claude_railway_crossing/Claude_railway_crossing.glb` (derived)
- `previews/map/Claude_railway_crossing/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/e2_map_infrastructure.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
