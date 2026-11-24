# Battery Lantern
- Asset ID: Claude_battery_lantern
- Base ID: battery_lantern
- Creator: Claude
- Category: survival
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_B
- Scale family: full
- Intended uses: Night light (game lantern) (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A forest-green camping lantern that lived in the garage with the tent. Since the power went it has stood on the kitchen table every night; the batteries are almost done and nobody has found more.

Condition: **used**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.2 m
- Depth (Y): 0.1875 m
- Height (Z): 0.35 m
- Grid: 16 x 15 x 28 cells at 0.0125 m (micro tier), 1,476 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the working / interaction side.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [8.0, 7.5, 0.0])
- Resolution rationale: 1.25 cm cells: a hand-sized pickup would be only 3-6 cells at 2.5 cm, losing the grip, cap or label that identifies it.

## Materials and colors
`black`, `charcoal`, `green`, `green_dark`, `green_deep`, `porcelain`, `porcelain_mid`, `steel`, `steel_dark`, `steel_hi`, `steel_light`

## Details included
- Round green base with a rotary dial and a rubber foot ring
- Frosted globe (opaque, unlit) between four slim struts
- Vented top cap with a wire bail handle folded up
- Scuffs on the base rim where it is set down

## Details excluded
- No emissive globe or glow
- No brand marks

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 0.2 x 0.1875 m

## Outputs
- `models/survival/Claude_battery_lantern/Claude_battery_lantern.vox` (editable master)
- `models/survival/Claude_battery_lantern/model.json`
- `models/survival/Claude_battery_lantern/Claude_battery_lantern.glb` (derived)
- `previews/survival/Claude_battery_lantern/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/b2_survival_gear.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
