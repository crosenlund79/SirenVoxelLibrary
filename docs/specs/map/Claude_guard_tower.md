# Guard Tower
- Asset ID: Claude_guard_tower
- Base ID: guard_tower
- Creator: Claude
- Category: map
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_E
- Scale family: full
- Intended uses: Regional-map destination (Weapons) (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A timber watchtower over a perimeter road. The last guard climbed down and never came back; the searchlight still points at the gate.

Condition: **abandoned**.

## Silhouette
Tall braced timber stilt frame carrying a box cabin with an open window band and a pyramid metal roof.

## Dimensions and orientation
- Width (X): 4.0 m
- Depth (Y): 4.0 m
- Height (Z): 10.5 m
- Grid: 8 x 8 x 21 cells at 0.5 m (map tier), 382 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the street side / main entrance.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [4.0, 4.0, 0.0])
- Resolution rationale: 50 cm cells: regional-map scale, real-world metres with far fewer voxels; only massing, roofs, entrances and one identifying feature are modelled.

## Materials and colors
`galv`, `galv_hi`, `steel`, `steel_hi`, `wgrey`, `wgrey_dark`, `wgrey_deep`, `wgrey_hi`, `wgrey_mid`

## Details included
- Four timber legs with girts and diagonal braces
- Cabin with a solid lower wall, open window band and corner posts
- Galvanised pyramid roof, timber ladder on the street side
- Searchlight on the front corner

## Details excluded
- No readable text

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 4.0 x 4.0 m

## Outputs
- `models/map/Claude_guard_tower/Claude_guard_tower.vox` (editable master)
- `models/map/Claude_guard_tower/model.json`
- `models/map/Claude_guard_tower/Claude_guard_tower.glb` (derived)
- `previews/map/Claude_guard_tower/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/e1_map_buildings.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
