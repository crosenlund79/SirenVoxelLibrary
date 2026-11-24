# Diner
- Asset ID: Claude_diner
- Base ID: diner
- Creator: Claude
- Category: map
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_E
- Scale family: full
- Intended uses: Regional-map destination (Food) (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A stainless roadside diner on the county road. Everything was left mid-shift: the booths are set, the lights are off, the place is otherwise intact.

Condition: **abandoned**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 11.0 m
- Depth (Y): 8.0 m
- Height (Z): 6.5 m
- Grid: 22 x 16 x 13 cells at 0.5 m (map tier), 917 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the street side / main entrance.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [11.0, 8.0, 0.0])
- Resolution rationale: 50 cm cells: regional-map scale, real-world metres with far fewer voxels; only massing, roofs, entrances and one identifying feature are modelled.

## Materials and colors
`asphalt`, `chrome`, `concrete_dark`, `concrete_hi`, `galv_hi`, `glass`, `glass_dark`, `grass`, `label_cream`, `line_white`, `maroon`, `paint_white`, `steel`, `steel_dark`, `steel_light`

## Details included
- Long low body with a steel skirt, continuous ribbon windows and a maroon stripe
- Softened roof crown, central glazed vestibule
- Blank sign board on a pole above the roof
- Front parking strip

## Details excluded
- No readable text or logo on the sign

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 11.0 x 8.0 m

## Outputs
- `models/map/Claude_diner/Claude_diner.vox` (editable master)
- `models/map/Claude_diner/model.json`
- `models/map/Claude_diner/Claude_diner.glb` (derived)
- `previews/map/Claude_diner/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/e1_map_buildings.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
