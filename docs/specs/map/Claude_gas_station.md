# Gas Station
- Asset ID: Claude_gas_station
- Base ID: gas_station
- Creator: Claude
- Category: map
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_E
- Scale family: full
- Intended uses: Regional-map destination (Fuel) (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A two-island filling station on the main road. The tanks were pumped dry in the first days; a car was abandoned at the pumps and one pump was knocked flat by a reversing truck.

Condition: **abandoned**.

## Silhouette
Wide flat white canopy with a red stripe on columns over two pump islands, kiosk behind, blank price sign.

## Dimensions and orientation
- Width (X): 13.0 m
- Depth (Y): 12.0 m
- Height (Z): 5.0 m
- Grid: 26 x 24 x 10 cells at 0.5 m (map tier), 1,397 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the street side / main entrance.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [13.0, 12.0, 0.0])
- Resolution rationale: 50 cm cells: regional-map scale, real-world metres with far fewer voxels; only massing, roofs, entrances and one identifying feature are modelled.

## Materials and colors
`black`, `bluegrey`, `charcoal`, `concrete`, `concrete_dark`, `concrete_deep`, `concrete_hi`, `galv_hi`, `glass`, `glass_dark`, `glass_deep`, `grass`, `label_red`, `paint_white`, `paint_white_shadow`, `plaster`, `roof`, `screen`, `steel`, `steel_dark`

## Details included
- Flat canopy with a white fascia and red stripe on four columns
- Two kerbed pump islands with four pumps, one knocked over
- Kiosk shop with a glazed front at the back of the forecourt
- Blank price sign on a pole at the corner

## Details excluded
- No readable text, prices or brand

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 13.0 x 12.0 m

## Outputs
- `models/map/Claude_gas_station/Claude_gas_station.vox` (editable master)
- `models/map/Claude_gas_station/model.json`
- `models/map/Claude_gas_station/Claude_gas_station.glb` (derived)
- `previews/map/Claude_gas_station/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/e1_map_buildings.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
