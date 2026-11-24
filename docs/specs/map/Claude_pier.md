# Small Pier
- Asset ID: Claude_pier
- Base ID: pier
- Creator: Claude
- Category: map
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_E
- Scale family: full
- Intended uses: Regional-map infrastructure piece (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A timber fishing pier off the beach road. A winter storm took two deck boards near the far end; the rest is grey and splintered but still walked on.

Condition: **worn**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 4.0 m
- Depth (Y): 15.0 m
- Height (Z): 1.5 m
- Grid: 8 x 30 x 3 cells at 0.5 m (map tier), 318 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the shore end; the pier runs out toward -Y.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [4.0, 15.0, 0.0])
- Resolution rationale: 50 cm cells: regional-map scale, real-world metres with far fewer voxels; only massing, roofs, entrances and one identifying feature are modelled.

## Materials and colors
`steel`, `steel_light`, `wgrey`, `wgrey_dark`, `wgrey_deep`, `wgrey_mid`, `wgrey_warm`

## Details included
- Grey timber deck 1 m above the water on paired piles
- Pile heads standing proud of the deck along both edges
- Lighter worn walking line down the middle
- Two missing boards at the far end, steel ladder down to the water

## Details excluded
- No water, no boats

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 4.0 x 15.0 m

## Outputs
- `models/map/Claude_pier/Claude_pier.vox` (editable master)
- `models/map/Claude_pier/model.json`
- `models/map/Claude_pier/Claude_pier.glb` (derived)
- `previews/map/Claude_pier/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/e2_map_infrastructure.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
