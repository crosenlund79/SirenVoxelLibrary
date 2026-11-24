# Handgun
- Asset ID: Claude_handgun
- Base ID: handgun
- Creator: Claude
- Category: survival
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_C
- Scale family: full
- Intended uses: The game's only weapon today (9 mm) (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A police-pattern service pistol carried in a belt holster for years, then left in a kitchen drawer when the sirens stopped. The slide's front edges are rubbed bright by the holster; the grip texture is worn smooth where the thumb rested.

Condition: **used**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.0375 m
- Depth (Y): 0.2375 m
- Height (Z): 0.1625 m
- Grid: 3 x 19 x 13 cells at 0.0125 m (micro tier), 321 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the working / interaction side.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [1.5, 9.5, 0.0])
- Resolution rationale: 1.25 cm cells: a hand-sized pickup would be only 3-6 cells at 2.5 cm, losing the grip, cap or label that identifies it.

## Materials and colors
`black`, `charcoal`, `iron`, `iron_edge`, `steel`, `steel_dark`, `steel_light`

## Details included
- Steel slide, lighter than the dark polymer frame, with rear serrations
- Front and rear sights
- Exposed barrel hood at the ejection port
- Stippled grip panels with a hand-polished front strap
- Trigger guard with trigger
- Holster-worn muzzle edges

## Details excluded
- No markings or serial plates
- No internal mechanism
- No light, optic or accessories

## Attachment points
- `grip`: voxel [1, 3, 4], [np.float64(0.0), np.float64(-0.075), np.float64(0.0562)] m from the pivot. Main hand on the grip, under the slide's rear.

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 0.0375 x 0.2375 m

## Outputs
- `models/survival/Claude_handgun/Claude_handgun.vox` (editable master)
- `models/survival/Claude_handgun/model.json`
- `models/survival/Claude_handgun/Claude_handgun.glb` (derived)
- `previews/survival/Claude_handgun/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/c1_combat.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
