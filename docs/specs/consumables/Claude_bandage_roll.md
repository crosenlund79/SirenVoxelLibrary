# Bandage Roll
- Asset ID: Claude_bandage_roll
- Base ID: bandage_roll
- Creator: Claude
- Category: consumables
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_C
- Scale family: full
- Intended uses: Inventory item 'bandage' (health +20) (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A fresh roll of gauze from a bathroom cabinet's first-aid tin, just unwrapped. The loose end has been pulled out across the floor, ready to be cut.

Condition: **new**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.125 m
- Depth (Y): 0.1625 m
- Height (Z): 0.1 m
- Grid: 10 x 13 x 8 cells at 0.0125 m (micro tier), 389 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the label / opening side.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [5.0, 6.5, 0.0])
- Resolution rationale: 1.25 cm cells: a hand-sized pickup would be only 3-6 cells at 2.5 cm, losing the grip, cap or label that identifies it.

## Materials and colors
`porcelain`, `porcelain_hi`, `porcelain_mid`, `porcelain_shadow`

## Details included
- Clean 8-cell round roll lying on its side
- End faces show the wound layers and a darker core
- Loose tail unrolled flat from under the roll, with a soft fold and a frayed end

## Details excluded
- No packaging, clips or tape
- No blood

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 0.125 x 0.1625 m

## Outputs
- `models/consumables/Claude_bandage_roll/Claude_bandage_roll.vox` (editable master)
- `models/consumables/Claude_bandage_roll/model.json`
- `models/consumables/Claude_bandage_roll/Claude_bandage_roll.glb` (derived)
- `previews/consumables/Claude_bandage_roll/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/c2_consumables.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
