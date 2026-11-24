# Intersection
- Asset ID: Claude_road_intersection
- Base ID: road_intersection
- Creator: Claude
- Category: map
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_E
- Scale family: full
- Intended uses: Regional-map infrastructure piece (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A four-way junction at the centre of the subdivision. The traffic lights were on another tile; here only the zebra crossings and the corner kerbs remain, worn white where buses turned.

Condition: **worn**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 12.5 m
- Depth (Y): 12.5 m
- Height (Z): 0.5 m
- Grid: 25 x 25 x 1 cells at 0.5 m (map tier), 625 occupied voxels
- Front direction: +Y (library voxel)
- Front: Symmetric; arms leave every edge centred like the straight tile.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [12.5, 12.5, 0.0])
- Resolution rationale: 50 cm cells: regional-map scale, real-world metres with far fewer voxels; only massing, roofs, entrances and one identifying feature are modelled.

## Materials and colors
`asphalt`, `asphalt_dark`, `concrete_hi`, `curb`, `grass`, `line_white`

## Details included
- Four arms with the shared road section
- Zebra crossing on every arm
- Rounded kerb corners (1 m radius) with sidewalks wrapping the corners
- Grass corner squares, one patched arm

## Details excluded
- No signals or signs
- No readable markings

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 12.5 x 12.5 m

## Outputs
- `models/map/Claude_road_intersection/Claude_road_intersection.vox` (editable master)
- `models/map/Claude_road_intersection/model.json`
- `models/map/Claude_road_intersection/Claude_road_intersection.glb` (derived)
- `previews/map/Claude_road_intersection/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/e2_map_infrastructure.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
