# Industrial Warehouse
- Asset ID: Claude_industrial_warehouse
- Base ID: industrial_warehouse
- Creator: Claude
- Category: map
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_E
- Scale family: full
- Intended uses: Regional-map destination (Construction) (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A distribution warehouse on the industrial estate. Two loading doors are still locked; the middle one was torn open by a truck that reversed straight through it.

Condition: **abandoned**.

## Silhouette
Big corrugated front-gabled shed with three tall loading doors (one torn open) and ridge ventilators.

## Dimensions and orientation
- Width (X): 18.0 m
- Depth (Y): 14.0 m
- Height (Z): 10.5 m
- Grid: 36 x 28 x 21 cells at 0.5 m (map tier), 3,780 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the street side / main entrance.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [18.0, 14.0, 0.0])
- Resolution rationale: 50 cm cells: regional-map scale, real-world metres with far fewer voxels; only massing, roofs, entrances and one identifying feature are modelled.

## Materials and colors
`black`, `concrete`, `concrete_dark`, `galv`, `galv_dark`, `galv_hi`, `glass_dark`, `gravel`, `green`, `green_dark`, `hazard_yellow_dark`, `roof_hi`, `steel`, `steel_dark`

## Details included
- Corrugated steel walls on a concrete base, panel seams every 2 m
- Low-pitch front gable with a louvre, ridge ventilators
- Three 3 m loading doors, the middle one torn open with its panel hanging
- Clerestory windows, yellow bollards, a skip on the apron

## Details excluded
- No readable text or logo

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 18.0 x 14.0 m

## Outputs
- `models/map/Claude_industrial_warehouse/Claude_industrial_warehouse.vox` (editable master)
- `models/map/Claude_industrial_warehouse/model.json`
- `models/map/Claude_industrial_warehouse/Claude_industrial_warehouse.glb` (derived)
- `previews/map/Claude_industrial_warehouse/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/e1_map_buildings.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
