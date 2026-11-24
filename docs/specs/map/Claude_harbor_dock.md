# Harbour Dock
- Asset ID: Claude_harbor_dock
- Base ID: harbor_dock
- Creator: Claude
- Category: map
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_E
- Scale family: full
- Intended uses: Regional-map infrastructure piece (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A small concrete jetty in the fishing harbour. The last boats left in a hurry: a crate stack was abandoned on the quay and the jib crane still has its hook out over the water.

Condition: **worn**.

## Silhouette
Raised concrete jetty with black fenders and bollards round its edge, an orange jib crane and a crate stack.

## Dimensions and orientation
- Width (X): 10.0 m
- Depth (Y): 16.0 m
- Height (Z): 5.0 m
- Grid: 20 x 32 x 10 cells at 0.5 m (map tier), 1,385 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the shore end; the jetty projects toward -Y with water on three sides.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [10.0, 16.0, 0.0])
- Resolution rationale: 50 cm cells: regional-map scale, real-world metres with far fewer voxels; only massing, roofs, entrances and one identifying feature are modelled.

## Materials and colors
`black`, `card`, `card_dark`, `charcoal`, `concrete`, `concrete_dark`, `concrete_hi`, `iron`, `line_yellow`, `pine_aged`, `pine_light`, `pine_mid`, `safety_orange_dark`, `steel_dark`, `wgrey_mid`

## Details included
- 1.5 m concrete jetty projecting from the shore (+Y) with joint lines
- Black rubber fenders and iron bollards along both sides and the end
- Yellow safety line, steps down to the water on the camera side
- Orange jib crane over the -X side, stacked timber crates and a pallet

## Details excluded
- No water, no boats
- No readable markings

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 10.0 x 16.0 m

## Outputs
- `models/map/Claude_harbor_dock/Claude_harbor_dock.vox` (editable master)
- `models/map/Claude_harbor_dock/model.json`
- `models/map/Claude_harbor_dock/Claude_harbor_dock.glb` (derived)
- `previews/map/Claude_harbor_dock/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/e2_map_infrastructure.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
