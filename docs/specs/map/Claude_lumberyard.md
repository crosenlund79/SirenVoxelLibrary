# Lumberyard / Sawmill
- Asset ID: Claude_lumberyard
- Base ID: lumberyard
- Creator: Claude
- Category: map
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_E
- Scale family: full
- Intended uses: Regional-map destination (Construction) (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A family sawmill at the edge of the woods. The last log is still on the carriage under the saw; the yard crew stacked the week's boards and never came back for them.

Condition: **abandoned**.

## Silhouette
Open metal-roofed saw shed with an inclined conveyor to a sawdust heap, a log pyramid and pale lumber bundles.

## Dimensions and orientation
- Width (X): 15.0 m
- Depth (Y): 14.0 m
- Height (Z): 5.5 m
- Grid: 30 x 28 x 11 cells at 0.5 m (map tier), 1,982 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the street side / main entrance.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [15.0, 14.0, 0.0])
- Resolution rationale: 50 cm cells: regional-map scale, real-world metres with far fewer voxels; only massing, roofs, entrances and one identifying feature are modelled.

## Materials and colors
`bark`, `bark_mid`, `black`, `break_fresh`, `concrete`, `galv`, `galv_dark`, `galv_hi`, `gravel`, `hazard_yellow_dark`, `pine_light`, `pine_mid`, `sawdust`, `snag_light`, `soil`, `steel`, `steel_dark`, `wgrey_dark`

## Details included
- Open-sided saw shed with a low metal gable roof and a closed back wall
- Carriage, log and saw housing inside the shed
- Inclined chip conveyor out of the camera-side end onto a sawdust heap
- Log deck stacked end-on to the street with pale cut ends
- Strapped lumber bundles on a rutted loading area

## Details excluded
- No vehicles
- No readable text

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 15.0 x 14.0 m

## Outputs
- `models/map/Claude_lumberyard/Claude_lumberyard.vox` (editable master)
- `models/map/Claude_lumberyard/model.json`
- `models/map/Claude_lumberyard/Claude_lumberyard.glb` (derived)
- `previews/map/Claude_lumberyard/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/e1_map_buildings.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
