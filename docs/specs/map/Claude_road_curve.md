# Road Curve
- Asset ID: Claude_road_curve
- Base ID: road_curve
- Creator: Claude
- Category: map
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_E
- Scale family: full
- Intended uses: Regional-map infrastructure piece (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A 90-degree bend where the street turns along the creek. Drivers cut the corner for years and wore the inside verge bare; the outer lane is patched.

Condition: **worn**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 12.5 m
- Depth (Y): 12.5 m
- Height (Z): 0.5 m
- Grid: 25 x 25 x 1 cells at 0.5 m (map tier), 625 occupied voxels
- Front direction: +Y (library voxel)
- Front: Road enters at the +Y edge and leaves at the -X edge, centred on each edge like the straight tile.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [12.5, 12.5, 0.0])
- Resolution rationale: 50 cm cells: regional-map scale, real-world metres with far fewer voxels; only massing, roofs, entrances and one identifying feature are modelled.

## Materials and colors
`asphalt`, `concrete_hi`, `curb`, `grass`, `grass_dry`, `line_yellow`

## Details included
- Same section as the straight tile, swept around a 6.25 m centre-line radius
- Two dashes per bend so the dash rhythm meets the straight tiles
- Patched outer lane, worn inside verge

## Details excluded
- No vehicles
- No readable markings

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 12.5 x 12.5 m

## Outputs
- `models/map/Claude_road_curve/Claude_road_curve.vox` (editable master)
- `models/map/Claude_road_curve/model.json`
- `models/map/Claude_road_curve/Claude_road_curve.glb` (derived)
- `previews/map/Claude_road_curve/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/e2_map_infrastructure.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
