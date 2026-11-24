# Road Barrier
- Asset ID: Claude_road_barrier
- Base ID: road_barrier
- Creator: Claude
- Category: map
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_E
- Scale family: full
- Intended uses: Regional-map infrastructure piece (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A checkpoint line thrown across a road: two concrete barriers, a manual boom between them and a cone at each end. Whoever manned it is gone; the boom is still down.

Condition: **worn**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 4.5 m
- Depth (Y): 1.0 m
- Height (Z): 1.5 m
- Grid: 9 x 2 x 3 cells at 0.5 m (map tier), 23 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the street side / main entrance.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [4.5, 1.0, 0.0])
- Resolution rationale: 50 cm cells: regional-map scale, real-world metres with far fewer voxels; only massing, roofs, entrances and one identifying feature are modelled.

## Materials and colors
`charcoal`, `concrete`, `concrete_hi`, `iron`, `paint_white`, `safety_orange`, `signal_red`

## Details included
- Two 1.5 m concrete barriers with a darker scuffed base
- Boom post with counterweight; striped arm lowered onto the right barrier
- A traffic cone in front of each barrier

## Details excluded
- No readable signs
- No people or vehicles

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 4.5 x 1.0 m

## Outputs
- `models/map/Claude_road_barrier/Claude_road_barrier.vox` (editable master)
- `models/map/Claude_road_barrier/model.json`
- `models/map/Claude_road_barrier/Claude_road_barrier.glb` (derived)
- `previews/map/Claude_road_barrier/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/e2_map_infrastructure.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
