# Scrapyard
- Asset ID: Claude_scrapyard_building
- Base ID: scrapyard_building
- Creator: Claude
- Category: map
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_E
- Scale family: full
- Intended uses: Regional-map destination (Construction) (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A salvage yard behind a wall of patched sheet metal. The crane still holds its magnet over the stack it was sorting; the office door was kicked in for the cash box.

Condition: **abandoned**.

## Silhouette
Patchwork sheet-metal enclosure with stacked car hulks, a yellow mast-and-jib crane and a yellow office cabin.

## Dimensions and orientation
- Width (X): 13.0 m
- Depth (Y): 10.0 m
- Height (Z): 6.5 m
- Grid: 26 x 20 x 13 cells at 0.5 m (map tier), 1,337 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the street side / main entrance.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [13.0, 10.0, 0.0])
- Resolution rationale: 50 cm cells: regional-map scale, real-world metres with far fewer voxels; only massing, roofs, entrances and one identifying feature are modelled.

## Materials and colors
`beige_dark`, `black`, `charcoal`, `concrete_dark`, `galv`, `galv_dark`, `glass_dark`, `glass_deep`, `gravel`, `hazard_yellow`, `hazard_yellow_dark`, `iron_edge`, `maroon_dark`, `mesh`, `navy_dark`, `rust`, `rust_dark`, `rust_deep`, `siding_yellow`, `soil_dark`, `steel`, `steel_dark`, `teal_dark`, `wgrey_dark`

## Details included
- Patchwork fence of salvaged sheets, rolling gate pushed aside
- Portable office cabin on blocks with an overhanging roof
- Two stacks of flattened car hulks and one intact wreck
- Tracked material handler with a raised boom and hanging magnet

## Details excluded
- No readable text or logo
- No branded vehicles

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 13.0 x 10.0 m

## Outputs
- `models/map/Claude_scrapyard_building/Claude_scrapyard_building.vox` (editable master)
- `models/map/Claude_scrapyard_building/model.json`
- `models/map/Claude_scrapyard_building/Claude_scrapyard_building.glb` (derived)
- `previews/map/Claude_scrapyard_building/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/e1_map_buildings.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
