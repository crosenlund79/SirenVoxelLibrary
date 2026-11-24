# Straight Road
- Asset ID: Claude_road_straight
- Base ID: road_straight
- Creator: Claude
- Category: map
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_E
- Scale family: full
- Intended uses: Regional-map infrastructure piece (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A two-lane suburban street. Years of patching show in darker squares, a pothole has opened in one lane and grass has started to creep over the sidewalk.

Condition: **worn**.

## Silhouette
Flat 8.5 m road strip: dark asphalt, yellow centre dashes, pale kerbs and sidewalks, green verges.

## Dimensions and orientation
- Width (X): 8.5 m
- Depth (Y): 16.0 m
- Height (Z): 0.5 m
- Grid: 17 x 32 x 1 cells at 0.5 m (map tier), 544 occupied voxels
- Front direction: +Y (library voxel)
- Front: Road runs along Y; +Y is an arbitrary end (the tile is symmetric).
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [8.5, 16.0, 0.0])
- Resolution rationale: 50 cm cells: regional-map scale, real-world metres with far fewer voxels; only massing, roofs, entrances and one identifying feature are modelled.

## Materials and colors
`asphalt`, `asphalt_dark`, `asphalt_deep`, `concrete_hi`, `curb`, `grass`, `grass_dry`, `iron_dark`, `line_yellow`

## Details included
- Shared road section: 2 x 2.5 m lanes, dashed yellow centre line, kerbs, sidewalks and verges
- Two patched repairs and one pothole
- Two kerb drains
- Dash phase continues across tile joints

## Details excluded
- No vehicles
- No readable markings

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 8.5 x 16.0 m

## Outputs
- `models/map/Claude_road_straight/Claude_road_straight.vox` (editable master)
- `models/map/Claude_road_straight/model.json`
- `models/map/Claude_road_straight/Claude_road_straight.glb` (derived)
- `previews/map/Claude_road_straight/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/e2_map_infrastructure.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
