# Hardware Store
- Asset ID: Claude_hardware_store
- Base ID: hardware_store
- Creator: Claude
- Category: map
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_E
- Scale family: full
- Intended uses: Regional-map destination (Hardware Store (current destination)) (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
The town hardware store, stripped of generators, fuel cans and tarps early on. The lumber yard behind the fence was left nearly full; the gate chain was cut.

Condition: **abandoned**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 13.0 m
- Depth (Y): 11.0 m
- Height (Z): 7.0 m
- Grid: 26 x 22 x 14 cells at 0.5 m (map tier), 1,597 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the street side / main entrance.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [13.0, 11.0, 0.0])
- Resolution rationale: 50 cm cells: regional-map scale, real-world metres with far fewer voxels; only massing, roofs, entrances and one identifying feature are modelled.

## Materials and colors
`asphalt`, `beige`, `card`, `concrete_dark`, `concrete_hi`, `galv`, `galv_dark`, `galv_hi`, `glass`, `glass_dark`, `grass`, `gravel`, `green`, `green_dark`, `khaki`, `khaki_dark`, `leaf`, `leaf_mid`, `line_white`, `pine_light`, `pine_mid`, `roof`, `sawdust`, `steel_dark`

## Details included
- Flat-roofed store with a stepped false front and a blank green sign band
- Glazed front under a metal awning, bagged soil on the sidewalk
- Fenced side yard with a lean-to lumber rack, a stacked lumber pile and plant pallets
- Gate standing open on the street side

## Details excluded
- No readable text or logo

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 13.0 x 11.0 m

## Outputs
- `models/map/Claude_hardware_store/Claude_hardware_store.vox` (editable master)
- `models/map/Claude_hardware_store/model.json`
- `models/map/Claude_hardware_store/Claude_hardware_store.glb` (derived)
- `previews/map/Claude_hardware_store/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/e1_map_buildings.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
