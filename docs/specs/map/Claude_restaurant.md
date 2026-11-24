# Restaurant
- Asset ID: Claude_restaurant
- Base ID: restaurant
- Creator: Claude
- Category: map
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_E
- Scale family: full
- Intended uses: Regional-map destination (Food) (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A family restaurant with a timber patio. A kitchen fire burned out the camera-side end after the staff fled; the patio umbrellas were left open and one has blown over.

Condition: **abandoned**.

## Silhouette
Brick box under a grey side-gable with a small entry gable; one end scorched, timber patio with umbrellas.

## Dimensions and orientation
- Width (X): 9.0 m
- Depth (Y): 10.0 m
- Height (Z): 5.5 m
- Grid: 18 x 20 x 11 cells at 0.5 m (map tier), 1,166 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the street side / main entrance.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [9.0, 10.0, 0.0])
- Resolution rationale: 50 cm cells: regional-map scale, real-world metres with far fewer voxels; only massing, roofs, entrances and one identifying feature are modelled.

## Materials and colors
`ash_dark`, `char`, `concrete_dark`, `concrete_hi`, `cream_hi`, `cream_mid`, `glass`, `glass_dark`, `grass`, `leaf_mid`, `paint_white`, `red`, `red_dark`, `roof`, `sage`, `sage_dark`, `sage_hi`, `soot`, `steel_light`, `wgrey`, `wgrey_dark`

## Details included
- Brick walls under a grey side-gable roof with a gabled entry
- Fire-scorched end: blackened roof patch, soot over the windows, burnt-out kitchen door
- Timber patio with planters, two open umbrellas and one blown over

## Details excluded
- No readable text
- No furniture beyond umbrellas and planters

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 9.0 x 10.0 m

## Outputs
- `models/map/Claude_restaurant/Claude_restaurant.vox` (editable master)
- `models/map/Claude_restaurant/model.json`
- `models/map/Claude_restaurant/Claude_restaurant.glb` (derived)
- `previews/map/Claude_restaurant/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/e1_map_buildings.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
