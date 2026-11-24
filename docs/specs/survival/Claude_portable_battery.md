# Portable Battery
- Asset ID: Claude_portable_battery
- Base ID: portable_battery
- Creator: Claude
- Category: survival
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_B
- Scale family: full
- Intended uses: Power for lights/radio (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A portable power station a neighbour bought for camping and lent out after the outage. It charges from the generator and runs a lamp and the radio; a phone cable is still plugged into the front.

Condition: **lightly_used**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.325 m
- Depth (Y): 0.225 m
- Height (Z): 0.2375 m
- Grid: 26 x 18 x 19 cells at 0.0125 m (micro tier), 1,957 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the working / interaction side.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [13.0, 7.5, 0.0])
- Resolution rationale: 1.25 cm cells: a hand-sized pickup would be only 3-6 cells at 2.5 cm, losing the grip, cap or label that identifies it.

## Materials and colors
`black`, `charcoal`, `iron_edge`, `porcelain_deep`, `porcelain_mid`, `screen`, `screen_sheen`, `steel`, `steel_dark`, `steel_light`

## Details included
- Dark case with lighter vented end panels and catch-lit edges
- Rigid carry handle with a rubber grip
- Front panel: small dark display, two AC sockets, USB ports, power button
- A pale phone cable plugged in and trailing onto the floor

## Details excluded
- No glowing display or LEDs
- No brand or text

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 0.325 x 0.1875 m

## Outputs
- `models/survival/Claude_portable_battery/Claude_portable_battery.vox` (editable master)
- `models/survival/Claude_portable_battery/model.json`
- `models/survival/Claude_portable_battery/Claude_portable_battery.glb` (derived)
- `previews/survival/Claude_portable_battery/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/b2_survival_gear.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
