# Dining Crockery Set
- Asset ID: Claude_dining_crockery
- Base ID: dining_crockery
- Creator: Claude
- Category: furniture
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_A
- Scale family: full
- Intended uses: Table dressing; kitchen clutter (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
The last clean things in the house: four dinner plates, a bowl, a mug and a tumbler put away on a folded tea towel after the final washing-up, and never used again.

Condition: **used**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.525 m
- Depth (Y): 0.3 m
- Height (Z): 0.125 m
- Grid: 21 x 12 x 5 cells at 0.025 m (fine tier), 595 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the side a person uses (seat, doors, drawers, controls).
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [10.5, 6.0, 0.0])
- Resolution rationale: 2.5 cm cells: a handheld or small gear item whose handles, straps and blades would be 2-4x too thick at 5 cm.

## Materials and colors
`blue_dark`, `blue_mid`, `cream`, `cream_mid`, `glass`, `glass_hi`, `porcelain`, `porcelain_hi`, `porcelain_mid`, `terra`, `terra_dark`, `terra_deep`, `terra_hi`

## Details included
- Stack of four dinner plates; the top plate shows its rim and sunken well
- White bowl with a foot ring
- Terracotta glazed mug with a loop handle
- Pale glass tumbler
- Folded cream tea towel with two faded blue stripes joins the set into one piece

## Details excluded
- No food
- No pattern noise on the plates

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 0.525 x 0.3 m

## Outputs
- `models/furniture/Claude_dining_crockery/Claude_dining_crockery.vox` (editable master)
- `models/furniture/Claude_dining_crockery/model.json`
- `models/furniture/Claude_dining_crockery/Claude_dining_crockery.glb` (derived)
- `previews/furniture/Claude_dining_crockery/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/a3_kitchen.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
