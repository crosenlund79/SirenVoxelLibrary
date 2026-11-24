# Candle
- Asset ID: Claude_candle
- Base ID: candle
- Creator: Claude
- Category: survival
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_B
- Scale family: full
- Intended uses: Night light (game candle) (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
An ivory pillar candle on a chipped sage saucer from the kitchen. It has been lit every evening since the outage and is burned halfway, wax spilled down one side; the spent match was dropped on the saucer.

Condition: **used**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.175 m
- Depth (Y): 0.175 m
- Height (Z): 0.1875 m
- Grid: 14 x 14 x 15 cells at 0.0125 m (micro tier), 517 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the working / interaction side.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [7.0, 7.0, 0.0])
- Resolution rationale: 1.25 cm cells: a hand-sized pickup would be only 3-6 cells at 2.5 cm, losing the grip, cap or label that identifies it.

## Materials and colors
`char`, `charcoal`, `cream`, `cream_hi`, `cream_mid`, `cream_shadow`, `pine_hi`, `porcelain`, `porcelain_mid`, `sage`, `sage_dark`, `sage_hi`

## Details included
- Pillar candle tunnelled at the top, one wall of wax left standing
- Curled black wick (unlit, no flame)
- Drips running down the camera side into a puddle on the saucer
- Sage glazed saucer with a chip showing the pale clay, a spent match

## Details excluded
- No flame or glow
- No candle holder glass

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 0.175 x 0.175 m

## Outputs
- `models/survival/Claude_candle/Claude_candle.vox` (editable master)
- `models/survival/Claude_candle/model.json`
- `models/survival/Claude_candle/Claude_candle.glb` (derived)
- `previews/survival/Claude_candle/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/b2_survival_gear.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
