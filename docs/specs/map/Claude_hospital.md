# Hospital
- Asset ID: Claude_hospital
- Base ID: hospital
- Creator: Claude
- Category: map
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_E
- Scale family: full
- Intended uses: Regional-map destination (Medical) (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
The regional hospital, overwhelmed in the first week and evacuated by helicopter in the second. The ambulances were left under the emergency canopy.

Condition: **abandoned**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 20.0 m
- Depth (Y): 18.0 m
- Height (Z): 13.0 m
- Grid: 40 x 36 x 26 cells at 0.5 m (map tier), 5,686 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the street side / main entrance.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [20.0, 18.0, 0.0])
- Resolution rationale: 50 cm cells: regional-map scale, real-world metres with far fewer voxels; only massing, roofs, entrances and one identifying feature are modelled.

## Materials and colors
`asphalt`, `asphalt_dark`, `black`, `concrete`, `concrete_dark`, `concrete_hi`, `galv_hi`, `glass`, `glass_dark`, `grass`, `line_white`, `paint_white`, `plaster`, `roof`, `signal_red`, `signal_red_dark`, `steel`, `steel_dark`

## Details included
- Four-storey main tower with glazed ribbon windows and a rooftop helipad (white ring, red cross)
- Large red cross on a white panel on the tower's top storey
- Two-storey wings; emergency canopy with an ambulance on the camera-side wing
- Glazed main entrance, drop-off lot with stalls

## Details excluded
- No readable text, H marking or real-organisation emblems

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 20.0 x 18.0 m

## Outputs
- `models/map/Claude_hospital/Claude_hospital.vox` (editable master)
- `models/map/Claude_hospital/model.json`
- `models/map/Claude_hospital/Claude_hospital.glb` (derived)
- `previews/map/Claude_hospital/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/e1_map_buildings.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
