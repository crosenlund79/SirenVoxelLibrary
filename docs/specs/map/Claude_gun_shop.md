# Gun Shop
- Asset ID: Claude_gun_shop
- Base ID: gun_shop
- Creator: Claude
- Category: map
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_E
- Scale family: full
- Intended uses: Regional-map destination (Weapons) (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
An independent gun shop in a strip of small units. The owner barred everything that opened, sandbagged a chicane at the door and held out for a week before the shop went dark.

Condition: **abandoned**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 8.0 m
- Depth (Y): 9.0 m
- Height (Z): 5.0 m
- Grid: 16 x 18 x 10 cells at 0.5 m (map tier), 884 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the street side / main entrance.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [8.0, 9.0, 0.0])
- Resolution rationale: 50 cm cells: regional-map scale, real-world metres with far fewer voxels; only massing, roofs, entrances and one identifying feature are modelled.

## Materials and colors
`asphalt`, `charcoal`, `concrete`, `concrete_dark`, `concrete_hi`, `galv`, `galv_hi`, `glass_dark`, `khaki`, `khaki_dark`, `line_white`, `olive_dark`, `roof`, `steel_light`

## Details included
- Concrete-block box with a dark blank sign band
- Two barred shopfront windows and a steel door under a roll-down shutter box
- Sandbag chicane in front of the door
- Flat roof with parapet

## Details excluded
- No readable text, logo or weapon silhouettes

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 8.0 x 9.0 m

## Outputs
- `models/map/Claude_gun_shop/Claude_gun_shop.vox` (editable master)
- `models/map/Claude_gun_shop/model.json`
- `models/map/Claude_gun_shop/Claude_gun_shop.glb` (derived)
- `previews/map/Claude_gun_shop/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/e1_map_buildings.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
