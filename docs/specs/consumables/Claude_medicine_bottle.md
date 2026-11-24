# Medicine Bottle
- Asset ID: Claude_medicine_bottle
- Base ID: medicine_bottle
- Creator: Claude
- Category: consumables
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_C
- Scale family: full
- Intended uses: Medicine pickup (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A large amber pharmacy stock bottle of painkillers from a ransacked pharmacy counter. Handled a lot: the white label has a torn corner and the cap is scuffed.

Condition: **used**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.1 m
- Depth (Y): 0.1 m
- Height (Z): 0.1875 m
- Grid: 8 x 8 x 15 cells at 0.0125 m (micro tier), 484 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the label / opening side.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [4.0, 4.0, 0.0])
- Resolution rationale: 1.25 cm cells: a hand-sized pickup would be only 3-6 cells at 2.5 cm, losing the grip, cap or label that identifies it.

## Materials and colors
`label_blue`, `paper`, `porcelain`, `porcelain_hi`, `porcelain_mid`, `rust`, `rust_dark`

## Details included
- Clean 8-cell round amber bottle with a narrower neck
- White child-proof cap with grip ridges
- Plain white label wrapped round with a blue band; torn top corner

## Details excluded
- No text, dosage or pharmacy name
- No loose pills

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 0.1 x 0.1 m

## Outputs
- `models/consumables/Claude_medicine_bottle/Claude_medicine_bottle.vox` (editable master)
- `models/consumables/Claude_medicine_bottle/model.json`
- `models/consumables/Claude_medicine_bottle/Claude_medicine_bottle.glb` (derived)
- `previews/consumables/Claude_medicine_bottle/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/c2_consumables.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
