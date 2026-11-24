# Protective Vest
- Asset ID: Claude_protective_vest
- Base ID: protective_vest
- Creator: Claude
- Category: combat
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_C
- Scale family: full
- Intended uses: Planned protective vest (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A patrol officer's soft armour vest, unstrapped and stood on a locker-room bench for the last time. The carrier has faded at the shoulders, the hem is rubbed pale at the front and one shoulder tab has come loose.

Condition: **used**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.525 m
- Depth (Y): 0.3 m
- Height (Z): 0.6 m
- Grid: 21 x 12 x 24 cells at 0.025 m (fine tier), 1,146 occupied voxels
- Front direction: +Y (library voxel)
- Front: Working end / muzzle points +Y, top side up; lowest point on z = 0.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [10.5, 6.0, 0.0])
- Resolution rationale: 2.5 cm cells: a handheld or small gear item whose handles, straps and blades would be 2-4x too thick at 5 cm.

## Materials and colors
`black`, `blue_dark`, `blue_deep`, `charcoal`, `denim_dark`, `navy`, `navy_dark`

## Details included
- Front and back panels joined by shoulder straps; open neck and armholes
- Velcro ID panel on the chest (blank, no lettering)
- Two magazine pouches and a small radio pouch with flaps
- Elastic side straps with tabs
- Drag loop at the back collar
- Sun-faded shoulders, scuffed front hem, one lifted shoulder tab

## Details excluded
- No 'POLICE' or other lettering, no badges or flags
- No visible armour plate

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 0.525 x 0.3 m

## Outputs
- `models/combat/Claude_protective_vest/Claude_protective_vest.vox` (editable master)
- `models/combat/Claude_protective_vest/model.json`
- `models/combat/Claude_protective_vest/Claude_protective_vest.glb` (derived)
- `previews/combat/Claude_protective_vest/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/c1_combat.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
