# Medical Bag
- Asset ID: Claude_medical_bag
- Base ID: medical_bag
- Creator: Claude
- Category: consumables
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_C
- Scale family: full
- Intended uses: Medical loot container (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A paramedic's duffel left in the back of an ambulance at a roadblock. It has been opened and closed many times since: the zips are intact, the base is grimy and the reflective band has dulled.

Condition: **used**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.4125 m
- Depth (Y): 0.2375 m
- Height (Z): 0.3125 m
- Grid: 33 x 19 x 25 cells at 0.0125 m (micro tier), 3,269 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the label / opening side.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [16.5, 9.5, 0.0])
- Resolution rationale: 1.25 cm cells: a hand-sized pickup would be only 3-6 cells at 2.5 cm, losing the grip, cap or label that identifies it. Overridden from 2.5 cm to 1.25 cm (the medical family's tier): zips, webbing and the cross patch are 1-3 cm features that would all become 2.5 cm bars, and the cross would shrink to a 3-cell plus.

## Materials and colors
`black`, `blue_dark`, `blue_deep`, `charcoal`, `galv`, `iron`, `navy`, `navy_dark`, `paper`, `signal_red`, `steel`, `steel_light`

## Details included
- Soft navy duffel with a rounded top and flat base
- Front zip pocket carrying a white patch with a red cross
- Zip end pockets
- Main zip along the top with a pull tab
- Two webbing carry handles joined by a wrap
- Shoulder strap clipped to both ends, lying along the top
- Dulled reflective band around the body

## Details excluded
- No text, service names or badges
- No visible medical contents

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 0.4125 x 0.2375 m

## Outputs
- `models/consumables/Claude_medical_bag/Claude_medical_bag.vox` (editable master)
- `models/consumables/Claude_medical_bag/model.json`
- `models/consumables/Claude_medical_bag/Claude_medical_bag.glb` (derived)
- `previews/consumables/Claude_medical_bag/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/c2_consumables.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
