# Supermarket
- Asset ID: Claude_supermarket
- Base ID: supermarket
- Creator: Claude
- Category: map
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_E
- Scale family: full
- Intended uses: Regional-map destination (Grocery Store (current destination)) (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
The district supermarket, emptied shelf by shelf in the first fortnight. The carts are still corralled in the lot and a delivery was never unloaded at the side dock.

Condition: **abandoned**.

## Silhouette
Long low beige hall with a raised red sign panel over a glazed entrance canopy, side dock and a striped lot.

## Dimensions and orientation
- Width (X): 20.0 m
- Depth (Y): 15.0 m
- Height (Z): 7.0 m
- Grid: 40 x 30 x 14 cells at 0.5 m (map tier), 3,056 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the street side / main entrance.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [20.0, 15.0, 0.0])
- Resolution rationale: 50 cm cells: regional-map scale, real-world metres with far fewer voxels; only massing, roofs, entrances and one identifying feature are modelled.

## Materials and colors
`asphalt`, `beige`, `black`, `card`, `card_dark`, `concrete`, `concrete_dark`, `concrete_hi`, `galv`, `galv_hi`, `glass`, `glass_dark`, `glass_deep`, `glass_hi`, `hazard_yellow_dark`, `label_cream`, `label_red`, `line_white`, `maroon`, `roof`, `steel`, `steel_dark`

## Details included
- Big-box hall with pilaster rhythm, flat roof with HVAC and skylights
- Glazed entrance bay under a projecting canopy and a raised blank sign panel
- Raised loading dock with two roll-up doors on the camera side
- Parking lot with stalls, cart corral and one abandoned car

## Details excluded
- No readable text or logo

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 20.0 x 15.0 m

## Outputs
- `models/map/Claude_supermarket/Claude_supermarket.vox` (editable master)
- `models/map/Claude_supermarket/model.json`
- `models/map/Claude_supermarket/Claude_supermarket.glb` (derived)
- `previews/map/Claude_supermarket/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/e1_map_buildings.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
