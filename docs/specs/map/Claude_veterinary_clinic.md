# Veterinary Clinic
- Asset ID: Claude_veterinary_clinic
- Base ID: veterinary_clinic
- Creator: Claude
- Category: map
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_E
- Scale family: full
- Intended uses: Regional-map destination (Medical) (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A small-town vet in a converted house. Before leaving, the staff opened the kennels and the dog-run gate so the boarders could fend for themselves.

Condition: **abandoned**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 10.0 m
- Depth (Y): 10.0 m
- Height (Z): 7.0 m
- Grid: 20 x 20 x 14 cells at 0.5 m (map tier), 1,214 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the street side / main entrance.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [10.0, 10.0, 0.0])
- Resolution rationale: 50 cm cells: regional-map scale, real-world metres with far fewer voxels; only massing, roofs, entrances and one identifying feature are modelled.

## Materials and colors
`asphalt`, `black`, `concrete_dark`, `concrete_hi`, `galv_dark`, `glass`, `glass_dark`, `grass`, `gravel`, `label_blue`, `line_white`, `paint_white`, `red_dark`, `roof`, `siding_sage`, `steel_dark`, `steel_light`, `wgrey_warm`, `wood_stain`

## Details included
- Sage-sided building with a 45-degree front gable and entrance canopy
- Fenced gravel dog run on the camera side with a red-roofed dog house
- Dog-run gate standing open
- Two parking stalls and a low blank sign

## Details excluded
- No readable text, paw logos or animals

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 10.0 x 10.0 m

## Outputs
- `models/map/Claude_veterinary_clinic/Claude_veterinary_clinic.vox` (editable master)
- `models/map/Claude_veterinary_clinic/model.json`
- `models/map/Claude_veterinary_clinic/Claude_veterinary_clinic.glb` (derived)
- `previews/map/Claude_veterinary_clinic/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/e1_map_buildings.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
