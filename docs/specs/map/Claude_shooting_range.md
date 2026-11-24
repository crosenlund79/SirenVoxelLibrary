# Shooting Range
- Asset ID: Claude_shooting_range
- Base ID: shooting_range
- Creator: Claude
- Category: map
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_E
- Scale family: full
- Intended uses: Regional-map destination (Weapons) (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A members' outdoor range with a timber clubhouse. Targets are still pinned up from the last practice; the range became a meeting point, then a place to avoid.

Condition: **abandoned**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 16.0 m
- Depth (Y): 11.0 m
- Height (Z): 5.5 m
- Grid: 32 x 22 x 11 cells at 0.5 m (map tier), 1,763 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the street side / main entrance.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [16.0, 11.0, 0.0])
- Resolution rationale: 50 cm cells: regional-map scale, real-world metres with far fewer voxels; only massing, roofs, entrances and one identifying feature are modelled.

## Materials and colors
`concrete`, `concrete_dark`, `concrete_hi`, `galv`, `glass_dark`, `grass`, `gravel`, `paper`, `pine_dark`, `roof`, `soil`, `wgrey`, `wgrey_dark`, `wood_stain`

## Details included
- Low timber clubhouse with a grey gable roof
- Covered firing line with benches under a lean-to roof
- Four gravel lanes with short baffles and paper target frames
- Stepped 4.5 m earth backstop berm with a bare impact face

## Details excluded
- No readable text
- No weapons or people

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 16.0 x 11.0 m

## Outputs
- `models/map/Claude_shooting_range/Claude_shooting_range.vox` (editable master)
- `models/map/Claude_shooting_range/model.json`
- `models/map/Claude_shooting_range/Claude_shooting_range.glb` (derived)
- `previews/map/Claude_shooting_range/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/e1_map_buildings.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
