# Medical Clinic
- Asset ID: Claude_clinic
- Base ID: clinic
- Creator: Claude
- Category: map
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_E
- Scale family: full
- Intended uses: Regional-map destination (Medical Clinic (current destination)) (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
The walk-in medical clinic where people queued for days after the sirens stopped. The ambulance under the canopy never left; the doors are chained from inside.

Condition: **abandoned**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 11.0 m
- Depth (Y): 11.0 m
- Height (Z): 6.0 m
- Grid: 22 x 22 x 12 cells at 0.5 m (map tier), 1,330 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the street side / main entrance.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [11.0, 11.0, 0.0])
- Resolution rationale: 50 cm cells: regional-map scale, real-world metres with far fewer voxels; only massing, roofs, entrances and one identifying feature are modelled.

## Materials and colors
`asphalt`, `asphalt_dark`, `black`, `bluegrey`, `concrete_dark`, `concrete_hi`, `galv_hi`, `glass`, `glass_dark`, `lamp_red`, `line_white`, `paint_white`, `plaster`, `roof`, `signal_red`, `steel`

## Details included
- Single-storey flat-roofed clinic with a raised entrance tower
- White sign panel with a red cross on the tower
- Ambulance canopy on two posts over the side bay, ambulance parked under it
- Front parking stalls and a kerbed walk

## Details excluded
- No readable text or real-organisation emblems

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 11.0 x 11.0 m

## Outputs
- `models/map/Claude_clinic/Claude_clinic.vox` (editable master)
- `models/map/Claude_clinic/model.json`
- `models/map/Claude_clinic/Claude_clinic.glb` (derived)
- `previews/map/Claude_clinic/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/e1_map_buildings.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
