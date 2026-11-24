# Small Family House
- Asset ID: Claude_small_family_house
- Base ID: small_family_house
- Creator: Claude
- Category: map
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_E
- Scale family: full
- Intended uses: Regional-map destination (Nearby Homes) (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A one-storey starter home on a small lot. The family boarded every window and left in the first week; the lawn has gone to seed around the porch.

Condition: **abandoned**.

## Silhouette
Low blue box under a steep brown side-gable, brick chimney up one gable, small porch roof on two white posts.

## Dimensions and orientation
- Width (X): 9.0 m
- Depth (Y): 9.0 m
- Height (Z): 7.0 m
- Grid: 18 x 18 x 14 cells at 0.5 m (map tier), 1,112 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the street side / main entrance.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [9.0, 9.0, 0.0])
- Resolution rationale: 50 cm cells: regional-map scale, real-world metres with far fewer voxels; only massing, roofs, entrances and one identifying feature are modelled. A 45-degree gable reads clearly as a pitched roof at map scale.

## Materials and colors
`concrete`, `concrete_dark`, `grass`, `grass_dry`, `grass_hi`, `leaf`, `paint_white`, `pine_light`, `red`, `red_dark`, `shingle_brown`, `siding_blue`, `wgrey`, `wood_stain`

## Details included
- 45-degree side-gable shingle roof with 0.5 m eaves and rakes
- Brick chimney running up the camera-side gable
- Covered porch on two white posts, door centred on the street side
- Pale plywood over every window
- Overgrown lawn, concrete path to the street

## Details excluded
- No readable text, no house number
- No interior

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 9.0 x 9.0 m

## Outputs
- `models/map/Claude_small_family_house/Claude_small_family_house.vox` (editable master)
- `models/map/Claude_small_family_house/model.json`
- `models/map/Claude_small_family_house/Claude_small_family_house.glb` (derived)
- `previews/map/Claude_small_family_house/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/e1_map_buildings.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
