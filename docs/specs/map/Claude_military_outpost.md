# Military Outpost
- Asset ID: Claude_military_outpost
- Base ID: military_outpost
- Creator: Claude
- Category: map
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_E
- Scale family: full
- Intended uses: Regional-map destination (Weapons) (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A forward checkpoint compound thrown up to hold the county road. The unit pulled out in a hurry: the boom is down, the tents still pitched and one truck left behind.

Condition: **abandoned**.

## Silhouette
Square ring of tan barrier baskets around prefab barracks, olive tents, a truck and a thin radio mast.

## Dimensions and orientation
- Width (X): 14.0 m
- Depth (Y): 14.0 m
- Height (Z): 8.0 m
- Grid: 28 x 28 x 16 cells at 0.5 m (map tier), 1,919 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the street side / main entrance.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [14.0, 14.0, 0.0])
- Resolution rationale: 50 cm cells: regional-map scale, real-world metres with far fewer voxels; only massing, roofs, entrances and one identifying feature are modelled.

## Materials and colors
`black`, `card_dark`, `galv_dark`, `glass_dark`, `glass_deep`, `gravel`, `green`, `green_dark`, `khaki`, `khaki_dark`, `olive`, `olive_dark`, `paint_white`, `signal_red_dark`, `soil`, `steel_dark`, `steel_light`

## Details included
- Perimeter of 1 m sand-filled barrier baskets with a boom gate and a sandbagged guard post
- Two prefab barrack units with a radio mast
- Two olive ridge tents on the camera side
- Utility truck and fuel drums

## Details excluded
- No readable text, insignia or real-army markings

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 14.0 x 14.0 m

## Outputs
- `models/map/Claude_military_outpost/Claude_military_outpost.vox` (editable master)
- `models/map/Claude_military_outpost/model.json`
- `models/map/Claude_military_outpost/Claude_military_outpost.glb` (derived)
- `previews/map/Claude_military_outpost/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/e1_map_buildings.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
